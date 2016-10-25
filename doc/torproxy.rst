..
  Copyright (C) 2016 Michael Scherer

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

===================
DNF torproxy Plugin
===================

-----------
Description
-----------

Automatically pass all traffic in the tor network, and abort if tor is not running or blocked, to avoid any kind
of identity leak.

However, if there is a specific proxy settings in the configuration, the plugin will not
overwrite it, assuming that the user did set it on purpose.

-------------
Configuration
-------------

``/etc/dnf/plugins/torproxy.conf``

The minimal content of conf file should contain ``main`` sections with parameters ``enabled`` and
``strict``, otherwise plugin will not work. If the ``strict`` parameter is set to ``True``, torproxy plugin will halt DNF in the case of Tor network unavailability.::

  [main]
  enabled = true
  strict = false

If you do not want to use the default setup of tor, ie running it on the localhost, you can also specify
the port and host of the tor client in a torproxy section like this::

  [torproxy]
  port = 9050
  hostname = tor.example.org

