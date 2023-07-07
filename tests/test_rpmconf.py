# Copyright (C) 2016 Maxim Prokhorov
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

import errno
import os
from shutil import rmtree

import tempfile
import unittest
from unittest.util import safe_repr

from dnf.pycomp import StringIO

import tests.support
from tests.support import mock
from importlib.metadata import version
from packaging.version import parse

from itertools import zip_longest

import rpm_conf


def create_file(path, content):
    with open(path, 'wb') as f:
        f.write(content)
    return path, content

class FakeRpmfile(object):
    def __init__(self, conf_file, fflags):
        self.name = conf_file
        self.fflags = fflags

class RpmconfPluginStub(object):

    def __init__(self, pkgname, conf_file):
        self.packages = [pkgname]
        self._conf_file = conf_file
        self.diff = None
        self.frontend = None
        self._interactive = True
        self._patches = []

    def __enter__(self):
        self._patches = [
            mock.patch("rpm.TransactionSet.dbMatch", return_value=self.packages),
            mock.patch("rpm.fi", return_value=((self._conf_file, None, None, None, 1), ))
                if parse(version('rpmconf')) < parse('1.1.10') else
                    mock.patch("rpm.files", return_value=(FakeRpmfile(self._conf_file, 1), ))
        ]
        for patch in self._patches:
            patch.__enter__()

        return self

    def __exit__(self, *exc_info):
        for patch in self._patches:
            patch.__exit__(*exc_info)
        self._patches = None

    if rpm_conf:
        run = rpm_conf.Rpmconf.transaction


class TestRpmConf(unittest.TestCase):

    def setUp(self):
        self.pkgname = 'package'
        self.prefix = tempfile.mkdtemp(prefix="dnf-test_rpmconf-")

        self.conf_file = (
            os.path.join(self.prefix, '{0}.conf'.format(self.pkgname)),
            b'package = good\ntrue = false\nwhat = "tahw"\n')

        self.conf_file_rpmorig = (
            '{0}.rpmorig'.format(self.conf_file[0]),
            self.conf_file[1])

        self.conf_file_rpmnew = (
            '{0}.rpmnew'.format(self.conf_file[0]),
            b'package = good\ntrue = false\n')

        self.conf_file_rpmsave = (
            '{0}.rpmsave'.format(self.conf_file[0]),
            b'package = bad\ntrue = true\n')

        self.rpmconf_plugin = RpmconfPluginStub(self.pkgname,
                                                self.conf_file[0])
        self.addCleanup(rmtree, self.prefix)

    def _create_conf(self):
        return create_file(*self.conf_file)

    def _create_rpmorig(self):
        return create_file(*self.conf_file_rpmorig)

    def _create_rpmnew(self):
        return create_file(*self.conf_file_rpmnew)

    def _create_rpmsave(self):
        return create_file(*self.conf_file_rpmsave)

    def test_non_interactive(self):
        _, _ = self._create_conf()
        _, _ = self._create_rpmnew()

        with self.rpmconf_plugin as rpmconf,\
                mock.patch("rpmconf.rpmconf.RpmConf.flush_input", return_value='S'),\
                mock.patch("sys.stdout", new_callable=StringIO) as stdout:
            rpmconf._interactive = False
            rpmconf.run()

            lines = stdout.getvalue().splitlines()

        self.assertEqual(len(lines), 0)

    def test_frontend_none(self):
        c_path, c_content = self._create_conf()
        new_path, new_content = self._create_rpmnew()

        with self.rpmconf_plugin as rpmconf,\
                mock.patch("rpmconf.rpmconf.RpmConf.flush_input", return_value='M'),\
                mock.patch("sys.stdout", new_callable=StringIO),\
                mock.patch.dict("os.environ"):
            if os.environ.get("MERGE"):
                del os.environ["MERGE"]
            try:
                rpmconf.frontend = 'env'
                rpmconf.run()
            except SystemExit as e:
                if e.code in (errno.ENOENT, errno.EINTR):
                    self.fail("rpmconf has exited prematurely in the merge phase")
                else:
                    self.fail(
                        "rpmconf has exited prematurely"
                        "with unknown exit code {0}".format(safe_repr(e.code)))

        self.assertTrue(os.access(c_path, os.F_OK))
        with open(c_path, 'rb') as f:
            c_result = f.read()

        self.assertEqual(c_result, c_content)

        self.assertTrue(os.access(new_path, os.F_OK))
        with open(new_path, 'rb') as f:
            new_result = f.read()

        self.assertEqual(new_result, new_content)

    def test_frontend_env(self):
        c_path, _ = self._create_conf()
        new_path, _ = self._create_rpmnew()

        def merge_conf_files(_, conf_file, other_file):
            self.assertEqual(conf_file, c_path)
            self.assertEqual(other_file, new_path)
            os.unlink(new_path)

        with self.rpmconf_plugin as rpmconf,\
                mock.patch.dict("os.environ", MERGE="/usr/bin/accidental_merge_tool"),\
                mock.patch("rpmconf.rpmconf.RpmConf._merge_conf_files", merge_conf_files),\
                mock.patch("rpmconf.rpmconf.RpmConf.flush_input", return_value='M'),\
                mock.patch("sys.stdout", new_callable=StringIO) as stdout:
            rpmconf.frontend = 'env'
            rpmconf.run()

            lines = stdout.getvalue().splitlines()

        expected_last_line_to_f30 = "File {0} was removed by 3rd party. Skipping.".format(new_path)
        # Newer rpmconf changed output since F31
        expected_last_line_from_f31 = "File {0} has been merged.".format(new_path)

        self.assertRegex(lines[-1], "{0}|{1}"
                         .format(expected_last_line_to_f30, expected_last_line_from_f31))

    def test_diff_output(self):
        self._create_conf()
        self._create_rpmnew()
        self._create_rpmsave()

        with self.rpmconf_plugin as rpmconf,\
                mock.patch("sys.stdout", new_callable=StringIO) as stdout:
            rpmconf.diff = True
            rpmconf.run()

            lines = stdout.getvalue().splitlines()

        expected_lines = [
            "--- {0}".format(*self.conf_file),
            "+++ {0}".format(*self.conf_file_rpmnew),
            "@@ -1,3 +1,2 @@",
            " package = good",
            " true = false",
            '-what = "tahw"',
            "--- {0}".format(*self.conf_file_rpmsave),
            "+++ {0}".format(*self.conf_file),
            "@@ -1,2 +1,3 @@",
            "-package = bad",
            "-true = true",
            "+package = good",
            "+true = false",
            '+what = "tahw"',
        ]

        msg_tmpl = "{0} does not start with {1}"
        for line, expected_line in zip_longest(lines, expected_lines, fillvalue=''):
            if not line.startswith(expected_line):
                self.fail(msg_tmpl.format(safe_repr(line), safe_repr(expected_line)))
