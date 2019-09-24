# Show any DNF variables
#
# Copyright (2018).  Fermi Research Alliance, LLC
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

from dnfpluginsextras import _

from dnf import Plugin
from dnf.cli import commands

import dnf.conf.substitutions


class ShowVars(Plugin):
    """DNF Plugin to add the showvars command"""

    name = 'showvars'

    def __init__(self, base, cli):
        """Initialize the plugin instance."""
        super(ShowVars, self).__init__(base, cli)
        if cli is not None:
            cli.register_command(ShowVarsCommand)


class ShowVarsCommand(commands.Command):
    """A class containing methods needed by the cli to execute the
    showvars command.
    """

    aliases = ('showvars',)
    summary = _('show all active dnf variables')

    def run(self):
        dnfvars = dnf.conf.substitutions.Substitutions()
        dnfvars.update_from_etc(self.base.conf.installroot)

        defined = list(dnfvars.keys())
        defined.append('basearch')
        defined.append('releasever')
        defined.sort()
        for var in defined:
            if var == 'basearch':
                print("basearch=" + self.base.conf.basearch)
            elif var == 'releasever':
                print("releasever=" + self.base.conf.releasever)
            else:
                print(var + '=' + dnfvars[var])
