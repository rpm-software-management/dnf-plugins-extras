################################
Extras DNF Plugins Release Notes
################################

.. contents::

====================
4.0.15 Release Notes
====================

- Bug fixes:
  - system-upgrade: Handle empty transaction on download (RhBug:1917639)

Bugs fixed in 4.0.15:

* :rhbug:`1917639`

====================
4.0.14 Release Notes
====================

- [spec] Add dnf-command() provides for offline commands (RhBug:1917378)

Bugs fixed in 4.0.14:

* :rhbug:`1917378`

====================
4.0.13 Release Notes
====================

- system-upgrade: Use Transaction Store/Replay
- system-upgrade: Pretty-print the state json

Bugs fixed in 4.0.13:


====================
4.0.12 Release Notes
====================

- Update Cmake to pull translations from weblate
- Drop Python 2 support
- README: Add Installation, Contribution, etc.

- New features:
  - Add the DNF_SYSTEM_UPGRADE_NO_REBOOT env variable to control system-upgrade reboot.
  - [system-upgrade] Upgrade groups and environments (RhBug:1845562,1860408)

- Bug fixes:
  - Bugs fixed (RhBug:1863434)

Bugs fixed in 4.0.12:

* :rhbug:`1860408`
* :rhbug:`1845562`
* :rhbug:`1863434`

====================
4.0.10 Release Notes
====================

- Ensure plymouth progressbar is filled up only once (RhBug:1809096)

Bugs fixed in 4.0.10:

* :rhbug:`1809096`

===================
4.0.9 Release Notes
===================

- [doc] move manpages for plugins to "dnf-PLUGIN" (RhBug:1706386)
- Add offline-upgrade and offline-distrosync commands
- [doc] Add description for new offline command
- Store reason for system-upgrade plugin
- Do not show Operation aborted as an error (RhBug:1797427)

Bugs fixed in 4.0.9:

* :rhbug:`1706386`
* :rhbug:`1797427`

===================
4.0.8 Release Notes
===================

- Set clean_requirements_on_remove=False during remove (RhBug:1764169)

Bugs fixed in 4.0.8:

* :rhbug:`1764169`

===================
4.0.7 Release Notes
===================

- Fix kickstart plugin
- Enable kickstart tests for PY3

===================
4.0.6 Release Notes
===================

- [system-upgrade] Use --system-upgrade plymouth mode (RhBug:1681584)
- [system-upgrade] Fix traceback caused by setting gpgcheck options (RhBug:1751103,1746346)
- Fix kickstart plugin (RhBug:1649093)
- [system-upgrade] Ensure identical transaction in download and update steps (RhBug:1758588)
- [system-upgrade] Provide distro specific url for help with system-upgrade

Bugs fixed in 4.0.6:

* :rhbug:`1649093`
* :rhbug:`1681584`
* :rhbug:`1758588`
* :rhbug:`1751103`
* :rhbug:`1746346`

===================
4.0.5 Release Notes
===================

- [system-upgrade] Save gpgcheck and repo_gpgcheck repo options (RhBug:1693677)
- Add showvars plugin for showing what DNF vars are set for the dnf runtime

Bugs fixed in 4.0.5:

* :rhbug:`1693677`

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
