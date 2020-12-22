..
  Copyright (C) 2015 Igor Gnatenko

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


==================
DNF rpmconf Plugin
==================

Handles .rpmnew, .rpmsave and .rpmorig after transactions.

-------------
Configuration
-------------

``/etc/dnf/plugins/rpmconf.conf``

The minimal plugin configuration file should consists of `[main]` section with `enabled` parameter.::

  [main]
  enabled = 1

[main] section optional parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``frontend``
    string, default: ``env``

    Defines which frontend should be used for merging. For list of valid frontends see :manpage:`rpmconf(8)`.
    When set to ``env``, the command to use is taken from the environment variable $MERGE.

``diff``
    boolean, default: False

    Defines whether plugin should only display file differences.

``unattended``
    string, default: None

    Defines if unattended operation should be used and in which mode.
    For list of valid modes see :manpage:`rpmconf(8)`.

--------
See Also
--------

:manpage:`rpmconf(8)`.
