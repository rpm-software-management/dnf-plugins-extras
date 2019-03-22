# test_offline_upgrade.py - unit tests for offline-upgrade plugin

import offline_upgrade

from offline_upgrade import PLYMOUTH, CliError

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


@patch('offline_upgrade.call', return_value=0)
class PlymouthTestCase(unittest.TestCase):
    def setUp(self):
        self.ply = offline_upgrade.PlymouthOutput()
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


@patch('offline_upgrade.call', return_value=0)
class PlymouthTransactionProgressTestCase(unittest.TestCase):
    actions = (PKG_CLEANUP, PKG_DOWNGRADE, PKG_INSTALL, PKG_OBSOLETE,
               PKG_REINSTALL, PKG_REMOVE, PKG_UPGRADE, PKG_VERIFY,
               TRANS_POST)

    # pylint: disable=protected-access
    def setUp(self):
        offline_upgrade.Plymouth = offline_upgrade.PlymouthOutput()
        self.display = offline_upgrade.PlymouthTransactionProgress()
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
# @unittest.skip("There is no translation yet to offline-upgrade")
class I18NTestCaseBase(unittest.TestCase):
    @classmethod
    @unittest.skip("There is no translation yet to offline-upgrade")
    def setUpClass(cls):
        cls.localedir = tempfile.mkdtemp(prefix='i18ntest')
        cls.msgdir = os.path.join(cls.localedir, TESTLANG + "/LC_MESSAGES")
        cls.msgfile = offline_upgrade.TEXTDOMAIN + ".mo"
        os.makedirs(cls.msgdir)
        shutil.copy2(TESTLANG_MO, os.path.join(cls.msgdir, cls.msgfile))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.localedir)

    def setUp(self):
        self.t = gettext.translation(offline_upgrade.TEXTDOMAIN, self.localedir,
                                     languages=[TESTLANG], fallback=True)
        self.gettext = self.t.gettext


class I18NTestCase(I18NTestCaseBase):
    @unittest.skip("There is no translation yet to offline-upgrade")
    def test_selftest(self):
        self.assertIn(self.msgfile, os.listdir(self.msgdir))
        self.assertIn(TESTLANG, os.listdir(self.localedir))
        t = gettext.translation(offline_upgrade.TEXTDOMAIN, self.localedir,
                                languages=[TESTLANG], fallback=False)
        info = t.info()
        self.assertIn("language", info)
        self.assertEqual(info["language"], TESTLANG.replace("_", "-"))

    @unittest.skip("There is no translation yet to offline-upgrade")
    def test_fallback(self):
        msg = "THIS STRING DOES NOT EXIST"
        trans_msg = self.gettext(msg)
        self.assertEqual(msg, trans_msg)

    @unittest.skip("There is no translation yet to offline-upgrade")
    def test_translation(self):
        msg = "the color of the sky"
        trans_msg = self.gettext(msg)
        self.assertNotEqual(msg, trans_msg)


class StateTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.statedir = tempfile.mkdtemp(prefix="state.test.")
        cls.StateClass = offline_upgrade.State
        cls.StateClass.statefile = os.path.join(cls.statedir, "state")

    def setUp(self):
        self.state = self.StateClass()

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

    def tearDown(self):
        shutil.rmtree(self.tmpdir)


class CommandTestCaseBase(unittest.TestCase):
    def setUp(self):
        self.statedir = tempfile.mkdtemp(prefix="command.test.statedir.")
        self.statefile = os.path.join(self.statedir, "state")
        self.old_statefile = offline_upgrade.State.statefile
        offline_upgrade.State.statefile = self.statefile
        self.cli = mock.MagicMock()
        self.command = offline_upgrade.OfflineUpgradeCommand(cli=self.cli)
        self.command.base.conf.cachedir = os.path.join(self.statedir, "cache")
        self.command.base.conf.destdir = None

    def tearDown(self):
        shutil.rmtree(self.statedir)
        offline_upgrade.State.statefile = self.old_statefile


class CommandTestCase(CommandTestCaseBase):
    # self-tests for the command test cases
    def test_state(self):
        # initial state: no status
        self.assertEqual(self.command.state.download_status, None)
        self.assertEqual(self.command.state.upgrade_status, None)


