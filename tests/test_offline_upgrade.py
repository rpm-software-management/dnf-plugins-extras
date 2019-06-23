# test_offline_upgrade.py - unit tests for offline-upgrade plugin

# No gettext checking here
# pylint: disable=W9903
# Because of hypothesis limits possibilities
# pylint: disable=no-self-argument,no-value-for-parameter

from __future__ import absolute_import
from __future__ import unicode_literals

import argparse
import collections
import gettext
import io
import logging
import os
import shutil
import sys
import tempfile
import unittest
import uuid

import dnf
from dnf.callback import (PKG_CLEANUP, PKG_DOWNGRADE, PKG_INSTALL,
                          PKG_OBSOLETE, PKG_REINSTALL, PKG_REMOVE, PKG_UPGRADE,
                          PKG_VERIFY, TRANS_POST)

import hypothesis as ht
import hypothesis.strategies as st

from systemd.journal import _convert_realtime

from dnfpluginsextras import logger

import offline_upgrade
from offline_upgrade import CliError, PLYMOUTH
from tests import support
from tests.support import mock

patch = mock.patch


def draw_distro_sync(draw):
    return draw(st.one_of(st.none(), st.booleans()))


def draw_versioning(draw):
    return draw(st.one_of(st.none(), st.just('aaa'), st.just('bbb')))


def draw_repos_ed(draw):
    return draw(st.one_of(st.none(),
                          st.just(False),
                          st.just([]),
                          st.just([['*', 'disable'], ['test', 'enable']])))


def draw_exclude(draw):
    return draw(st.one_of(st.none(),
                          st.just([]),
                          st.lists(st.text(alphabet="L", min_size=4, max_size=8),
                                   min_size=1, max_size=10, unique=True)))


def draw_upgrade_status(draw):
    return draw(st.one_of(st.none(),
                          st.just('ready'),
                          st.just('incomplete'),
                          st.just('complete'),
                          st.text()))


class MockJournalReader:
    def add_match(self, *args, **kwargs):
        pass

    def __iter__(self):
        return iter([
            {
                'MESSAGE_ID': offline_upgrade.ID_TO_IDENTIFY_BOOTS.hex,
                '_BOOT_ID': uuid.UUID('12345678901234567890123456789012'),
                '_UID': 0,
                '__REALTIME_TIMESTAMP': _convert_realtime(1553439109893999),
            },
            {
                'MESSAGE_ID': offline_upgrade.ID_TO_IDENTIFY_BOOTS.hex,
                '_BOOT_ID': uuid.UUID('12345678901234567890123456789012'),
                '_UID': 0,
                '__REALTIME_TIMESTAMP': _convert_realtime(1553439209893999),
            },
            {
                'MESSAGE_ID': uuid.UUID('12345678901234567890123456789011'),
                '_BOOT_ID': uuid.UUID('12345678901234567890123456789012'),
                '_UID': 0,
                '__REALTIME_TIMESTAMP': _convert_realtime(1553439209893999),
            },
            {
                'MESSAGE_ID': offline_upgrade.ID_TO_IDENTIFY_BOOTS.hex,
                '_BOOT_ID': uuid.UUID('12345678901234567890123456789013'),
                '_UID': 0,
                '__REALTIME_TIMESTAMP': _convert_realtime(1553439309893999),
            },
        ])


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
            msg = self.display._fmt_event(self.pkg, action, 1, 1000)  # noqa: SF01
            # updating plymouth display means two plymouth calls
            call.assert_has_calls([
                mock.call((PLYMOUTH, "system-update", "--progress", "0")),
                mock.call((PLYMOUTH, "display-message", "--text", msg)),
            ], any_order=True)

    def test_filter_calls(self, call):
        action = PKG_INSTALL
        # first display update -> set percentage and text
        self.display.progress(self.pkg, action, 0, 100, 1, 1000)
        msg1 = self.display._fmt_event(self.pkg, action, 1, 1000)  # noqa: SF01
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
        msg2 = self.display._fmt_event(self.pkg, action, 2, 1000)  # noqa: SF01
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
        cls.msgdir = os.path.join(cls.localedir, TESTLANG, "LC_MESSAGES")
        cls.msgfile = "dnf-plugins-extras" + ".mo"
        os.makedirs(cls.msgdir)
        shutil.copy2(TESTLANG_MO, os.path.join(cls.msgdir, cls.msgfile))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.localedir)

    def setUp(self):
        self.t = gettext.translation("dnf-plugins-extras", self.localedir,
                                     languages=[TESTLANG], fallback=True)
        self.gettext = self.t.gettext


