..
  Copyright (C) 2014 Igor Gnatenko
  Copyright (C) 2017 Red Hat

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
DNF snapper Plugin
==================

Creates a pair of snapshots of root filesystem. One snapshot is created just before the transaction run (Pre). This means after a successful transaction check and successful transaction test. And another snapshot is created when the transaction has finished (Post).
The user is not supposed to interact with the plugin in any way.

.. warning:: There is no mechanism to ensure data consistency during creating a snapshot. Files which are written at the same time as snapshot is created (eg. database files) can be corrupted or partially written in snapshot. Restoring such files will cause problems. Moreover, some system files must never be restored. Recommended is to only restore files that belong to the action you want to revert.
