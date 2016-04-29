# kickstart.py, supplies the 'kickstart' command.
#
# Copyright (C) 2013  Red Hat, Inc.
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
from dnfpluginsextras import _, logger

import dnf.cli
import pykickstart.parser


def parse_kickstart_packages(path):
    """Return content of packages sections in the kickstart file."""
    handler = pykickstart.version.makeVersion()
    parser = MaskableKickstartParser(handler)

    # Ignore all commands and sections except the packages.
    handler.maskAllExcept({})
    parser.mask_all({pykickstart.sections.PackageSection.sectionOpen})

    parser.readKickstart(path)

    return handler.packages


class Kickstart(dnf.Plugin):
    """DNF plugin supplying the kickstart command."""

    name = 'kickstart'

    def __init__(self, base, cli):
        """Initialize the plugin instance."""
        super(Kickstart, self).__init__(base, cli)
        if cli is not None:
            cli.register_command(KickstartCommand)


class KickstartCommand(dnf.cli.Command):
    """A command installing groups/packages defined in kickstart files."""

    aliases = ('kickstart',)
    summary = _("Install packages defined in a kickstart file on your system")

    @staticmethod
    def set_argparser(parser):
        parser.add_argument("filename", nargs=1,
                                  help=_("kickstart file"))

    def configure(self, args):
        demands = self.cli.demands
        demands.resolving = True
        demands.root_user = True
        demands.sack_activation = True
        dnf.cli.commands.checkGPGKey(self.base, self.cli)
        dnf.cli.commands.checkEnabledRepo(self.base, self.opts.filename[0])


    def run(self, extcmds):
        """Execute the command."""
        path = self.opts.filename[0]

        try:
            packages = parse_kickstart_packages(path)
        except pykickstart.errors.KickstartError:
            raise dnf.exceptions.Error(_('file cannot be parsed: %s') % path)
        group_names = [group.name for group in packages.groupList]

        if group_names:
            self.base.read_comps()
        try:
            self.base.install_grouplist(group_names)
        except dnf.exceptions.Error:
            are_groups_installed = False
        else:
            are_groups_installed = True

        are_packages_installed = False
        for pattern in packages.packageList:
            try:
                self.base.install(pattern)
            except dnf.exceptions.MarkingError:
                logger.info(_('No package %s available.'), pattern)
            else:
                are_packages_installed = True

        if not are_groups_installed and not are_packages_installed:
            raise dnf.exceptions.Error(_('Nothing to do.'))


class MaskableKickstartParser(pykickstart.parser.KickstartParser):
    """Kickstart files parser able to ignore given sections."""

    def mask_all(self, section_exceptions=()):
        """Ignore all sections except the given sections."""
        null_class = pykickstart.sections.NullSection
        for section_open, _section in self._sections.items():
            if section_open not in section_exceptions:
                self.registerSection(
                    null_class(self.handler, sectionOpen=section_open))
