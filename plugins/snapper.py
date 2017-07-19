# creates snapshots via 'snapper'.
#
# Copyright (C) 2014 Igor Gnatenko
# Copyright (C) 2017 Red Hat
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

from dbus import SystemBus, Interface, DBusException
import sys

from dnfpluginsextras import _, logger
import dnf


class Snapper(dnf.Plugin):
    name = 'snapper'

    def __init__(self, base, cli):
        self.base = base
        self.description = " ".join(sys.argv)
        self._pre_snap_created = False
        self._snapper = None
        self._pre_snap_number = None

    def pre_transaction(self):
        if not len(self.base.transaction):
            return

        try:
            bus = SystemBus()
            self._snapper = Interface(bus.get_object('org.opensuse.Snapper',
                                      '/org/opensuse/Snapper'),
                                      dbus_interface='org.opensuse.Snapper')
        except DBusException as e:
            logger.critical(
                "snapper: " + _("connect to snapperd failed: %s"), e
            )
            return

        try:
            logger.debug(
                "snapper: " + _("creating pre_snapshot")
            )
            self._pre_snap_number = self._snapper.CreatePreSnapshot("root", self.description,
                                                                    "number", {})
            self._pre_snap_created = True
            logger.debug(
                "snapper: " + _("created pre_snapshot %d"), self._pre_snap_number
            )
        except DBusException as e:
            logger.critical(
                "snapper: " + _("creating pre_snapshot failed: %s"), e
            )

    def transaction(self):
        if not self._pre_snap_created:
            logger.debug(
                "snapper: " + _("skipping post_snapshot because creation of pre_snapshot failed")
            )
            return

        try:
            logger.debug(
                "snapper: " + _("creating post_snapshot")
            )
            snap_post_number = self._snapper.CreatePostSnapshot("root", self._pre_snap_number,
                                                                self.description, "number", {})
            logger.debug(
                "snapper: " + _("created post_snapshot %d"), snap_post_number
            )
        except DBusException as e:
            logger.critical(
                "snapper: " + _("creating post_snapshot failed: %s"), e
            )
