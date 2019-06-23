################################
Extras DNF Plugins Release Notes
################################

.. contents::

Added offline-upgrade plugin.

===================
4.0.4 Release Notes
===================

* Use improved config parser that preserves order of data
* [system-upgrade] Save module_platform_id option through system upgrade (RhBug:1656509)
* [system-upgrade] On modular systems, system upgrade requires the next module_platform_id

Bugs fixed in 4.0.4:

* :rhbug:`1656509`

===================
4.0.2 Release Notes
===================

Minor changes

===================
4.0.1 Release Notes
===================

Bugs fixed in 4.0.1:

* :rhbug:`1649745`

===================
4.0.0 Release Notes
===================

Bugs fixed in 4.0.0:

* :rhbug:`1638689`
* :rhbug:`1643551`

===================
3.0.2 Release Notes
===================

Bugs fixed in 3.0.2:

* :rhbug:`1597657`

===================
3.0.1 Release Notes
===================

Bugs fixed in 3.0.1:

* :rhbug:`1603806`

===================
3.0.0 Release Notes
===================

Bugs fixed in 3.0.0:

* :rhbug:`1531356`
* :rhbug:`1513823`

===================
2.0.5 Release Notes
===================

Bugs fixed in 2.0.5:

* :rhbug:`1519543`

===================
2.0.4 Release Notes
===================

Bugs fixed in 2.0.4:

* :rhbug:`1516234`
* :rhbug:`1499284`

===================
2.0.3 Release Notes
===================

Bugs fixed in 2.0.3:

* :rhbug:`1473435`
* :rhbug:`1490832`
* :rhbug:`1492036`

===================
2.0.2 Release Notes
===================

CLI changes in 2.0.2:

* Remove ``--datadir`` option from ``system upgrade``

Bugs fixed in 2.0.2:

* :rhbug:`1324151`
* :rhbug:`1387136`
* :rhbug:`1225442`
* :rhbug:`1248806`

===================
2.0.1 Release Notes
===================

Bugs fixed in 2.0.1:

* :rhbug:`1379906`

===================
2.0.0 Release Notes
===================

* Moved ``DEBUG`` plugin from dnf-plugins-extras to dnf-plugins-core
* Moved ``LEAVES`` plugin from dnf-plugins-extras to dnf-plugins-core
* Moved ``LOCAL`` plugin from dnf-plugins-extras to dnf-plugins-core
* Moved ``MIGRATE`` plugin from dnf-plugins-extras to dnf-plugins-core
* Moved ``NEEDS RESTARTING`` plugin from dnf-plugins-extras to dnf-plugins-core
* Moved ``REPOCLOSURE`` plugin from dnf-plugins-extras to dnf-plugins-core
* Moved ``REPOGRAPH`` plugin from dnf-plugins-extras to dnf-plugins-core
* Moved ``REPOMANAGE`` plugin from dnf-plugins-extras to dnf-plugins-core
* Moved ``SHOW LEAVES`` plugin from dnf-plugins-extras to dnf-plugins-core
* Moved ``VERSIONLOCK`` plugin from dnf-plugins-extras to dnf-plugins-core

=====================
 0.10.0 Release Notes
=====================

DNF 2.0 compatibility (not compatible with 1.x), bugfixes and performance
improvements.

Incorporated system-upgrade plugin.

Bugs fixed in 0.10.0:

* :rhbug:`1303983`
* :rhbug:`1365698`
* :rhbug:`1377742`
* :rhbug:`1383603`

=====================
 0.0.12 Release Notes
=====================

Bugfixes in :doc:`local` plugin. Fixes in packaging.

=====================
 0.0.11 Release Notes
=====================

Bugfix in :doc:`kickstart` packaging plugin.

=====================
 0.0.10 Release Notes
=====================

Provides :doc:`kickstart`. Bugfixes in some plugins.

Bugs fixed in 0.0.10:

* :rhbug:`1263699`
* :rhbug:`1225894`

====================
 0.0.9 Release Notes
====================

Provides :doc:`show-leaves` and :doc:`versionlock`. Fixed some crashes in :doc:`migrate` and :doc:`repomanage`.

Bugs fixed in 0.0.9:

* :rhbug:`1226607`
* :rhbug:`1225282`
* :rhbug:`1230503`

====================
 0.0.8 Release Notes
====================

Many fixes in :doc:`migrate` plugin. Few cleanups in packagingi, now you can install `dnf-command(migrate)` to get `dnf-plugins-extras-migrare` installed.

Bugs fixed in 0.0.8:

* :rhbug:`1208773`
* :rhbug:`1211596`
* :rhbug:`1214807`
* :rhbug:`1223034`

====================
 0.0.7 Release Notes
====================

Renamed orphans to :doc:`leaves`. Fixed some crashes in :doc:`tracer`, :doc:`migrate` and :doc:`local`. Renamed ``--repoid`` to ``--repo`` in :doc:`repoclosure` and :doc:`repograph`. Old option saved for compatibility.

Bugs fixed in 0.0.7:

* :rhbug:`1208614`
* :rhbug:`1209864`
* :rhbug:`1209043`

====================
 0.0.6 Release Notes
====================

Provides :doc:`migrate` and :doc:`orphans`.

Bugs fixed in 0.0.6:

* :rhbug:`1201471`

====================
 0.0.5 Release Notes
====================

Adapt packaging to install Python 3 version for F23+. Provides: :doc:`debug`

Bugs fixed in 0.0.5:

* :rhbug:`1187763`
* :rhbug:`1192779`

====================
 0.0.4 Release Notes
====================

Fixes in packaging, include man pages for plugins.

====================
 0.0.3 Release Notes
====================

Trivial fixes in packaging, few improvements for plugins, tests for plugins. Provides: :doc:`local`, :doc:`repograph` and :doc:`repoclosure`.

Bugs fixed in 0.0.3:

* :rhbug:`1177631`
* :rhbug:`991014`

====================
 0.0.2 Release Notes
====================

Provides :doc:`repomanage`, :doc:`rpmconf` and :doc:`tracer`.

Bugs fixed in 0.0.2:

* :rhbug:`1048541`

====================
 0.0.1 Release Notes
====================

Provides :doc:`snapper`.
