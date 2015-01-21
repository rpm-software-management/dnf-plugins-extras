..
  Copyright (C) 2015 Jakub Kadlčík

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


DNF tracer Plugin
=================

Plugin
------

Calls `tracer <http://tracer-package.com/>`_ after every successful transaction. It finds running applications which are outdated by transaction's packages.

There you can see DNF output with ``dnf-plugins-extras-tracer`` installed:

::

    $[FrostyX  ~]-> sudo dnf update vim-X11
    ...
    Running transaction
      Upgrading    : vim-common-2:7.4.179-1.fc20.i686                           1/6
      Upgrading    : vim-X11-2:7.4.179-1.fc20.i686                              2/6
      Upgrading    : vim-enhanced-2:7.4.179-1.fc20.i686                         3/6
      ...

    Upgraded:
      vim-X11.i686 2:7.4.179-1.fc20           vim-common.i686 2:7.4.179-1.fc20
      vim-enhanced.i686 2:7.4.179-1.fc20

    You should restart:
      gvim

    Done!

It is a good idea to restart those applications, because they can be potentially dangerous. They can contain old security issues, which are fixed in new version.


Command
-------

DNF command for tracer does only one thing. Directly executes tracer with passed arguments.

::

    # You can choose which one you like better
    sudo tracer <arguments>
    # or
    dnf tracer <arguments>

For example `usage <http://docs.tracer-package.com/en/latest/user-guide/>`_ or possible `arguments <http://docs.tracer-package.com/en/latest/manpage/>`_ please visit it's `documentation <http://docs.tracer-package.com>`_.
