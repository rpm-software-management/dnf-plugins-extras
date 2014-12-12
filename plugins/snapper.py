# creates snapshots via 'snapper'.
#
# Copyright (C) 2014 Igor Gnatenko
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
from dbus import SystemBus, Interface, DBusException


class Snapper(dnf.Plugin):
    name = 'snapper'

    def __init__(self, base, cli):
        self.base = base
        # TODO: get full cmdline for description
        # https://bugzilla.redhat.com/show_bug.cgi?id=1173620
        self.description = "dnf"

    def transaction(self):
        try:
            bus = SystemBus()
            snapper = Interface(bus.get_object('org.opensuse.Snapper',
                                               '/org/opensuse/Snapper'),
                                dbus_interface='org.opensuse.Snapper')
        except DBusException as e:
            logger.critical(
                "snapper: " + _("connect to snapperd failed: %s"), e
            )
            return
        try:
            snapper.GetConfig("root")
        except DBusException:
            snapper.CreateConfig("root", "/")
        try:
            logger.info(
                "snapper: " + _("creating snapshot")
            )
            snap = snapper.CreateSingleSnapshot("root", self.description, "", {})
            logger.debug(
                "snapper: " + _("created snapshot %d"), snap
            )
        except DBusException as e:
            logger.critical(
                "snapper: " + _("creating snapshot failed: %s"), e
            )
