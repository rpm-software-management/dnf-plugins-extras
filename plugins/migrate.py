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

from dnf.i18n import ucd
from dnf.yum.history import YumHistory, YumHistoryPackage

import dnf
import dnf.cli
import dnfpluginsextras


_ = dnfpluginsextras._


class Migrate(dnf.Plugin):

    name = 'migrate'

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

    @staticmethod
    def _parse_args(args):
        parser = dnfpluginsextras.ArgumentParser(MigrateCommand.aliases[0])
        parser.add_argument(
            "--nogroups", action="store_true", default=False,
            help=_("do not migrate groups data."))
        parser.add_argument(
            "--nohistory", action="store_true", default=False,
            help=_("do not migrate history data."))
        parser.add_argument(
            "--noyumdb", action="store_true", default=False,
            help=_("do not migrate yumdb data."))
        opts = parser.parse_args(args)
        if opts.help_cmd:
            print(parser.format_help())
            return
        return opts

    def run(self, args):
        opts = self._parse_args(args)

        if not opts:
            return
