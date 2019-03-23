# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author(s): Will Woods <wwoods@redhat.com>

"""system_upgrade.py - DNF plugin to handle major-version system upgrades."""

from __future__ import unicode_literals
from distutils.version import StrictVersion
from subprocess import call, Popen
import json
import os
import os.path
import uuid

from systemd import journal

from dnfpluginsextras import _, logger

import dnf
import dnf.cli
from dnf.cli import CliError
import dnf.transaction

import libdnf.conf


# Translators: This string is only used in unit tests.
_("the color of the sky")

DOWNLOAD_FINISHED_ID = uuid.UUID('9348174c5cc74001a71ef26bd79d302e')
REBOOT_REQUESTED_ID = uuid.UUID('fef1cc509d5047268b83a3a553f54b43')
UPGRADE_STARTED_ID = uuid.UUID('3e0a5636d16b4ca4bbe5321d06c6aa62')
UPGRADE_FINISHED_ID = uuid.UUID('8cec00a1566f4d3594f116450395f06c')

ID_TO_IDENTIFY_BOOTS = UPGRADE_STARTED_ID

DNFVERSION = StrictVersion(dnf.const.VERSION)

PLYMOUTH = '/usr/bin/plymouth'
DEFAULT_DATADIR = '/var/lib/dnf/system-upgrade'
MAGIC_SYMLINK = '/system-update'

RELEASEVER_MSG = _(
    "Need a --releasever greater than the current system version.")
DOWNLOAD_FINISHED_MSG = _(  # Translators: do not change "reboot" here
    "Download complete! Use 'dnf system-upgrade reboot' to start the upgrade.\n"
    "To remove cached metadata and transaction use 'dnf system-upgrade clean'")
CANT_RESET_RELEASEVER = _(
    "Sorry, you need to use 'download --releasever' instead of '--network'")

# --- Miscellaneous helper functions ------------------------------------------


def reboot():
    Popen(["systemctl", "reboot"])


# DNF-FIXME: dnf.util.clear_dir() doesn't delete regular files :/
def clear_dir(path):
    if not os.path.isdir(path):
        return

    for entry in os.listdir(path):
        fullpath = os.path.join(path, entry)
        try:
            if os.path.isdir(fullpath):
                dnf.util.rm_rf(fullpath)
            else:
                os.unlink(fullpath)
        except OSError:
            pass


def checkReleaseVer(conf, target=None):
    if dnf.rpm.detect_releasever(conf.installroot) == conf.releasever:
        raise CliError(RELEASEVER_MSG)
    if target and target != conf.releasever:
        # it's too late to set releasever here, so this can't work.
        # (see https://bugzilla.redhat.com/show_bug.cgi?id=1212341)
        raise CliError(CANT_RESET_RELEASEVER)


def disable_blanking():
    try:
        tty = open('/dev/tty0', 'wb')
        tty.write(b'\33[9;0]')
    except Exception as e:
        print(_("Screen blanking can't be disabled: %s") % e)

# --- State object - for tracking upgrade state between runs ------------------


# DNF-INTEGRATION-NOTE: basically the same thing as dnf.persistor.JSONDB
class State(object):
    statefile = '/var/lib/dnf/system-upgrade.json'

    def __init__(self):
        self._data = {}
        self._read()

    def _read(self):
        try:
            with open(self.statefile) as fp:
                self._data = json.load(fp)
        except IOError:
            self._data = {}
        except ValueError:
            self._data = {}
            logger.warning(_("Failed loading state file: %s, continuing with "
                             "empty state."), self.statefile)

    def write(self):
        dnf.util.ensure_dir(os.path.dirname(self.statefile))
        with open(self.statefile, 'w') as outf:
            json.dump(self._data, outf)

    def clear(self):
        if os.path.exists(self.statefile):
            os.unlink(self.statefile)
        self._read()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.write()

    # helper function for creating properties. pylint: disable=protected-access
    def _prop(option):  # pylint: disable=no-self-argument
        def setprop(self, value):
            self._data[option] = value

        def getprop(self):
            return self._data.get(option)
        return property(getprop, setprop)

    download_status = _prop("download_status")
    destdir = _prop("destdir")
    target_releasever = _prop("target_releasever")
    system_releasever = _prop("system_releasever")
    gpgcheck = _prop("gpgcheck")
    upgrade_status = _prop("upgrade_status")
    distro_sync = _prop("distro_sync")
    allow_erasing = _prop("allow_erasing")
    enable_disable_repos = _prop("enable_disable_repos")
    best = _prop("best")
    exclude = _prop("exclude")
    install_packages = _prop("install_packages")
    install_weak_deps = _prop("install_weak_deps")
    module_platform_id = _prop("module_platform_id")

