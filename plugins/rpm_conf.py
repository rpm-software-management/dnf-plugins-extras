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

from dnfpluginsextras import _, logger

import dnf
from rpmconf import rpmconf


class Rpmconf(dnf.Plugin):
    name = 'rpmconf'

    def __init__(self, base, cli):
        self.base = base
        self.packages = []

    def resolved(self):
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
        rconf = rpmconf.RpmConf(packages=self.packages)
        rconf.run()
