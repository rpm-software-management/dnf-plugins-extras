# test_system_upgrade.py - unit tests for system-upgrade plugin

import system_upgrade

from system_upgrade import PLYMOUTH, CliError

import os
import tempfile
import shutil
import gettext

from dnf.callback import (PKG_CLEANUP, PKG_DOWNGRADE, PKG_INSTALL,
                          PKG_OBSOLETE, PKG_REINSTALL, PKG_REMOVE, PKG_UPGRADE,
                          PKG_VERIFY, TRANS_POST)

import unittest
try:
    from unittest import mock
except ImportError:
    import mock
patch = mock.patch


@patch('system_upgrade.call', return_value=0)
class PlymouthTestCase(unittest.TestCase):
    def setUp(self):
        self.ply = system_upgrade.PlymouthOutput()
        self.msg = "Hello, plymouth."
        self.msg_args = (PLYMOUTH, "display-message", "--text", self.msg)

    def test_ping(self, call):
        self.ply.ping()
        call.assert_called_once_with((PLYMOUTH, "--ping"))
        self.assertTrue(self.ply.alive)

    def test_ping_when_dead(self, call):
        call.return_value = 1
        self.ply.ping()
        self.assertFalse(self.ply.alive)
        call.return_value = 0
        self.ply.ping()
        self.assertEqual(call.call_count, 2)
        self.assertTrue(self.ply.alive)

    def test_mode_no_plymouth(self, call):
        call.side_effect = OSError(2, 'No such file or directory')
        self.ply.set_mode("updates")
        self.assertFalse(self.ply.alive)

    def test_message(self, call):
        self.ply.message(self.msg)
        call.assert_called_once_with(self.msg_args)

    def test_hide_message(self, call):
        messages = ("first", "middle", "BONUS", "last")
        for m in messages:
            self.ply.message(m)

        def hidem(m):
            return mock.call((PLYMOUTH, "hide-message", "--text", m))

        def dispm(m):
            return mock.call((PLYMOUTH, "display-message", "--text", m))
        m1, m2, m3, m4 = messages
        call.assert_has_calls([
            dispm(m1),
            hidem(m1), dispm(m2),
            hidem(m2), dispm(m3),
            hidem(m3), dispm(m4),
        ])

    def test_message_dupe(self, call):
        self.ply.message(self.msg)
        self.ply.message(self.msg)
        call.assert_called_once_with(self.msg_args)

    def test_message_dead(self, call):
        call.return_value = 1
        self.ply.message(self.msg)
        self.assertFalse(self.ply.alive)
        self.ply.message("not even gonna bother")
        call.assert_called_once_with(self.msg_args)

    def test_progress(self, call):
        self.ply.progress(27)
        call.assert_called_once_with(
            (PLYMOUTH, "system-update", "--progress", str(27)))

    def test_mode(self, call):
        self.ply.set_mode("updates")
        call.assert_called_once_with((PLYMOUTH, "change-mode", "--updates"))


@patch('system_upgrade.call', return_value=0)
class PlymouthTransactionProgressTestCase(unittest.TestCase):
    actions = (PKG_CLEANUP, PKG_DOWNGRADE, PKG_INSTALL, PKG_OBSOLETE,
               PKG_REINSTALL, PKG_REMOVE, PKG_UPGRADE, PKG_VERIFY,
               TRANS_POST)

    # pylint: disable=protected-access
    def setUp(self):
        system_upgrade.Plymouth = system_upgrade.PlymouthOutput()
        self.display = system_upgrade.PlymouthTransactionProgress()
        self.pkg = "testpackage"

    def test_display(self, call):
        for action in self.actions:
            self.display.progress(self.pkg, action, 0, 100, 1, 1000)
            msg = self.display._fmt_event(self.pkg, action, 1, 1000)
            # updating plymouth display means two plymouth calls
            call.assert_has_calls([
                mock.call((PLYMOUTH, "system-update", "--progress", "0")),
                mock.call((PLYMOUTH, "display-message", "--text", msg))
            ], any_order=True)

    def test_filter_calls(self, call):
        action = PKG_INSTALL
        # first display update -> set percentage and text
        self.display.progress(self.pkg, action, 0, 100, 1, 1000)
        msg1 = self.display._fmt_event(self.pkg, action, 1, 1000)
        call.assert_has_calls([
            mock.call((PLYMOUTH, "system-update", "--progress", "0")),
            mock.call((PLYMOUTH, "display-message", "--text", msg1)),
        ])

        # event progress on the same transaction item.
        # no new calls to plymouth because the percentage and text don't change
        for te_cur in range(1, 100):
            self.display.progress(self.pkg, action, te_cur, 100, 1, 1000)
        call.assert_has_calls([
            mock.call((PLYMOUTH, "system-update", "--progress", "0")),
            mock.call((PLYMOUTH, "display-message", "--text", msg1)),
        ])

        # new item: new message ("[2/1000] ..."), but percentage still 0..
        self.display.progress(self.pkg, action, 0, 100, 2, 1000)
        # old message hidden, new message displayed. no new percentage.
        msg2 = self.display._fmt_event(self.pkg, action, 2, 1000)
        call.assert_has_calls([
            mock.call((PLYMOUTH, "system-update", "--progress", "0")),
            mock.call((PLYMOUTH, "display-message", "--text", msg1)),
            mock.call((PLYMOUTH, "hide-message", "--text", msg1)),
            mock.call((PLYMOUTH, "display-message", "--text", msg2)),
        ])