class RebootCheckCommandTestCase(CommandTestCaseBase):
    def setUp(self):
        super(RebootCheckCommandTestCase, self).setUp()
        self.MAGIC_SYMLINK = self.statedir + '/symlink'

    def test_pre_configure_reboot(self):
        with self.command.state as state:
            state.destdir = "/grape/wine"
        self.command.pre_configure_reboot()
        self.assertEqual(self.command.base.conf.destdir, "/grape/wine")

    def test_configure_reboot(self):
        self.cli.demands.root_user = None
        self.command.configure_reboot()
        self.assertTrue(self.cli.demands.root_user)

    def check_reboot(self, status='complete', lexists=False, dnfverok=True):
        with patch('offline_upgrade.os.path.lexists') as lexists_func:
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
        with patch('offline_upgrade.MAGIC_SYMLINK', self.MAGIC_SYMLINK):
            self.command.run_prepare()
        self.assertEqual(os.readlink(self.MAGIC_SYMLINK), self.command.base.conf.cachedir)
        self.assertEqual(self.command.state.upgrade_status, 'ready')

    @patch('offline_upgrade.OfflineUpgradeCommand.run_prepare')
    @patch('offline_upgrade.OfflineUpgradeCommand.log_status')
    @patch('offline_upgrade.reboot')
    def test_run_reboot(self, reboot, log_status, run_prepare):
        self.command.opts = mock.MagicMock()
        self.command.opts.tid = ["reboot"]
        self.command.run_reboot()
        run_prepare.assert_called_once_with()
        self.assertEqual(offline_upgrade.REBOOT_REQUESTED_ID,
                         log_status.call_args[0][1])
        self.assertTrue(reboot.called)

    @patch('offline_upgrade.OfflineUpgradeCommand.run_prepare')
    @patch('offline_upgrade.OfflineUpgradeCommand.log_status')
    @patch('offline_upgrade.reboot')
    def test_reboot_prepare_only(self, reboot, log_status, run_prepare):
        self.command.opts = mock.MagicMock()
        self.command.opts.tid = [None]
        self.command.run_reboot()
        run_prepare.assert_called_once_with()
        self.assertFalse(log_status.called)
        self.assertFalse(reboot.called)


class DownloadCommandTestCase(CommandTestCase):
    def test_pre_configure_download_default(self):
        self.command.opts = mock.MagicMock()
        self.command.pre_configure_download()

    def test_pre_configure_download_destdir(self):
        self.command.opts = mock.MagicMock()
        self.command.opts.destdir = "/grape/wine"
        self.command.pre_configure_download()
        self.assertEqual(self.command.base.conf.destdir, "/grape/wine")

    def test_configure_download(self):
        self.command.opts = mock.MagicMock()
        self.command.opts.tid = "download"
        self.command.configure()
        self.assertTrue(self.cli.demands.root_user)
        self.assertTrue(self.cli.demands.resolving)
        self.assertTrue(self.cli.demands.sack_activation)
        self.assertTrue(self.cli.demands.available_repos)

    def test_transaction_download(self):
        pkg = mock.MagicMock()
        repo = mock.MagicMock()
        repo.id = 'test'
        pkg.name = "kernel"
        pkg.repo = repo
        self.cli.base.transaction.install_set = [pkg]
        self.command.opts = mock.MagicMock()
        self.command.opts.distro_sync = "distro_sync"
        self.command.opts.repos_ed = []
        self.cli.demands.allow_erasing = "allow_erasing"
        self.command.base.conf.best = "best"
        self.command.base.conf.installroot = "/"
        self.command.base.conf.gpgcheck = True
        self.command.base.conf.destdir = "/grape/wine"
        self.command.base.conf.install_weak_deps = True
        self.command.base.conf.module_platform_id = ''
        self.command.transaction_download()
        with offline_upgrade.State() as state:
            self.assertEqual(state.download_status, "complete")
            self.assertEqual(state.distro_sync, "distro_sync")
            self.assertEqual(state.allow_erasing, "allow_erasing")
            self.assertEqual(state.best, "best")
            self.assertEqual(state.destdir, "/grape/wine")


class UpgradeCommandTestCase(CommandTestCase):
    def test_pre_configure_upgrade(self):
        with self.command.state as state:
            state.destdir = "/grape/wine"
        self.command.pre_configure_upgrade()
        self.assertEqual(self.command.base.conf.destdir, "/grape/wine")

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
        self.command.opts = mock.MagicMock()
        self.command.opts.number = None
        with patch('offline_upgrade.list_logs') as list_logs:
            self.command.run_log()
        list_logs.assert_called_once_with()

    def test_run_log_prev(self):
        with patch('offline_upgrade.show_log') as show_log:
            self.command.opts = mock.MagicMock()
            self.command.opts.number = -2
            self.command.run_log()
        show_log.assert_called_once_with(-2)