# --- Plymouth output helpers -------------------------------------------------


class PlymouthOutput(object):
    """A plymouth output helper class that filters duplicate calls, and stops
    calling the plymouth binary if we fail to contact it."""
    def __init__(self):
        self.alive = True
        self._last_args = dict()
        self._last_msg = None

    def _plymouth(self, cmd, *args):
        dupe_cmd = (args == self._last_args.get(cmd))
        if (self.alive and not dupe_cmd) or cmd == '--ping':
            try:
                self.alive = (call((PLYMOUTH, cmd) + args) == 0)
            except OSError:
                self.alive = False
            self._last_args[cmd] = args
        return self.alive

    def ping(self):
        return self._plymouth("--ping")

    def message(self, msg):
        if self._last_msg and self._last_msg != msg:
            self._plymouth("hide-message", "--text", self._last_msg)
        self._last_msg = msg
        return self._plymouth("display-message", "--text", msg)

    def set_mode(self, mode):
        return self._plymouth("change-mode", "--" + mode)

    def progress(self, percent):
        return self._plymouth("system-update", "--progress", str(percent))

# A single PlymouthOutput instance for us to use within this module
Plymouth = PlymouthOutput()


# A TransactionProgress class that updates plymouth for us.
class PlymouthTransactionProgress(dnf.callback.TransactionProgress):

    # pylint: disable=too-many-arguments
    def progress(self, package, action, ti_done, ti_total, ts_done, ts_total):
        self._update_plymouth(package, action, ts_done, ts_total)

    def _update_plymouth(self, package, action, current, total):
        Plymouth.progress(int(100.0 * current / total))
        Plymouth.message(self._fmt_event(package, action, current, total))

    def _fmt_event(self, package, action, current, total):
        action = dnf.transaction.ACTIONS.get(action, action)
        return "[%d/%d] %s %s..." % (current, total, action, package)

# --- journal helpers -------------------------------------------------


def find_boots(message_id):
    """Find all boots with this message id.

    Returns the entries of all found boots.
    """
    j = journal.Reader()
    j.add_match(MESSAGE_ID=message_id.hex,  # identify the message
                _UID=0)                     # prevent spoofing of logs

    oldboot = None
    for entry in j:
        boot = entry['_BOOT_ID']
        if boot == oldboot:
            continue
        oldboot = boot
        yield entry


def list_logs():
    print(_('The following boots appear to contain upgrade logs:'))
    n = -1
    for n, entry in enumerate(find_boots(ID_TO_IDENTIFY_BOOTS)):
        print('{} / {.hex}: {:%Y-%m-%d %H:%M:%S} {}→{}'.format(
            n + 1,
            entry['_BOOT_ID'],
            entry['__REALTIME_TIMESTAMP'],
            entry.get('SYSTEM_RELEASEVER', '??'),
            entry.get('TARGET_RELEASEVER', '??')))
    if n == -1:
        print(_('-- no logs were found --'))


