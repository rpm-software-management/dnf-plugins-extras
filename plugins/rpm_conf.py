# handling packages via 'rpmconf'.
#
# Copyright (C) 2015 Igor Gnatenko
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details. You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA. Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#

import sys
import errno

from rpmconf import rpmconf

from dnfpluginsextras import _, logger
import dnf


class Rpmconf(dnf.Plugin):
    name = 'rpmconf'

    def __init__(self, base, cli):
        super().__init__(base, cli)
        self.base = base
        self.packages = []
        self.frontend = None
        self.diff = None

    def config(self):
        self._interactive = True
        if (not sys.stdin or not sys.stdin.isatty()) \
                or self.base.conf.assumeyes \
                or self.base.conf.assumeno:
            self._interactive = False

        conf = self.read_config(self.base.conf)

        if conf.has_section('main') and conf.has_option('main', 'diff'):
            self.diff = conf.getboolean('main', 'diff')
        else:
            self.diff = False

        if conf.has_section('main') and conf.has_option('main', 'frontend'):
            self.frontend = conf.get('main', 'frontend')
        else:
            self.frontend = None

    def resolved(self):
        if not self._interactive:
            return

        tmp = []
        for trans_item in self.base.transaction:
            tmp.append(trans_item.installs())
        for packages in tmp:
            for pkg in packages:
                logger.debug(
                    _("Adding '{}' to list of handling "
                      "packages for rpmconf").format(pkg.name))
                self.packages.append(pkg.name)

    def transaction(self):
        if not self._interactive:
            logger.debug(_("rpmconf plugin will not run "
                           "in non-interactive mode"))
            return

        rconf = rpmconf.RpmConf(
            packages=self.packages,
            frontend=self.frontend,
            diff=self.diff)
        try:
            rconf.run()
        except SystemExit as e:
            if e.code == errno.ENOENT:
                logger.debug(
                    _("ignoring sys.exit from rpmconf "
                      "due to missing MERGE variable"))
            elif e.code == errno.EINTR:
                logger.debug(
                    _("ignoring sys.exit from rpmconf "
                      "due to missing file"))