TESTLANG = "zh_CN"
TESTLANG_MO = "po/%s.mo" % TESTLANG


@unittest.skipUnless(os.path.exists(TESTLANG_MO), "make %s first" %
                     TESTLANG_MO)
# @unittest.skip("There is no translation yet to system-upgrade")
class I18NTestCaseBase(unittest.TestCase):
    @classmethod
    @unittest.skip("There is no translation yet to system-upgrade")
    def setUpClass(cls):
        cls.localedir = tempfile.mkdtemp(prefix='i18ntest')
        cls.msgdir = os.path.join(cls.localedir, TESTLANG+"/LC_MESSAGES")
        cls.msgfile = system_upgrade.TEXTDOMAIN + ".mo"
        os.makedirs(cls.msgdir)
        shutil.copy2(TESTLANG_MO, os.path.join(cls.msgdir, cls.msgfile))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.localedir)

    def setUp(self):
        self.t = gettext.translation(system_upgrade.TEXTDOMAIN, self.localedir,
                                     languages=[TESTLANG], fallback=True)
        self.gettext = self.t.gettext


class I18NTestCase(I18NTestCaseBase):
    @unittest.skip("There is no translation yet to system-upgrade")
    def test_selftest(self):
        self.assertIn(self.msgfile, os.listdir(self.msgdir))
        self.assertIn(TESTLANG, os.listdir(self.localedir))
        t = gettext.translation(system_upgrade.TEXTDOMAIN, self.localedir,
                                languages=[TESTLANG], fallback=False)
        info = t.info()
        self.assertIn("language", info)
        self.assertEqual(info["language"], TESTLANG.replace("_", "-"))

    @unittest.skip("There is no translation yet to system-upgrade")
    def test_fallback(self):
        msg = "THIS STRING DOES NOT EXIST"
        trans_msg = self.gettext(msg)
        self.assertEqual(msg, trans_msg)

    @unittest.skip("There is no translation yet to system-upgrade")
    def test_translation(self):
        msg = "the color of the sky"
        trans_msg = self.gettext(msg)
        self.assertNotEqual(msg, trans_msg)


class StateTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.statedir = tempfile.mkdtemp(prefix="state.test.")
        cls.StateClass = system_upgrade.State
        cls.StateClass.statefile = os.path.join(cls.statedir, "state")

    def setUp(self):
        self.state = self.StateClass()

    def test_set_write_get(self):
        path = "/some/stupid/path"
        with self.state:
            self.state.datadir = path
        del self.state
        self.state = self.StateClass()
        self.assertEqual(self.state.datadir, path)

    def test_clear(self):
        self.state.clear()
        del self.state
        self.state = self.StateClass()
        self.assertIs(self.state.datadir, None)

    def test_bool_value(self):
        with self.state:
            self.state.distro_sync = True
        del self.state
        self.state = self.StateClass()
        self.assertIs(self.state.distro_sync, True)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.statedir)