def pick_boot(message_id, n):
    boots = list(find_boots(message_id))
    # Positive indices index all found boots starting with 1 and going forward,
    # zero is the current boot, and -1, -2, -3 are previous going backwards.
    # This is the same as journalctl.
    try:
        if n == 0:
            raise IndexError
        if n > 0:
            n -= 1
        return boots[n]['_BOOT_ID']
    except IndexError:
        raise CliError(_("Cannot find logs with this index."))


def show_log(n):
    boot_id = pick_boot(ID_TO_IDENTIFY_BOOTS, n)
    process = Popen(['journalctl', '--boot', boot_id.hex])
    process.wait()
    rc = process.returncode
    if rc == 1:
        raise dnf.exceptions.Error(_("Unable to match systemd journal entry"))


CMDS = ['download', 'clean', 'reboot', 'upgrade', 'log']

# --- The actual Plugin and Command objects! ----------------------------------


class SystemUpgradePlugin(dnf.Plugin):
    name = 'system-upgrade'

    def __init__(self, base, cli):
        super(SystemUpgradePlugin, self).__init__(base, cli)
        if cli:
            cli.register_command(SystemUpgradeCommand)


class SystemUpgradeCommand(dnf.cli.Command):
    aliases = ('system-upgrade', 'fedup')
    summary = _("Prepare system for upgrade to a new release")

    def __init__(self, cli):
        super(SystemUpgradeCommand, self).__init__(cli)
        self.state = State()

    @staticmethod
    def set_argparser(parser):
        parser.add_argument("--no-downgrade", dest='distro_sync',
                            action='store_false',
                            help=_("keep installed packages if the new "
                                   "release's version is older"))
        parser.add_argument('tid', nargs=1, choices=CMDS,
                            metavar="[%s]" % "|".join(CMDS))
        parser.add_argument('--number', type=int, help=_('which logs to show'))

    def log_status(self, message, message_id):
        "Log directly to the journal"
        journal.send(message,
                     MESSAGE_ID=message_id,
                     PRIORITY=journal.LOG_NOTICE,
                     SYSTEM_RELEASEVER=self.state.system_releasever,
                     TARGET_RELEASEVER=self.state.target_releasever,
                     DNF_VERSION=dnf.const.VERSION)

    def pre_configure(self):
        self._call_sub("pre_configure")

    def configure(self):
        self._call_sub("configure")
        self._call_sub("check")

    def run(self):
        self._call_sub("run")

    def run_transaction(self):
        self._call_sub("transaction")

    def _call_sub(self, name):
        subfunc = getattr(self, name + '_' + self.opts.tid[0], None)
        if callable(subfunc):
            subfunc()

    def _set_cachedir(self):
        # set download directories from json state file
        self.base.conf.cachedir = DEFAULT_DATADIR
        self.base.conf.destdir = self.state.destdir if self.state.destdir else None

    # == pre_configure_*: set up action-specific demands ==========================
    def pre_configure_download(self):
        # only download subcommand accepts --destdir command line option
        self.base.conf.cachedir = DEFAULT_DATADIR
        self.base.conf.destdir = self.opts.destdir if self.opts.destdir else None

    def pre_configure_reboot(self):
        self._set_cachedir()

    def pre_configure_upgrade(self):
        self._set_cachedir()
        if self.state.enable_disable_repos:
            self.opts.repos_ed = self.state.enable_disable_repos
        self.base.conf.releasever = self.state.target_releasever

    def pre_configure_clean(self):
        self._set_cachedir()

    # == configure_*: set up action-specific demands ==========================

    def configure_download(self):
        if self.base._promptWanted():
            msg = _('Before you continue ensure that your system is fully upgraded by running '
                    '"dnf --refresh upgrade". Do you want to continue')
            if self.base.conf.assumeno or not self.base.output.userconfirm(
                    msg='{} [y/N]: '.format(msg), defaultyes_msg='{} [Y/n]: '.format(msg)):
                raise CliError(_("Operation aborted."))
        self.cli.demands.root_user = True
        self.cli.demands.resolving = True
        self.cli.demands.available_repos = True
        self.cli.demands.sack_activation = True
        self.cli.demands.freshest_metadata = True
        # We want to do the depsolve / download / transaction-test, but *not*
        # run the actual RPM transaction to install the downloaded packages.
        # Setting the "test" flag makes the RPM transaction a test transaction,
        # so nothing actually gets installed.
        # (It also means that we run two test transactions in a row, which is
        # kind of silly, but that's something for DNF to fix...)
        self.base.conf.tsflags += ["test"]

    def configure_reboot(self):
        # FUTURE: add a --debug-shell option to enable debug shell:
        # systemctl add-wants system-update.target debug-shell.service
        self.cli.demands.root_user = True

    def configure_upgrade(self):
        # same as the download, but offline and non-interactive. so...
        self.cli.demands.root_user = True
        self.cli.demands.resolving = True
        self.cli.demands.available_repos = True
        self.cli.demands.sack_activation = True
        # use the saved value for --allowerasing, etc.
        self.opts.distro_sync = self.state.distro_sync
        self.cli.demands.allow_erasing = self.state.allow_erasing
        self.base.conf.gpgcheck = self.state.gpgcheck
        self.base.conf.best = self.state.best
        if self.state.exclude is None:
            self.state.exclude = []
        self.base.conf.exclude = libdnf.conf.VectorString(self.state.exclude)
        self.base.conf.install_weak_deps = self.state.install_weak_deps
        self.base.conf.module_platform_id = self.state.module_platform_id
        # don't try to get new metadata, 'cuz we're offline
        self.cli.demands.cacheonly = True
        # and don't ask any questions (we confirmed all this beforehand)
        self.base.conf.assumeyes = True
        self.cli.demands.transaction_display = PlymouthTransactionProgress()

    def configure_clean(self):
        self.cli.demands.root_user = True

    def configure_log(self):
        pass

    # == check_*: do any action-specific checks ===============================

    def check_download(self):
        checkReleaseVer(self.base.conf, target=self.opts.releasever)
        dnf.util.ensure_dir(self.base.conf.cachedir)
        if self.base.conf.destdir:
            dnf.util.ensure_dir(self.base.conf.destdir)

    def check_reboot(self):
        if not self.state.download_status == 'complete':
            raise CliError(_("system is not ready for upgrade"))
        if os.path.lexists(MAGIC_SYMLINK):
            raise CliError(_("upgrade is already scheduled"))
        dnf.util.ensure_dir(DEFAULT_DATADIR)
        # FUTURE: checkRPMDBStatus(self.state.download_transaction_id)

    def check_upgrade(self):
        if not os.path.lexists(MAGIC_SYMLINK):
            logger.info(_("trigger file does not exist. exiting quietly."))
            raise SystemExit(0)
        if os.readlink(MAGIC_SYMLINK) != DEFAULT_DATADIR:
            logger.info(_("another upgrade tool is running. exiting quietly."))
            raise SystemExit(0)
        # Delete symlink ASAP to avoid reboot loops
        dnf.yum.misc.unlink_f(MAGIC_SYMLINK)
        if not self.state.upgrade_status == 'ready':
            raise CliError(  # Translators: do not change "reboot" here
                _("use 'dnf system-upgrade reboot' to begin the upgrade"))

    # == run_*: run the action/prep the transaction ===========================

    def run_prepare(self):
        # make the magic symlink
        os.symlink(DEFAULT_DATADIR, MAGIC_SYMLINK)
        # set upgrade_status so that the upgrade can run
        with self.state as state:
            state.upgrade_status = 'ready'

    def run_reboot(self):
        self.run_prepare()

        if not self.opts.tid[0] == "reboot":
            return

        self.log_status(_("Rebooting to perform upgrade."),
                        REBOOT_REQUESTED_ID)
        reboot()

    def run_download(self):
        # Mark everything in the world for upgrade/sync
        if self.opts.distro_sync:
            self.base.distro_sync()
        else:
            self.base.upgrade_all()

        with self.state as state:
            state.download_status = 'downloading'
            state.target_releasever = self.base.conf.releasever
            state.exclude = list(self.base.conf.exclude)
            state.destdir = self.base.conf.destdir

    def run_upgrade(self):
        # change the upgrade status (so we can detect crashed upgrades later)
        with self.state as state:
            state.upgrade_status = 'incomplete'

        self.log_status(_("Starting system upgrade. This will take a while."),
                        UPGRADE_STARTED_ID)

        # reset the splash mode and let the user know we're running
        Plymouth.set_mode("updates")
        Plymouth.progress(0)
        Plymouth.message(_("Starting system upgrade. This will take a while."))

        # disable screen blanking
        disable_blanking()

        # NOTE: We *assume* that depsolving here will yield the same
        # transaction as it did during the download, but we aren't doing
        # anything to *ensure* that; if the metadata changed, or if depsolving
        # is non-deterministic in some way, we could end up with a different
        # transaction and then the upgrade will fail due to missing packages.
        #
        # One way to *guarantee* that we have the same transaction would be
        # to save & restore the Transaction object, but there's no documented
        # way to save a Transaction to disk.
        #
        # So far, though, the above assumption seems to hold. So... onward!

        # add the downloaded RPMs to the sack

        errs = []

        for repo_id, pkg_spec_list in self.state.install_packages.items():
            for pkgspec in pkg_spec_list:
                try:
                    self.base.install(pkgspec, reponame=repo_id)
                except dnf.exceptions.MarkingError:
                    msg = _('Unable to match package: %s')
                    logger.info(msg, self.base.output.term.bold(pkgspec + " " + repo_id))
                    errs.append(pkgspec)

        if errs:
            raise dnf.exceptions.MarkingError(_("Unable to match some of packages"))

    def run_clean(self):
        logger.info(_("Cleaning up downloaded data..."))
        clear_dir(self.base.conf.cachedir)
        if self.base.conf.destdir:
            clear_dir(self.base.conf.destdir)
        with self.state as state:
            state.download_status = None
            state.upgrade_status = None
            state.destdir = None
            state.install_packages = {}

    def run_log(self):
        if self.opts.number:
            show_log(self.opts.number)
        else:
            list_logs()

    # == transaction_*: do stuff after a successful transaction ===============

    def transaction_download(self):
        downloads = self.cli.base.transaction.install_set
        install_packages = {}
        for pkg in downloads:
            install_packages.setdefault(pkg.repo.id, []).append(str(pkg))

        # Okay! Write out the state so the upgrade can use it.
        system_ver = dnf.rpm.detect_releasever(self.base.conf.installroot)
        with self.state as state:
            state.download_status = 'complete'
            state.distro_sync = self.opts.distro_sync
            state.allow_erasing = self.cli.demands.allow_erasing
            state.gpgcheck = self.base.conf.gpgcheck
            state.best = self.base.conf.best
            state.system_releasever = system_ver
            state.target_releasever = self.base.conf.releasever
            state.install_packages = install_packages
            state.install_weak_deps = self.base.conf.install_weak_deps
            state.module_platform_id = self.base.conf.module_platform_id
            state.enable_disable_repos = self.opts.repos_ed
            state.destdir = self.base.conf.destdir
        logger.info(DOWNLOAD_FINISHED_MSG)
        self.log_status(_("Download finished."),
                        DOWNLOAD_FINISHED_ID)

    def transaction_upgrade(self):
        Plymouth.message(_("Upgrade complete! Cleaning up and rebooting..."))
        self.log_status(_("Upgrade complete! Cleaning up and rebooting..."),
                        UPGRADE_FINISHED_ID)
        self.run_clean()
        if self.opts.tid[0] == "upgrade":
            reboot()
