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
import dnf.cli
import dnfpluginsextras
import subprocess

_ = dnfpluginsextras._


class Tracer(dnf.Plugin):
    """DNF plugin for `tracer` command"""
    name = "tracer"

    def __init__(self, base, cli):
        super(Tracer, self).__init__(base, cli)
        self.timestamp = time.time()
        self.base = base
        self.cli = cli
        if self.cli is not None:
            self.cli.register_command(TracerCommand)

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

        installed = set([package.name for package in
                         self.base.transaction.install_set])
        erased = set([package.name for package in
                      self.base.transaction.remove_set])

        args = ["tracer", "-n"] + list(installed | erased)
        process = subprocess.Popen(
            args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        _print_output(out, err)

        if len(out) != 0:
            print("\n" + _("For more information run:"))
            print("    sudo tracer -iat " + str(self.timestamp))


class TracerCommand(dnf.cli.Command):
    """DNF tracer plugin"""
    aliases = ["tracer"]

    def run(self, args):
        """Called after running `dnf tracer ...`"""
        args = ["tracer"] + args
        process = subprocess.Popen(
            args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        _print_output(out, err)


def _print_output(out, err):
    if len(err) != 0:
        print("Tracer:")
        print("  " + _("Program 'tracer' crashed with following error:") + "\n")
        print(err)
        print(_("Please visit ") +
              "https://github.com/FrostyX/tracer/issues " +
              "and submit the issue. Thank you")
        print(_("We apologize for any inconvenience"))
        return

    if len(out) == 0:
        print(_("You should restart:"))
        print("  " + _("Nothing needs to be restarted"))
        return

    # Last value is blank line
    for line in out.decode("utf8").split("\n")[:-1]:
        print(line)
