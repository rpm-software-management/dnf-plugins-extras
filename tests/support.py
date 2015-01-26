# Copyright (C) 2014  Red Hat, Inc.
# Copyright (C) 2015 Igor Gnatenko
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

import dnf
import logging
import sys
import unittest

PY3 = False
if sys.version_info.major >= 3:
    PY3 = True

if PY3:
    from unittest import mock
else:
    from . import mock


class CliStub(object):
    """A class mocking `dnf.cli.Cli`."""

    nogpgcheck = True

    def __init__(self, base):
        """Initialize the CLI."""
        self.base = base
        self.cli_commands = {}
        self.demands = DemandsStub()
        self.logger = logging.getLogger()
        self.register_command(dnf.cli.commands.HelpCommand)

    def register_command(self, command):
        """Register given *command*."""
        self.cli_commands.update({alias: command for alias in command.aliases})


class DemandsStub(object):
    pass


class TestCase(unittest.TestCase):
    def assertEmpty(self, collection):
        return self.assertEqual(len(collection), 0)

    if not PY3:
        assertCountEqual = unittest.TestCase.assertItemsEqual
