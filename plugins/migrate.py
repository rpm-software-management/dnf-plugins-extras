#
# Copyright (C) 2015  Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#

from __future__ import absolute_import
from __future__ import unicode_literals

from dnf.yum.history import YumHistory, YumHistoryPackage
from subprocess import check_output

import contextlib
import dnf
import dnf.cli
import dnfpluginsextras
import glob
import logging
import os
import re
import yum

_ = dnfpluginsextras._
logger = dnfpluginsextras.logger


class _YumBase(yum.YumBase):

    """YUM's base extended for a use in this plugin."""

    def __init__(self):
        """Initialize the base."""
        super(_YumBase, self).__init__()
        self.logger = logger
        self.verbose_logger = logger

    def iter_yumdb(self, onerror):
        """Return a new iterator over pkgtups and pkgids in the YUMDB."""
        dirname_glob = os.path.join(self.rpmdb.yumdb.conf.db_path, "*", "*")
        for dirname in glob.glob(dirname_glob):
            basename = os.path.basename(dirname)
            match = re.match(
                r"^([^-]+)-(.+)-([^-]+)-([^-]+)-([^-]+)$", basename)
            if not match:
                onerror(_("failed to parse package NEVRA from: %s"), basename)
                continue
            pkgid, name, version, release, architecture = match.groups()
            yield (name, architecture, "", version, release), pkgid


class Migrate(dnf.Plugin):

    name = "migrate"

    def __init__(self, base, cli):
        super(Migrate, self).__init__(base, cli)
        self.base = base
        self.cli = cli
        if self.cli is not None:
            self.cli.register_command(MigrateCommand)