class UtilTestCase(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix='util.test.')
        self.dirs = ["dir1", "dir2"]
        self.files = ["file1", "dir2/file2"]
        for d in self.dirs:
            os.makedirs(os.path.join(self.tmpdir, d))
        for f in self.files:
            with open(os.path.join(self.tmpdir, f), 'wt') as fobj:
                fobj.write("hi there\n")

    def test_self_test(self):
        for d in self.dirs:
            self.assertTrue(os.path.isdir(os.path.join(self.tmpdir, d)))
        for f in self.files:
            self.assertTrue(os.path.exists(os.path.join(self.tmpdir, f)))

    def test_clear_dir(self):
        self.assertTrue(os.path.isdir(self.tmpdir))
        system_upgrade.clear_dir(self.tmpdir)
        self.assertTrue(os.path.isdir(self.tmpdir))
        self.assertEqual(os.listdir(self.tmpdir), [])

    def tearDown(self):
        shutil.rmtree(self.tmpdir)


class CommandTestCaseBase(unittest.TestCase):
    def setUp(self):
        self.statedir = tempfile.mkdtemp(prefix="command.test.statedir.")
        self.statefile = os.path.join(self.statedir, "state")
        self.old_statefile = system_upgrade.State.statefile
        system_upgrade.State.statefile = self.statefile
        self.cli = mock.MagicMock()
        self.command = system_upgrade.SystemUpgradeCommand(cli=self.cli)

    def tearDown(self):
        shutil.rmtree(self.statedir)
        system_upgrade.State.statefile = self.old_statefile


class CommandTestCase(CommandTestCaseBase):
    # self-tests for the command test cases
    def test_state(self):
        # initial state: no status
        self.assertEqual(self.command.state.download_status, None)
        self.assertEqual(self.command.state.upgrade_status, None)
        self.assertEqual(self.command.state.datadir, None)
        # check the context stuff works like we expect
        with self.command.state as state:
            state.datadir = os.path.join(self.statedir, "datadir")
            os.makedirs(state.datadir)
        self.assertTrue(os.path.isdir(self.command.state.datadir))


class CleanCommandTestCase(CommandTestCaseBase):
    def test_configure_clean(self):
        self.cli.demands.root_user = None
        self.command.configure_clean([])
        self.assertTrue(self.cli.demands.root_user)

    def test_run_clean(self):
        # set up a datadir and pretend like we're ready to upgrade
        datadir = os.path.join(self.statedir, "datadir")
        os.makedirs(datadir)
        fakerpm = os.path.join(datadir, "fake.rpm")
        with open(fakerpm, "w") as outf:
            outf.write("hi i am an rpm")
        with self.command.state as state:
            state.datadir = datadir
            state.download_status = "complete"
            state.upgrade_status = "ready"
        # make sure the datadir and state info is set up OK
        self.assertEqual(datadir, self.command.state.datadir)
        self.assertTrue(os.path.isdir(datadir))
        self.assertTrue(os.path.exists(fakerpm))
        self.assertEqual(self.command.state.download_status, "complete")
        self.assertEqual(self.command.state.upgrade_status, "ready")
        # run cleanup
        self.command.run_clean([])
        # datadir remains, but is empty, and state is cleared
        self.assertEqual(datadir, self.command.state.datadir)
        self.assertTrue(os.path.isdir(datadir))
        self.assertFalse(os.path.exists(fakerpm))
        self.assertEqual(self.command.state.download_status, None)
        self.assertEqual(self.command.state.upgrade_status, None)


