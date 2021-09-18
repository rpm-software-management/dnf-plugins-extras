# rebuild-initrd.py, runs akmods and dracut after installation of new kernels.
#
# Copyright (C) 2021 Andrzej Pacanowski <andrzej.pacanowski@gmail.com>
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

import subprocess

from dnfpluginsextras import logger
import dnf


class RebuildInitrd(dnf.Plugin):
    """
    Simple plugin that checks if new kernel is installed and runs akmod / dracut for it.
    """
    name = 'rebuildinitrd'

    def __init__(self, base, cli):
        self.base = base
        self._conf_check_module_exists = ''

    def config(self):
        conf = self.read_config(self.base.conf)
        if conf.has_section('main') and conf.has_option('main', 'check_module_exists'):
            self._conf_check_module_exists = conf.get('main', 'check_module_exists').strip()

    def _akmod(self, kernels):
        subprocess.check_call([
            'akmods',
            '--force',
            '--kernels',
            *kernels
        ])

    def _dracut(self, kernels):
        for kernel in kernels:
            subprocess.check_call([
                'dracut',
                '--force',
                '--kver',
                kernel
            ])

    def _check_module_exists(self, kernels):
        if self._conf_check_module_exists:
            logger.info(
                "%s: Check if %s is available in kernel.",
                self.name, self._conf_check_module_exists
            )
            for kernel in kernels:
                output = subprocess.check_output([
                    'lsinitrd',
                    f'/boot/initramfs-{kernel}.img'
                ], universal_newlines=True)
                if self._conf_check_module_exists in output:
                    logger.info("%s: Successfuly built for %s", self.name, kernel)
                else:
                    logger.critical("%s: ERROR not built for %s", self.name, kernel)

    def transaction(self):
        if not self.base.transaction:
            return

        kernels = [
            f"{package.version}-{package.release}.{package.arch}" for package in filter(
                lambda e: e.name == "kernel",
                self.base.transaction.install_set
            )
        ]

        if kernels:
            logger.info("%s: Kernels for which to rebuild initrd %s", self.name, kernels)
            self._akmod(kernels)
            self._dracut(kernels)
            self._check_module_exists(kernels)