class MigrateCommand(dnf.cli.Command):

    aliases = ("migrate",)
    summary = _("migrate yum's history, group and yumdb data to dnf")
    usage = "[%s] [%s]" % (_("OPTIONS"), _("KEYWORDS"))

    def __init__(self, cli):
        super(MigrateCommand, self).__init__(cli)
        self.dump_file = None

    def configure(self, args):
        demands = self.cli.demands
        demands.available_repos = True
        demands.sack_activation = True
        demands.root_user = True

    @staticmethod
    def _parse_args(args):
        parser = dnfpluginsextras.ArgumentParser(MigrateCommand.aliases[0])
        parser.add_argument("migrate", nargs="?", action="store",
                            choices=["all", "history", "groups", "yumdb"],
                            default="all",
                            help=_("which kind of yum data migrate."))
        opts = parser.parse_args(args)
        if opts.help_cmd:
            print(parser.format_help())
            return

        if opts.migrate == "all":
            opts.migrate = ["history", "groups", "yumdb"]
        else:
            opts.migrate = [opts.migrate]

        return opts

    def run(self, args):
        opts = self._parse_args(args)

        if not opts:
            return

        if "history" in opts.migrate:
            self.migrate_history()

        # Run before groups migration since it creates YUMDB records
        # consisting of group_member only which results in some warnings
        # generated by YUMDB migration.
        if "yumdb" in opts.migrate:
            self.migrate_yumdb()

        if "groups" in opts.migrate:
            self.migrate_groups()

    def migrate_history(self):
        logger.info(_("Migrating history data..."))
        yum_history = YumHistory("/var/lib/yum/history", None)
        dnf_history = YumHistory(self.base.conf.persistdir + "/history", None)

        self.migrate_history_pkgs(yum_history, dnf_history)
        self.migrate_history_transction(yum_history, dnf_history)
        self.migrate_history_reorder(dnf_history)

    def migrate_history_pkgs(self, yum_hist, dnf_hist):
        yum_cur = yum_hist._get_cursor()
        yum_cur.execute("""
            select pkgtupid, name, arch, epoch, version, release, checksum
              from pkgtups""")
        for (pid, name, arch, epoch, version, release, checksum) \
                in yum_cur.fetchall():
            ypkg = YumHistoryPackage(name, arch, epoch, version, release,
                                     checksum)
            pid = dnf_hist.pkg2pid(ypkg)
            self.migrate_history_pkgs_anydb(yum_hist, dnf_hist, pid, ypkg, "rpm")
            self.migrate_history_pkgs_anydb(yum_hist, dnf_hist, pid, ypkg, "yum")
        dnf_hist._get_cursor()
        dnf_hist._commit()

    @staticmethod
    def migrate_history_pkgs_anydb(yum_hist, dnf_hist, yumid, pkg, dbname):
        yum_cur = yum_hist._get_cursor()
        select = """select {db}db_key, {db}db_val
                    from pkg_{db}db where pkgtupid = ?""".format(db=dbname)
        yum_cur.execute(select, (yumid,))
        dnf_hist._wipe_anydb(pkg, dbname)
        for row in yum_cur.fetchall():
            dnf_hist._save_anydb_key(pkg, dbname, row[0], row[1])

    @staticmethod
    def migrate_history_transction(yum_hist, dnf_hist):
        yum_trans_list = yum_hist.old()
        dnf_cur = dnf_hist._get_cursor()
        for t in yum_trans_list:
            dnf_cur.execute("""select 1 from trans_beg
                                where timestamp = ?
                                  and rpmdb_version = ?
                                  and loginuid = ?""",
                            (t.beg_timestamp, t.beg_rpmdbversion, t.loginuid))
            if dnf_cur.fetchone():
                # skip akready migrated transactions
                continue
            dnf_cur.execute("""insert into trans_beg
                    (timestamp, rpmdb_version, loginuid) values (?, ?, ?)""",
                            (t.beg_timestamp, t.beg_rpmdbversion, t.loginuid))
            dnf_tid = dnf_cur.lastrowid
            if t.cmdline:
                dnf_cur.execute("""insert into trans_cmdline
                    (tid, cmdline) values (?, ?)""", (dnf_tid, t.cmdline))
            if t.end_timestamp:
                dnf_cur.execute("""insert into trans_end
                    (tid, timestamp, rpmdb_version, return_code)
                    values (?, ?, ?, ?)""",
                                (dnf_tid, t.end_timestamp, t.end_rpmdbversion,
                                 t.return_code))
            for pkg in t.trans_with:
                pid = dnf_hist.pkg2pid(pkg)
                dnf_cur.execute("""insert into trans_with_pkgs
                    (tid, pkgtupid) values (?, ?)""", (dnf_tid, pid))
            for pkg in t.trans_data:
                pid = dnf_hist.pkg2pid(pkg)
                dnf_cur.execute("""insert into trans_data_pkgs
                    (tid, pkgtupid, done, state) values (?, ?, ?, ?)""",
                                (dnf_tid, pid, pkg.done, pkg.state))
            for pkg in t.trans_skip:
                pid = dnf_hist.pkg2pid(pkg)
                dnf_cur.execute("""insert into trans_skip_pkgs
                    (tid, pkgtupid) values (?, ?)""", (dnf_tid, pid))
            for prob in t.rpmdb_problems:
                dnf_cur.execute("""insert into trans_rpmdb_problems
                    (tid, problem, msg)  values (?, ?, ?)""",
                                (dnf_tid, prob.problem, prob.text))
                rpid = dnf_cur.lastrowid
                for pkg in prob.packages:
                    pid = dnf_hist.pkg2pid(pkg)
                    dnf_cur.execute("""insert into trans_prob_pkgs
                        (rpid, pkgtupid, main) values (?, ?, ?)""",
                                    (rpid, pid, pkg.main))
            for err in t.errors:
                dnf_cur.execute("""insert into trans_error
                    (tid, msg)  values (?, ?)""", (dnf_tid, err))
            for msg in t.output:
                dnf_cur.execute("""insert into trans_script_stdout
                    (tid, line) values (?, ?)""", (dnf_tid, msg))
            dnf_hist._commit()

    @staticmethod
    def migrate_history_reorder(dnf_hist):
        dnf_cur = dnf_hist._get_cursor()
        dnf_cur.execute("""select max(tid) from trans_beg""")
        new_tid = dnf_cur.fetchone()[0]
        dnf_cur.execute("""select tid from trans_beg order by timestamp asc""")
        for row in dnf_cur.fetchall():
            old_tid = row[0]
            new_tid += 1
            for table in ["trans_beg", "trans_cmdline", "trans_end",
                          "trans_with_pkgs", "trans_data_pkgs",
                          "trans_skip_pkgs", "trans_rpmdb_problems",
                          "trans_error", "trans_script_stdout"]:
                dnf_cur.execute("update %s set tid = ? where tid = ?" % table,
                                (new_tid, old_tid))
            dnf_hist._commit()

    def migrate_groups(self):
        yum_exec = "/usr/bin/yum-deprecated"
        if not os.path.exists(yum_exec):
            yum_exec = "/usr/bin/yum"
        logger.info(_("Migrating groups data..."))

        installed = self.get_yum_installed_groups(yum_exec)
        if not installed:
            logger.info(_("No groups to migrate from Yum"))
            return

        # mark installed groups in dnf
        group_cmd = dnf.cli.commands.group.GroupCommand(self.cli)
        group_cmd._grp_setup()
        group_cmd._mark_install(installed)

    @staticmethod
    def get_yum_installed_groups(yum_exec):
        env_config = dict(os.environ, LANG="C", LC_ALL="C")
        output = dnf.i18n.ucd(check_output(
            [yum_exec, "-q", "group", "list", "installed", "-C"],
            env=env_config))
        return map(lambda l: l.lstrip(), output.splitlines())

    def migrate_yumdb(self):
        """Migrate YUMDB data."""
        attribute2mandatory = {
            "changed_by": False, "checksum_data": True, "checksum_type": True,
            "command_line": False, "from_repo": True,
            "from_repo_revision": False, "from_repo_timestamp": False,
            "installed_by": False, "reason": True, "releasever": True}
        migrated = skipped = 0
        logger.info(_("Migrating YUMDB data..."))
        try:
            with contextlib.closing(_YumBase()) as yumbase:
                for pkgtup, pkgid in yumbase.iter_yumdb(logger.warning):
                    nevra = "{0[0]}-{0[3]}-{0[4]}.{0[1]}".format(pkgtup)
                    dnfdata = self.base.yumdb.get_package(
                        pkgtup=pkgtup, pkgid=pkgid)
                    if next(iter(dnfdata), None) is not None:
                        logger.warning("%s found in DNFDB; skipping", nevra)
                        skipped += 1
                        continue

                    yumdata = yumbase.rpmdb.yumdb.get_package(
                        pkgtup=pkgtup, pkgid=pkgid)
                    for attribute, mandat in attribute2mandatory.items():
                        try:
                            value = getattr(yumdata, attribute)
                            setattr(dnfdata, attribute, value)
                        except OSError:
                            msg = _("YUMDB access denied")
                            raise dnf.exceptions.Error(msg)
                        except AttributeError:
                            lvl = logging.WARNING if mandat else logging.DEBUG
                            msg = _("%s of %s not found")
                            logger.log(lvl, msg, attribute, nevra)
                        else:
                            msg = _("%s of %s migrated")
                            logger.debug(msg, attribute, nevra)
                    migrated += 1
        finally:
            logger.info(
                _("%d YUMDB records found, %d migrated, %d skipped/preserved"),
                migrated + skipped, migrated, skipped)
