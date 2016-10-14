# -*- coding: utf-8 -*-
#
# Calls tracer after every successful transaction.
# Also supplies the 'tracer' command.
#
# Copyright (C) 2015 Jakub Kadlčík
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

from __future__ import absolute_import

import time
import traceback
import dnf.cli
import dnf.util
import dnfpluginsextras
from tracer import Query, Package
from tracer.views.default import DefaultView

_ = dnfpluginsextras._


class Tracer(dnf.Plugin):
    """DNF plugin for `tracer` command"""
    name = "tracer"

    def __init__(self, base, cli):
        super(Tracer, self).__init__(base, cli)
        self.timestamp = time.time()
        self.base = base
        self.cli = cli

    def transaction(self):
        """
        Call after successful transaction
        See https://rpm-software-management.github.io/dnf/api_transaction.html
        """
        # Don't run tracer when uninstalling it
        if dnfpluginsextras.is_erasing(self.base.transaction,
                                       "tracer"):
            return

        # Don't run tracer when preparing chroot for mock
        if self.base.conf.installroot != "/":
            return

        # Don't run tracer when "nothing to do"
        if not len(self.base.transaction):
            return

        installed = set([package.name for package in
                         self.base.transaction.install_set])
        erased = set([package.name for package in
                      self.base.transaction.remove_set])
        packages = [Package(p, time.time()) for p in list(installed | erased)]

        try:
            tracer = TracerFacade(packages)
            tracer.render()

            if len(tracer.apps) != 0:
                print("\n" + _("For more information run:"))
                print("    sudo tracer -iat " + str(self.timestamp))

        except Exception:
            render_error(traceback.format_exc())


class TracerFacade(object):
    def __init__(self, packages, args=None):
        self.apps = self.get_apps(packages)
        self.args = args

    def get_apps(self, packages):
        query = Query()
        return query.from_packages(packages).now().affected_applications().get()

    def render(self):
        # @TODO It is not in the Tracer API yet
        args = self.args if self.args else dnf.util.Bunch(all=False, quiet=False)
        view = DefaultView()
        view.assign("applications", self.apps)
        view.assign("args", args)
        return view.render()


def render_error(err):
    print("Tracer:")
    print(" " + _("Call to Tracer API ended unexpectedly:") + "\n")
    print(err)
    print(_("Please visit https://github.com/FrostyX/tracer/issues "
            "and submit the issue. Thank you"))
    print(_("We apologize for any inconvenience"))
