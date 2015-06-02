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
from dnfpluginsextras import _

import dnf
import dnf.exceptions
import os

PLUGIN_CONF = 'versionlock'
NOT_READABLE = _('Unable to read version lock configuration: %s')
NO_LOCKLIST = _('Locklist not set')

class VersionLock(dnf.Plugin):

    name = 'versionlock'

    def __init__(self, base, cli):
        super(VersionLock, self).__init__(base, cli)
        self.base = base
        self.cli = cli
        self.locklist = None

    def config(self):
        cp = self.read_config(self.base.conf, PLUGIN_CONF)
        self.locklist = cp.get('main','locklist')

    def sack(self):
        if not self.locklist:
            raise dnf.exceptions.Error(NO_LOCKLIST)

        locked = set()
        for pat in self._read_locklist():
            excl = False
            if pat and pat[0] == '!':
                pat = pat[1:]
                excl = True

            subj = dnf.subject.Subject(pat)
            pkgs = subj.get_best_query(self.base.sack)

            if excl:
                self.base.sack.add_excludes(pkgs)
            else:
                locked.update(pkgs.run())

        if locked:
            locked_names = [pkg.name for pkg in locked]
            all_versions = set(self.base.sack.query().filter(name=locked_names))
            other_versions = all_versions.difference(locked)
            self.base.sack.add_excludes(other_versions)

    def _read_locklist(self):
        locklist = []
        try:
            with open(self.locklist) as llfile:
                for line in llfile.readlines():
                    if line.startswith('#') or line.strip() == '':
                        continue
                    locklist.append(line.strip())
        except IOError as e:
            raise dnf.exceptions.Error(NOT_READABLE % e)
        return locklist

