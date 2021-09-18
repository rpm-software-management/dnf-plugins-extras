..
  Copyright (C) 2021 Andrzej Pacanowski

  This copyrighted material is made available to anyone wishing to use,
  modify, copy, or redistribute it subject to the terms and conditions of
  the GNU General Public License v.2, or (at your option) any later version.
  This program is distributed in the hope that it will be useful, but WITHOUT
  ANY WARRANTY expressed or implied, including the implied warranties of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
  Public License for more details.  You should have received a copy of the
  GNU General Public License along with this program; if not, write to the
  Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
  02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
  source code or documentation are not subject to the GNU General Public
  License and may only be used or replicated with the express permission of
  Red Hat, Inc.


=========================
DNF rebuild-initrd Plugin
=========================

Runs akmods and dracut for each new kernel installed.

This can solve problem of Nvidia hybrid cards users where nvidia.ko is
required to show plymouth password screen over HDMI.

-------------
Configuration
-------------

``/etc/dnf/plugins/rebuilinitrd.conf``

The minimal plugin configuration file should consists of `[main]` section with `check_module_exists` parameter.::

  [main]
  check_module_exists = 

``check_module_exists``
    string, default: empty

    Optionally we can also check initrd image for presence of desired module eg. nvidia.ko


--------
See Also
--------

:manpage:`dracut(8)`.
:manpage:`akmods(8)`.
:manpage:`lsinitrd(1)`.