class RebootCheckCommandTestCase(CommandTestCaseBase):
    def setUp(self):
        super(RebootCheckCommandTestCase, self).setUp()
        self.MAGIC_SYMLINK = self.statedir + '/symlink'
        self.SYSTEMD_FLAG_FILE = self.statedir + '/systemd.flag.file'

    def test_configure_reboot(self):
        self.cli.demands.root_user = None
        self.command.configure_reboot()
        self.assertTrue(self.cli.demands.root_user)

    def check_reboot(self, status='complete', lexists=False, dnfverok=True):
        with patch('system_upgrade.os.path.lexists') as lexists_func:
            self.command.state.download_status = status
            lexists_func.return_value = lexists
            self.command.check_reboot()

    def test_check_reboot_ok(self):
        self.check_reboot(status='complete', lexists=False, dnfverok=True)

    def test_check_reboot_no_download(self):
        with self.assertRaises(CliError):
            self.check_reboot(status=None, lexists=False, dnfverok=True)

    def test_check_reboot_link_exists(self):
        with self.assertRaises(CliError):
            self.check_reboot(status='complete', lexists=True, dnfverok=True)

    def test_run_prepare(self):
        self.command.state.datadir = '/lol/wut'
        with patch('system_upgrade.SYSTEMD_FLAG_FILE', self.SYSTEMD_FLAG_FILE):
            with patch('system_upgrade.MAGIC_SYMLINK', self.MAGIC_SYMLINK):
                self.command.run_prepare([])
        self.assertEqual(os.readlink(self.MAGIC_SYMLINK),
                         self.command.state.datadir)
        self.assertEqual(self.command.state.upgrade_status, 'ready')
        releasever = self.command.state.target_releasever
        with open(self.SYSTEMD_FLAG_FILE) as flag_file:
            self.assertIn('RELEASEVER=%s\n' % releasever, flag_file.read())

    @patch('system_upgrade.SystemUpgradeCommand.run_prepare')
    @patch('system_upgrade.SystemUpgradeCommand.log_status')
    @patch('system_upgrade.reboot')
    def test_run_reboot(self, reboot, log_status, run_prepare):
        self.command.opts = mock.MagicMock()
        self.command.opts.tid = ["reboot"]
        self.command.run_reboot([])
        run_prepare.assert_called_once_with([])
        self.assertEqual(system_upgrade.REBOOT_REQUESTED_ID,
                         log_status.call_args[0][1])
        self.assertTrue(reboot.called)

    @patch('system_upgrade.SystemUpgradeCommand.run_prepare')
    @patch('system_upgrade.SystemUpgradeCommand.log_status')
    @patch('system_upgrade.reboot')
    def test_reboot_prepare_only(self, reboot, log_status, run_prepare):
        self.command.opts = mock.MagicMock()
        self.command.opts.tid = [None]
        self.command.run_reboot([])
        run_prepare.assert_called_once_with([])
        self.assertFalse(log_status.called)
        self.assertFalse(reboot.called)


class DownloadCommandTestCase(CommandTestCase):
    def test_configure_download(self):
        self.command.opts = mock.MagicMock()
        self.command.opts.tid = "download"
        self.command.configure()
        self.assertTrue(self.cli.demands.root_user)
        self.assertTrue(self.cli.demands.resolving)
        self.assertTrue(self.cli.demands.sack_activation)
        self.assertTrue(self.cli.demands.available_repos)
        for repo in self.command.base.repos.values():
            self.assertEqual(repo.pkgdir, self.command.opts.datadir)

    def test_transaction_download(self):
        pkg = mock.MagicMock()
        pkg.name = "kernel"
        self.cli.base.transaction.install_set = [pkg]
        self.command.opts = mock.MagicMock()
        self.command.opts.distro_sync = "distro_sync"
        self.cli.demands.allow_erasing = "allow_erasing"
        self.command.base.conf.best = "best"
        self.command.base.conf.installroot = "/"
        self.command.base.conf.releasever = "35"
        self.command.transaction_download()
        with system_upgrade.State() as state:
            self.assertEqual(state.download_status, "complete")
            self.assertEqual(state.distro_sync, "distro_sync")
            self.assertEqual(state.allow_erasing, "allow_erasing")
            self.assertEqual(state.best, "best")

    def test_transaction_download_no_kernel(self):
        self.cli.base.transaction.install_set = []
        with self.assertRaises(CliError):
            self.command.transaction_download()


class UpgradeCommandTestCase(CommandTestCase):
    def test_configure_upgrade(self):
        # write state like download would have
        with self.command.state as state:
            state.download_status = "complete"
            state.distro_sync = True
            state.allow_erasing = True
            state.best = True
        # okay, now configure upgrade
        self.command.opts = mock.MagicMock()
        self.command.opts.tid = "upgrade"
        self.command.configure()
        # did we reset the depsolving flags?
        self.assertTrue(self.command.opts.distro_sync)
        self.assertTrue(self.cli.demands.allow_erasing)
        self.assertTrue(self.command.base.conf.best)
        # are we on autopilot?
        self.assertTrue(self.command.base.conf.assumeyes)
        self.assertTrue(self.cli.demands.cacheonly)


class LogCommandTestCase(CommandTestCase):
    def test_configure_log(self):
        self.command.opts = mock.MagicMock()
        self.command.opts.tid = "log"
        self.command.configure()

    def test_run_log_list(self):
        with patch('system_upgrade.list_logs') as list_logs:
            self.command.run_log(["log"])
        list_logs.assert_called_once_with()

    def test_run_log_prev(self):
        with patch('system_upgrade.show_log') as show_log:
            self.command.run_log(["log", "-2"])
        show_log.assert_called_once_with(-2)