class I18NTestCase(I18NTestCaseBase):
    @unittest.skip("There is no translation yet to offline-upgrade")
    def test_selftest(self):
        self.assertIn(self.msgfile, os.listdir(self.msgdir))
        self.assertIn(TESTLANG, os.listdir(self.localedir))
        t = gettext.translation("dnf-plugins-extras", self.localedir,
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

    def setUp(self):
        self.StateClass = offline_upgrade.State
        self.state = None
        self.statedir = tempfile.mkdtemp(prefix="state.test.")
        self.statefile = os.path.join(self.statedir, "state.json")
        self.old_statefile = offline_upgrade.State.statefile
        offline_upgrade.State.statefile = self.statefile

    def tearDown(self):
        shutil.rmtree(self.statedir)
        offline_upgrade.State.statefile = self.old_statefile

    def test_bool_value(self):
        self.state = self.StateClass()
        self.assertIsNone(self.state.distro_sync)
        with self.state:
            self.state.distro_sync = True
        del self.state
        self.state = self.StateClass()
        self.assertTrue(self.state.distro_sync)

    @patch('offline_upgrade.json.load')
    def test_io_error(self, json_load_mock):
        json_load_mock.side_effect = IOError('load')
        self.state = self.StateClass()
        with self.state:
            self.state.distro_sync = True
        del self.state
        self.state = self.StateClass()
        self.assertIsNone(self.state.distro_sync)

    def test_corrupted_file_value_error(self):
        with open(self.statefile, 'w') as outf:
            outf.write("}")
        self.state = self.StateClass()
        self.assertIsNone(self.state.distro_sync)

    def test_corrupted_file_int(self):
        with open(self.statefile, 'w') as outf:
            outf.write("1")
        self.state = self.StateClass()
        self.assertIsNone(self.state.distro_sync)

    def test_file_with_known_value(self):
        with open(self.statefile, 'w') as outf:
            outf.write('{"distro_sync":true}')
        self.state = self.StateClass()
        self.assertTrue(self.state.distro_sync)

    def test_clear(self):
        self.state = self.StateClass()
        with self.state:
            self.state.distro_sync = True
        self.state.clear()
        self.assertIs(os.path.isfile(self.statefile), False)

    def test_clear_asdir(self):
        self.state = self.StateClass()
        with self.state:
            self.state.distro_sync = True
        os.unlink(self.statefile)
        os.makedirs(self.statefile)
        with self.assertRaises(SystemExit):
            self.state.clear()

    def test_ctx_raise(self):
        self.state = self.StateClass()
        with self.assertRaises(SystemExit):
            with self.state:
                sys.exit()

    def test_exit(self):
        self.state = self.StateClass()
        with self.state:
            self.state.distro_sync = True
        self.assertTrue(os.path.isfile(self.statefile))
        del self.state
        self.state = self.StateClass()
        self.assertTrue(self.state.distro_sync)

    def test_exit_asdir(self):
        self.state = self.StateClass()
        with self.state:
            self.state.distro_sync = True
        os.unlink(self.statefile)
        os.makedirs(self.statefile)
        with self.assertRaises(SystemExit):
            with self.state:
                self.state.distro_sync = False


class CommandTestCaseBase(unittest.TestCase):
    # By default:
    # - statefile is missing
    # - cachedir exists
    # - MAGIC_SYMLINK is defined, but does not point anywhere
    def setUp(self):
        # mock statefile
        self.statedir = tempfile.mkdtemp(prefix="command.test.statedir.")
        self.statefile = os.path.join(self.statedir, "state.json")
        self.old_statefile = offline_upgrade.State.statefile
        offline_upgrade.State.statefile = self.statefile

        # mock command /w cli and opts
        self.cli = mock.MagicMock()
        self.command = offline_upgrade.OfflineUpgradeCommand(cli=self.cli)
        self.command.opts = mock.MagicMock()

        # setup cachedir
        self.command.base.conf.cachedir = os.path.join(self.statedir, "cache")
        os.makedirs(self.command.base.conf.cachedir)

        # setup other common
        self.TTY_NAME = os.path.join(self.statedir, "tty")
        self.MAGIC_SYMLINK = os.path.join(self.statedir, "symlink")

    def _state(self, kwargs):
        with self.command.state as state:
            for k in kwargs:
                self.default_state[k] = kwargs[k]
                setattr(state, k, kwargs[k])

    def tearDown(self):
        shutil.rmtree(self.statedir)
        offline_upgrade.State.statefile = self.old_statefile


class CommandTestCase(CommandTestCaseBase):
    # self-tests for the command test cases
    def test_state(self):
        # initial state: no status
        self.assertIsNone(self.command.state.download_status)
        self.assertIsNone(self.command.state.upgrade_status)

    def test_print_help(self):
        # pylint: disable=protected-access
        # From dnf/cli/option_parser.py
        prog = "%s %s" % (
            dnf.const.PROGRAM_NAME,
            self.command._basecmd,  # noqa: SF01
        )

        cp = dnf.cli.option_parser.OptionParser()
        sup = super(dnf.cli.option_parser.OptionParser, cp)
        sup.__init__(prog, add_help=False, parents=[], description=self.command.summary)

        cp.command_arg_parser = argparse.ArgumentParser(prog, add_help=False)
        cp.command_arg_parser.print_usage = mock.MagicMock()
        self.command.set_argparser(cp)
        cp._actions += cp.command_arg_parser._actions  # noqa: SF01

        with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
            sup.print_help()

        self.assertIn("usage: dnf offline-upgrade", mock_stdout.getvalue())
        self.assertIn("[download|reboot|upgrade|log]", mock_stdout.getvalue())
        self.assertIn("Prepare system for upgrade", mock_stdout.getvalue())


class DownloadCommandTestCase(CommandTestCaseBase):
    # This is mostly integration testing
    #
    # Only public command api calls are tested, marked as api_*
    #
    # When reboot command is meant to run, there is following:
    # - command is: download
    # - opt distro_sync is True
    def setUp(self):
        super(DownloadCommandTestCase, self).setUp()
        self.cli.demands.allow_erasing = True
        self.command.opts.tid = ["download"]
        self.command.opts.distro_sync = None
        self.command.opts.repos_ed = None
        self.command.base.conf.best = True
        self.command.base.conf.exclude = []
        self.command.base.conf.gpgcheck = False
        self.command.base.conf.install_weak_deps = True
        self.command.base.conf.module_platform_id = ''
        self.command.base.conf.tsflags = []

        class Package():  # pylint: disable=too-few-public-methods
            def __init__(self, name, repo):
                self.name = name
                self.repo = repo

            def __str__(self):
                return self.name

        repo = collections.namedtuple('Repo', ['id'])
        repo.id = "test"
        pkg = Package("kernel", repo)
        self.cli.base.transaction.install_set = [pkg]

    def _args(self, kwargs):
        for k in kwargs:
            setattr(self.command.opts, k, kwargs[k])

    @st.composite
    def _gen_args(draw):  # noqa: N805
        return {
            'distro_sync': draw_distro_sync(draw),
            'repos_ed': draw_repos_ed(draw),
            'versioning': draw_versioning(draw),
        }

    #
    def api_pre_configure(self, kwargs):
        self._args(kwargs)
        self.command.pre_configure()

    def api_configure(self, kwargs):
        self._args(kwargs)
        self.command.configure()
        # This is kind of pointless
        self.assertTrue(self.cli.demands.root_user)
        self.assertTrue(self.cli.demands.resolving)
        self.assertTrue(self.cli.demands.available_repos)
        self.assertTrue(self.cli.demands.sack_activation)
        self.assertIn("test", self.command.base.conf.tsflags)

    def api_run(self, kwargs):
        self._args(kwargs)
        self.command.run()
        self.assertEqual(self.command.state.download_status, 'downloading')

    def api_run_transaction(self, kwargs):
        self._args(kwargs)
        with patch('offline_upgrade.journal.send') as send_mock:
            self.command.run_transaction()
        self.assertEqual(self.command.state.download_status, 'complete')
        self.assertEqual(self.command.state.install_packages, {"test": ["kernel"]})
        self.assertEqual(send_mock.call_args[1]['MESSAGE_ID'], offline_upgrade.DOWNLOAD_FINISHED_ID)

    #
    @unittest.skip("Covered with test_all")
    @ht.given(kwargs=_gen_args())
    def test_pre_configure(self, kwargs):
        self.api_pre_configure(kwargs)

    @unittest.skip("Covered with test_all")
    @ht.given(kwargs=_gen_args())
    def test_configure(self, kwargs):
        self.api_configure(kwargs)

    @unittest.skip("Covered with test_all")
    @ht.given(kwargs=_gen_args())
    def test_run(self, kwargs):
        self.api_run(kwargs)

    @unittest.skip("Covered with test_all")
    @ht.given(kwargs=_gen_args())
    def test_run_transaction(self, kwargs):
        self.api_run_transaction(kwargs)

    @ht.given(kwargs=_gen_args())
    def test_all(self, kwargs):
        self.api_pre_configure(kwargs)
        self.api_configure(kwargs)
        self.api_run(kwargs)
        self.api_run_transaction(kwargs)


class RebootCommandTestCase(CommandTestCaseBase):
    # This is mostly integration testing
    #
    # Only public command api calls are tested, marked as api_*
    #
    # When reboot command is meant to run, there is following:
    # - command is: reboot
    # - by default state contains some meaninful values
    def setUp(self):
        super(RebootCommandTestCase, self).setUp()
        self.command.opts.tid = ["reboot"]
        with self.command.state as state:
            state.allow_erasing = False
            state.best = False
            state.distro_sync = True
            state.download_status = 'complete'
            state.repos_ed = []
            state.exclude = []
            state.gpgcheck = False
            # There really is something but go without for now
            state.install_packages = None
            state.install_weak_deps = False

    #
    def api_pre_configure(self):
        self.command.pre_configure()

    def api_configure(self, lexists=False):
        self.cli.demands.root_user = None
        with patch('offline_upgrade.os.path.lexists') as lexists_func:
            lexists_func.return_value = lexists
            self.command.configure()
        self.assertTrue(self.cli.demands.root_user)
        self.assertTrue(os.path.isdir(self.command.base.conf.cachedir))

    def api_run(self):
        self.cli.demands.root_user = True
        with patch('offline_upgrade.MAGIC_SYMLINK', self.MAGIC_SYMLINK) as symlink, \
                patch('offline_upgrade.Popen') as popen_mock, \
                patch('offline_upgrade.journal.send') as send_mock:
            popen_mock.return_value.returncode = 0
            self.command.run()

        self.assertTrue(self.cli.demands.root_user)
        self.assertTrue(os.path.isdir(self.command.base.conf.cachedir))

        self.assertEqual(self.command.state.upgrade_status, 'ready')
        self.assertEqual(os.readlink(symlink), self.command.base.conf.cachedir)
        self.assertEqual(send_mock.call_args[1]['MESSAGE_ID'], offline_upgrade.REBOOT_REQUESTED_ID)
        self.assertTrue(popen_mock.called_once)
        # This might be overkill
        self.assertTrue(popen_mock.called_once_with(mock.call(["systemctl", "reboot"])))

    def api_run_transaction(self):
        self.command.run_transaction()

    #
    @unittest.skip("Covered with test_all")
    def test_pre_configure(self):
        self.api_pre_configure()

    def test_pre_configure_ver(self):
        with self.command.state as state:
            state.versioning = "foo"
        with self.assertRaises(CliError):
            self.api_pre_configure()
        self.assertFalse(os.path.exists(self.statefile))

    #
    @unittest.skip("Covered with test_all")
    def test_configure(self):
        self.api_configure()

    def test_configure_wo_dir(self):
        self.command.base.conf.cachedir = os.path.join(self.statedir, "wo_dir")
        with self.assertRaises(CliError):
            self.api_configure()

    def test_configure_no_download_yet(self):
        with self.command.state as state:
            state.download_status = None
        with self.assertRaises(CliError):
            self.api_configure()

    def test_configure_link_exists(self):
        with self.assertRaises(CliError):
            self.api_configure(lexists=True)

    def test_configure_already_upgraded(self):
        with self.command.state as state:
            state.upgrade_status = 'complete'
        with self.assertRaises(CliError):
            self.api_configure()

    #
    @unittest.skip("Covered with test_all")
    def test_run(self):
        self.api_run()

    #
    @unittest.skip("Covered with test_all")
    def test_run_transaction(self):
        self.api_run_transaction()

    def test_all(self):
        self.api_pre_configure()
        self.api_configure()
        self.api_run()
        self.api_run_transaction()


class UpgradeCommandTestCase(CommandTestCaseBase):
    def setUp(self):
        super(UpgradeCommandTestCase, self).setUp()
        self.command.opts.tid = ["upgrade"]

    # This is needed because hypothesis does run setUp/tearDown only
    # once per test method
    def _init(self):
        self.default_state = {  # pylint: disable=attribute-defined-outside-init
            'allow_erasing': False,
            'best': False,
            'distro_sync': True,
            'download_status': None,
            'exclude': None,
            'gpgcheck': False,
            'install_packages': {"test": ["kernel"]},
            'install_weak_deps': False,
            'module_platform_id': '',
            'repos_ed': [],
            'upgrade_status': None,
            'versioning': "aaa",

        }
        if os.path.exists(self.statefile):
            os.unlink(self.statefile)
        with self.command.state as state:
            for k in self.default_state:
                setattr(state, k, self.default_state[k])
        self.cli.demands.allow_erasing = None
        self.command.opts.distro_sync = None
        self.command.opts.repos_ed = None
        self.command.base.conf.best = None
        self.command.base.conf.exclude = None
        self.command.base.conf.gpgcheck = None
        self.command.base.conf.install_weak_deps = None
        self.command.base.conf.module_platform_id = None
        self.command.base.conf.tsflags = None
        if os.path.lexists(self.MAGIC_SYMLINK):
            os.unlink(self.MAGIC_SYMLINK)
        os.symlink(self.command.base.conf.cachedir, self.MAGIC_SYMLINK)

    @st.composite
    def _gen_args(draw):  # noqa: N805
        return {
            'exclude': draw_exclude(draw),
            'repos_ed': draw_repos_ed(draw),
            'upgrade_status': draw_upgrade_status(draw),
            'versioning': draw_versioning(draw),
        }

    #
    def api_pre_configure(self, kwargs):
        self._state(kwargs)
        with patch('offline_upgrade.MAGIC_SYMLINK', self.MAGIC_SYMLINK), \
                patch('offline_upgrade.complete_version_str', return_value=kwargs['versioning']):
            if kwargs['versioning'] == 'aaa':
                self.command.pre_configure()
            else:
                kwargs['fail'] = True
                with self.assertRaises(CliError):
                    self.command.pre_configure()
        if self.command.opts.repos_ed or self.command.state.repos_ed:
            self.assertEqual(self.command.opts.repos_ed, self.command.state.repos_ed)

    def api_configure(self, kwargs):
        self._state(kwargs)

        with patch('offline_upgrade.MAGIC_SYMLINK', self.MAGIC_SYMLINK):
            if kwargs['upgrade_status'] == 'ready':
                self.command.configure()
            else:
                kwargs['fail'] = True
                with self.assertRaises(CliError):
                    self.command.configure()

        if 'fail' in kwargs:
            return

        # This is kind of pointless
        self.assertTrue(self.cli.demands.root_user)
        self.assertTrue(self.cli.demands.resolving)
        self.assertTrue(self.cli.demands.available_repos)
        self.assertTrue(self.cli.demands.sack_activation)
        self.assertTrue(self.cli.demands.cacheonly)
        self.assertTrue(self.command.base.conf.assumeyes)
        #
        self.assertEqual(self.default_state['distro_sync'], self.command.opts.distro_sync)
        self.assertEqual(self.default_state['allow_erasing'], self.cli.demands.allow_erasing)
        self.assertEqual(self.default_state['gpgcheck'], self.command.base.conf.gpgcheck)
        self.assertEqual(self.default_state['best'], self.command.base.conf.best)
        self.assertIsNotNone(self.command.base.conf.exclude)
        self.assertEqual(self.command.state.exclude, self.command.base.conf.exclude)
        self.assertEqual(self.default_state['install_weak_deps'],
                         self.command.base.conf.install_weak_deps)
        self.assertEqual(self.default_state['module_platform_id'],
                         self.command.base.conf.module_platform_id)
        self.assertIsInstance(self.cli.demands.transaction_display,
                              offline_upgrade.PlymouthTransactionProgress)
        self.assertFalse(os.path.lexists(self.MAGIC_SYMLINK))

    def api_run(self, kwargs, install_side_effect=None):
        self._state(kwargs)
        with patch('offline_upgrade.MAGIC_SYMLINK', self.MAGIC_SYMLINK), \
                patch('offline_upgrade.journal.send') as send_mock, \
                patch('offline_upgrade.call', return_value=0):  # as call_mock:
            self.command.base.install.side_effect = install_side_effect
            self.command.run()

        if 'fail' in kwargs:
            return

        self.assertEqual(self.command.state.upgrade_status, 'incomplete')
        self.assertEqual(send_mock.call_args[1]['MESSAGE_ID'], offline_upgrade.UPGRADE_STARTED_ID)
        # hypothesis has a bug where it does not have output after initial call
        # if call_mock.call_args_list:
        #    call_mock.assert_any_call((PLYMOUTH, "change-mode", "--updates"))

    def api_run_transaction(self, kwargs):
        self._state(kwargs)
        with patch('offline_upgrade.MAGIC_SYMLINK', self.MAGIC_SYMLINK), \
                patch('offline_upgrade.journal.send') as send_mock, \
                patch('offline_upgrade.Popen') as popen_mock, \
                patch('offline_upgrade.call', return_value=0):
            self.command.run_transaction()
        self.assertEqual(self.command.state.upgrade_status, 'complete')
        self.assertEqual(send_mock.call_args[1]['MESSAGE_ID'], offline_upgrade.UPGRADE_FINISHED_ID)
        self.assertTrue(popen_mock.called_once)
        # This might be overkill
        self.assertTrue(popen_mock.called_once_with(mock.call(["systemctl", "reboot"])))

    #
    @unittest.skip("Covered with test_all")
    @ht.given(kwargs=_gen_args())
    def test_pre_configure(self, kwargs):
        self._init()
        self.api_pre_configure(kwargs)

    @unittest.skip("Covered with test_all")
    @ht.given(kwargs=_gen_args())
    def test_configure(self, kwargs):
        self._init()
        self.api_configure(kwargs)

    @ht.given(kwargs=_gen_args())
    def test_configure_nolink(self, kwargs):
        self._init()
        os.unlink(self.MAGIC_SYMLINK)
        kwargs['fail'] = True
        with self.assertRaises(SystemExit):
            self.api_configure(kwargs)

    @ht.given(kwargs=_gen_args())
    def test_configure_badlink(self, kwargs):
        self._init()
        os.unlink(self.MAGIC_SYMLINK)
        os.symlink(self.statedir, self.MAGIC_SYMLINK)
        kwargs['fail'] = True
        with self.assertRaises(SystemExit):
            self.api_configure(kwargs)

    @unittest.skip("Covered with test_all")
    @ht.given(kwargs=_gen_args())
    def test_run(self, kwargs):
        self._init()
        self.api_run(kwargs)

    @ht.given(kwargs=_gen_args())
    def test_run_tty(self, kwargs):
        self._init()
        with patch('offline_upgrade.TTY_NAME', self.TTY_NAME):
            self.api_run(kwargs)

    @ht.given(kwargs=_gen_args())
    def test_run_install(self, kwargs):
        self._init()
        kwargs['fail'] = True
        with self.assertRaises(dnf.exceptions.MarkingError):
            self.api_run(kwargs, install_side_effect=dnf.exceptions.MarkingError())

    @unittest.skip("Covered with test_all")
    @ht.given(kwargs=_gen_args())
    def test_run_transaction(self, kwargs):
        self._init()
        self.api_run_transaction(kwargs)

    @ht.given(kwargs=_gen_args())
    def test_all(self, kwargs):
        self._init()
        self.api_pre_configure(kwargs)
        self.api_configure(kwargs)
        self.api_run(kwargs)
        self.api_run_transaction(kwargs)


class LogCommandTestCase(CommandTestCaseBase):
    def setUp(self):
        super(LogCommandTestCase, self).setUp()
        self.command.opts.tid = ["log"]

    def test_configure(self):
        self.command.configure()

    def test_run_log_list(self):
        self.command.opts.number = None
        with patch('offline_upgrade.list_logs') as list_logs:
            self.command.run_log()
        list_logs.assert_called_once_with()

    def test_run_log_prev(self):
        self.command.opts.number = -2
        with patch('offline_upgrade.show_log') as show_log:
            self.command.run_log()
        show_log.assert_called_once_with(-2)

    def test_find_boots(self):
        with patch('offline_upgrade.journal.Reader', side_effect=MockJournalReader):
            lst = list(offline_upgrade.find_boots(offline_upgrade.ID_TO_IDENTIFY_BOOTS))
            self.assertIs(len(lst), 2)

    def test_find_boots_empty(self):
        with patch('offline_upgrade.journal.Reader'):
            self.assertFalse(list(offline_upgrade.find_boots(offline_upgrade.ID_TO_IDENTIFY_BOOTS)))

    @unittest.skipUnless(support.PY3, "test_list_logs not compat with Py2")
    def test_list_logs(self):
        stdout_stream_h = logging.StreamHandler(sys.stdout)
        logger.addHandler(stdout_stream_h)
        try:
            with patch('offline_upgrade.journal.Reader', side_effect=MockJournalReader), \
                    patch('sys.stdout', new=io.StringIO()) as mock_stdout, \
                    self.assertLogs(logger) as log:
                offline_upgrade.list_logs()

                if not log.output:
                    logger.info("no log output")
                else:
                    self.assertFalse("Unexpected log")  # pylint: disable=redundant-unittest-assert

            def haslines():
                for line in log.output, mock_stdout.getvalue():
                    if "12345678901234567890123456789" in line:
                        return True
                return False
            self.assertTrue(haslines())
        finally:
            logger.removeHandler(stdout_stream_h)

    def test_list_logs_empty(self):  # pylint: disable=no-self-use
        with patch('offline_upgrade.journal.Reader'):
            offline_upgrade.list_logs()

    def test_pick_boot(self):
        with patch('offline_upgrade.journal.Reader', side_effect=MockJournalReader):
            rv = offline_upgrade.pick_boot(offline_upgrade.ID_TO_IDENTIFY_BOOTS, 1)
            self.assertEqual(rv, uuid.UUID('12345678-9012-3456-7890-123456789012'))

    def test_pick_boot_0(self):
        with patch('offline_upgrade.journal.Reader', side_effect=MockJournalReader), \
                self.assertRaises(dnf.cli.CliError):
            offline_upgrade.pick_boot(offline_upgrade.ID_TO_IDENTIFY_BOOTS, 0)

    def test_pick_boot_3(self):
        with patch('offline_upgrade.journal.Reader', side_effect=MockJournalReader), \
                self.assertRaises(dnf.cli.CliError):
            offline_upgrade.pick_boot(offline_upgrade.ID_TO_IDENTIFY_BOOTS, 0)

    def test_pick_boot_m1(self):
        with patch('offline_upgrade.journal.Reader', side_effect=MockJournalReader):
            rv = offline_upgrade.pick_boot(offline_upgrade.ID_TO_IDENTIFY_BOOTS, -1)
            self.assertEqual(rv, uuid.UUID('12345678-9012-3456-7890-123456789013'))

    def test_show_log(self):  # pylint: disable=no-self-use
        with patch('offline_upgrade.journal.Reader', side_effect=MockJournalReader), \
                patch('offline_upgrade.Popen') as popen:
            popen.return_value.returncode = 0
            popen.return_value.communicate.return_value = ('line1',)
            offline_upgrade.show_log(-1)

    def test_show_log_error(self):
        with patch('offline_upgrade.journal.Reader', side_effect=MockJournalReader), \
                patch('offline_upgrade.Popen') as popen, \
                self.assertRaises(dnf.exceptions.Error):
            popen.return_value.returncode = 1
            offline_upgrade.show_log(1)


class PluginTestCase(unittest.TestCase):
    def test_plugin(self):  # pylint: disable=no-self-use
        base = mock.MagicMock()
        cli = mock.Mock(return_value=True)

        offline_upgrade.OfflineUpgradePlugin(base, cli)
        cli.register_command.assert_called_once_with(offline_upgrade.OfflineUpgradeCommand)

    def test_plugin_nocli(self):  # pylint: disable=no-self-use
        base = mock.MagicMock()
        cli = mock.MagicMock()
        if support.PY3:
            cli.__bool__.return_value = False
        else:
            cli.__nonzero__.return_value = False

        offline_upgrade.OfflineUpgradePlugin(base, cli)
        cli.register_command.assert_not_called()

    def test_complete_version_str(self):
        with patch('offline_upgrade.DNFVERSION', '1'), \
                patch('offline_upgrade.OFFLINE_UPGRADE_PLUGIN_VERSION', '2'):
            rv = offline_upgrade.complete_version_str()
            self.assertEqual(rv, '1 2')

    def test_complete_version_str_2(self):
        rv = offline_upgrade.complete_version_str()
        self.assertNotEqual(rv, ' ')
