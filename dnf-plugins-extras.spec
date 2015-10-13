%{!?dnf_lowest_compatible: %global dnf_lowest_compatible 1.1.2}
%{!?dnf_not_compatible: %global dnf_not_compatible 2.0}

%bcond_with py3_kickstart

Name:		dnf-plugins-extras
Version:	0.0.10
Release:	1%{?dist}
Summary:	Extras Plugins for DNF
Group:		System Environment/Base
License:	GPLv2+
URL:		https://github.com/rpm-software-management/dnf-plugins-extras
Source0:	%{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	cmake
BuildRequires:	gettext
# py2
%if 0%{?fedora} < 23
BuildRequires:	python-dnf >= %{dnf_lowest_compatible}
BuildRequires:	python-dnf < %{dnf_not_compatible}
%else
BuildRequires:	python2-dnf >= %{dnf_lowest_compatible}
BuildRequires:	python2-dnf < %{dnf_not_compatible}
%endif
BuildRequires:	python-nose
BuildRequires:	python-sphinx
BuildRequires:	python2-devel
%if 0%{?fedora} >= 23
BuildRequires:   python-kickstart
%else
BuildRequires:   pykickstart
%endif
# py3
BuildRequires:	python3-devel
BuildRequires:	python3-dnf >= %{dnf_lowest_compatible}
BuildRequires:	python3-dnf < %{dnf_not_compatible}
BuildRequires:	python3-nose
BuildRequires:	python3-sphinx
%if 0%{?fedora} >= 23
BuildRequires:	python3-kickstart
%endif

%description
Extras Plugins for DNF.

%package -n python-dnf-plugins-extras-common
Summary:	Common files for Extras Plugins for DNF
%if 0%{?fedora} < 23
Requires:	python-dnf >= %{dnf_lowest_compatible}
Requires:	python-dnf < %{dnf_not_compatible}
Provides:	dnf-plugins-extras-common = %{version}-%{release}
Obsoletes:	dnf-plugins-extras-common <= 0.0.4-2
Obsoletes:	dnf-plugins-extras < 0.0.6-3
%else
Requires:	python2-dnf >= %{dnf_lowest_compatible}
Requires:	python2-dnf < %{dnf_not_compatible}
%endif
Obsoletes:	python-dnf-plugins-extras < 0.0.6-3

%description -n python-dnf-plugins-extras-common
Common files for Extras Plugins, Python 2 version.

%package -n python3-dnf-plugins-extras-common
Summary:	Common files for Extras Plugins for DNF
Requires:	python3-dnf >= %{dnf_lowest_compatible}
Requires:	python3-dnf < %{dnf_not_compatible}
%if 0%{?fedora} >= 23
Provides:	dnf-plugins-extras-common = %{version}-%{release}
Obsoletes:	dnf-plugins-extras-common <= 0.0.4-2
Obsoletes:	dnf-plugins-extras < 0.0.6-3
%endif
Obsoletes:	python3-dnf-plugins-extras < 0.0.6-3

%description -n python3-dnf-plugins-extras-common
Common files for Extras Plugins for DNF, Python 3 version.

%package -n python-dnf-plugins-extras-debug
Summary:	Debug Plugin for DNF
Requires:	python-dnf-plugins-extras-common = %{version}-%{release}
%if 0%{?fedora} < 23
Provides:	dnf-command(debug-dump)
Provides:	dnf-command(debug-restore)
Provides:	dnf-plugins-extras-debug = %{version}-%{release}
Obsoletes:	dnf-plugins-extras-debug <= 0.0.4-2
%endif

%description -n python-dnf-plugins-extras-debug
Debug Plugin for DNF, Python 2 version. Writes system RPM configuration to a dump file
and restores it.

%package -n python3-dnf-plugins-extras-debug
Summary:	Debug Plugin for DNF
Requires:	python3-dnf-plugins-extras-common = %{version}-%{release}
%if 0%{?fedora} >= 23
Provides:	dnf-command(debug-dump)
Provides:	dnf-command(debug-restore)
Provides:	dnf-plugins-extras-debug = %{version}-%{release}
Obsoletes:	dnf-plugins-extras-debug <= 0.0.4-2
%endif

%description -n python3-dnf-plugins-extras-debug
Debug Plugin for DNF, Python 3 version. Writes system RPM configuration to
a dump file and restores it.

%package -n python-dnf-plugins-extras-leaves
Summary:	Leaves Plugin for DNF
Requires:	python-dnf-plugins-extras-common = %{version}-%{release}
%if 0%{?fedora} < 23
Provides:	dnf-command(leaves)
Provides:	dnf-plugins-extras-leaves = %{version}-%{release}
Obsoletes:	dnf-plugins-extras-leaves <= 0.0.4-2
Obsoletes:	dnf-plugins-extras-orphans < 0.0.6-3
Obsoletes:	python-dnf-plugins-extras-orphans < 0.0.6-3
%endif

%description -n python-dnf-plugins-extras-leaves
Leaves Plugin for DNF, Python 2 version. List all installed packages
not required by any other installed package.

%package -n python3-dnf-plugins-extras-leaves
Summary:	Leaves Plugin for DNF
Requires:	python3-dnf-plugins-extras-common = %{version}-%{release}
%if 0%{?fedora} >= 23
Provides:	dnf-command(leaves)
Provides:	dnf-plugins-extras-leaves = %{version}-%{release}
Obsoletes:	dnf-plugins-extras-leaves <= 0.0.4-2
Obsoletes:	dnf-plugins-extras-orphans < 0.0.6-3
Obsoletes:	python3-dnf-plugins-extras-orphans < 0.0.6-3
%endif

%description -n python3-dnf-plugins-extras-leaves
Leaves Plugin for DNF, Python 3 version. List all installed packages
not required by any other installed package.

%package -n python-dnf-plugins-extras-local
Summary:	Local Plugin for DNF
Requires:	python-dnf-plugins-extras-common = %{version}-%{release}
Requires:	/usr/bin/createrepo_c
%if 0%{?fedora} < 23
Provides:	dnf-plugins-extras-local = %{version}-%{release}
Obsoletes:	dnf-plugins-extras-local <= 0.0.4-2
%endif

%description -n python-dnf-plugins-extras-local
Local Plugin for DNF, Python 2 version. Automatically copy all downloaded packages to a
repository on the local filesystem and generating repo metadata.

%package -n python3-dnf-plugins-extras-local
Summary:	Local Plugin for DNF
Requires:	python3-dnf-plugins-extras-common = %{version}-%{release}
Requires:	/usr/bin/createrepo_c
%if 0%{?fedora} >= 23
Provides:	dnf-plugins-extras-local = %{version}-%{release}
Obsoletes:	dnf-plugins-extras-local <= 0.0.4-2
%endif

%description -n python3-dnf-plugins-extras-local
Local Plugin for DNF, Python 3 version. Automatically copy all downloaded
packages to a repository on the local filesystem and generating repo metadata.

%package -n python-dnf-plugins-extras-migrate
Summary:	Migrate Plugin for DNF
Requires:	python-dnf-plugins-extras-common = %{version}-%{release}
Requires:	yum
%if 0%{?fedora} < 23
Requires:	python-dnf >= %{dnf_lowest_compatible}
Provides:	dnf-command(migrate)
Provides:	dnf-plugins-extras-migrate = %{version}-%{release}
Obsoletes:	dnf-plugins-extras-migrate <= 0.0.4-2
%else
Requires:   python2-dnf >= %{dnf_lowest_compatible}
%endif

%description -n python-dnf-plugins-extras-migrate
Migrate Plugin for DNF, Python 2 version. igrates yum's history, group and
yumdb data to dnf.

%package -n python-dnf-plugins-extras-kickstart
Summary:	Kickstart Plugin for DNF
Requires:	python-dnf-plugins-extras-common = %{version}-%{release}
Conflicts:	python-dnf-plugins-core <= 0.1.12
%if 0%{?fedora} >= 23
BuildRequires:   python-kickstart
%else
BuildRequires:   pykickstart
%endif
%if 0%{?fedora} < 23
Provides:	dnf-command(kickstart)
Provides:	dnf-plugins-extras-kickstart = %{version}-%{release}
%endif
%if 0%{?fedora} >= 23
%if %{without py3_kickstart}
Provides:       dnf-command(kickstart)
Provides:       dnf-plugins-extras-kickstart = %{version}-%{release}
%endif
%endif

%description -n python-dnf-plugins-extras-kickstart
Kickstart Plugin for DNF, Python 2 version. Install packages listed in a
Kickstart file.

%if %{with py3_kickstart}
%if 0%{?fedora} >= 23
%package -n python3-dnf-plugins-extras-kickstart
Summary:	Kickstart Plugin for DNF
Requires:	python3-dnf-plugins-extras-common = %{version}-%{release}
Requires:	python3-kickstart
Conflicts:	python3-dnf-plugins-core <= 0.1.12
Provides:	dnf-command(kickstart)
Provides:	dnf-plugins-extras-kickstart = %{version}-%{release}

%description -n python3-dnf-plugins-extras-kickstart
Kickstart Plugin for DNF, Python 3 version. Install packages listed in a
Kickstart file.

%endif
%endif

%package -n python-dnf-plugins-extras-repoclosure
Summary:	RepoClosure Plugin for DNF
Requires:	python-dnf-plugins-extras-common = %{version}-%{release}
%if 0%{?fedora} < 23
Provides:	dnf-command(repoclosure)
Provides:	dnf-plugins-extras-repoclosure = %{version}-%{release}
Obsoletes:	dnf-plugins-extras-repoclosure <= 0.0.4-2
%endif

%description -n python-dnf-plugins-extras-repoclosure
RepoClosure Plugin for DNF, Python 2 version. Display a list of unresolved dependencies for
repositories.

%package -n python3-dnf-plugins-extras-repoclosure
Summary:	RepoClosure Plugin for DNF
Requires:	python3-dnf-plugins-extras-common = %{version}-%{release}
%if 0%{?fedora} >= 23
Provides:	dnf-command(repoclosure)
Provides:	dnf-plugins-extras-repoclosure = %{version}-%{release}
Obsoletes:	dnf-plugins-extras-repoclosure <= 0.0.4-2
%endif

%description -n python3-dnf-plugins-extras-repoclosure
RepoClosure Plugin for DNF, Python 3 version. Display a list of unresolved
dependencies for repositories.

%package -n python-dnf-plugins-extras-repograph
Summary:	RepoGraph Plugin for DNF
Requires:	python-dnf-plugins-extras-common = %{version}-%{release}
%if 0%{?fedora} < 23
Provides:	dnf-command(repograph)
Provides:	dnf-plugins-extras-repograph = %{version}-%{release}
Obsoletes:	dnf-plugins-extras-repograph <= 0.0.4-2
%endif

%description -n python-dnf-plugins-extras-repograph
RepoGraph Plugin for DNF, Python 2 version. Output a full package dependency graph in dot format.

%package -n python3-dnf-plugins-extras-repograph
Summary:	RepoGraph Plugin for DNF
Requires:	python3-dnf-plugins-extras-common = %{version}-%{release}
%if 0%{?fedora} >= 23
Provides:	dnf-command(repograph)
Provides:	dnf-plugins-extras-repograph = %{version}-%{release}
Obsoletes:	dnf-plugins-extras-repograph <= 0.0.4-2
%endif

%description -n python3-dnf-plugins-extras-repograph
RepoGraph Plugin for DNF, Python 3 version. Output a full package dependency
graph in dot format.

%package -n python-dnf-plugins-extras-repomanage
Summary:	RepoManage Plugin for DNF
Requires:	python-dnf-plugins-extras-common = %{version}-%{release}
%if 0%{?fedora} < 23
Provides:	dnf-command(repomanage)
Provides:	dnf-plugins-extras-repomanage = %{version}-%{release}
Obsoletes:	dnf-plugins-extras-repomanage <= 0.0.4-2
%endif

%description -n python-dnf-plugins-extras-repomanage
RepoManage Plugin for DNF, Python 2 version. Manage a directory of rpm packages.

%package -n python3-dnf-plugins-extras-repomanage
Summary:	RepoManage Plugin for DNF
Requires:	python3-dnf-plugins-extras-common = %{version}-%{release}
%if 0%{?fedora} >= 23
Provides:	dnf-command(repomanage)
Provides:	dnf-plugins-extras-repomanage = %{version}-%{release}
Obsoletes:	dnf-plugins-extras-repomanage <= 0.0.4-2
%endif

%description -n python3-dnf-plugins-extras-repomanage
RepoManage Plugin for DNF, Python 3 version. Manage a directory of rpm packages.

%if 0%{?fedora} > 21
%package -n python3-dnf-plugins-extras-rpmconf
Summary:	RpmConf Plugin for DNF
Requires:	python3-dnf-plugins-extras-common = %{version}-%{release}
Requires:	python3-rpmconf
%if 0%{?fedora} >= 23
Provides:	dnf-plugins-extras-rpmconf = %{version}-%{release}
%endif

%description -n python3-dnf-plugins-extras-rpmconf
RpmConf Plugin for DNF, Python 3 version. Handles .rpmnew, .rpmsave every
transaction.
%endif

%package -n python-dnf-plugins-extras-show-leaves
Summary:	Leaves Plugin for DNF
Requires:	python-dnf-plugins-extras-common = %{version}-%{release}
Requires:	python-dnf-plugins-extras-leaves = %{version}-%{release}
%if 0%{?fedora} < 23
Provides:	dnf-plugins-extras-show-leaves = %{version}-%{release}
%endif

%description -n python-dnf-plugins-extras-show-leaves
Show-leaves Plugin for DNF, Python 2 version. List all installed
packages that are no longer required by any other installed package
after a transaction.

%package -n python3-dnf-plugins-extras-show-leaves
Summary:	Show-leaves Plugin for DNF
Requires:	python3-dnf-plugins-extras-common = %{version}-%{release}
Requires:	python3-dnf-plugins-extras-leaves = %{version}-%{release}
%if 0%{?fedora} >= 23
Provides:	dnf-plugins-extras-show-leaves = %{version}-%{release}
%endif

%description -n python3-dnf-plugins-extras-show-leaves
Show-leaves Plugin for DNF, Python 3 version. List all installed
packages that are no longer required by any other installed package
after a transaction.

%package -n python-dnf-plugins-extras-snapper
Summary:	Snapper Plugin for DNF
Requires:	python-dnf-plugins-extras-common = %{version}-%{release}
Requires:	dbus-python
Requires:	snapper
%if 0%{?fedora} < 23
Provides:	dnf-plugins-extras-snapper = %{version}-%{release}
Obsoletes:	dnf-plugins-extras-snapper <= 0.0.4-2
%endif

%description -n python-dnf-plugins-extras-snapper
Snapper Plugin for DNF, Python 2 version. Creates snapshot every transaction.

%package -n python3-dnf-plugins-extras-snapper
Summary:	Snapper Plugin for DNF
Requires:	python3-dnf-plugins-extras-common = %{version}-%{release}
Requires:	python3-dbus
Requires:	snapper
%if 0%{?fedora} >= 23
Provides:	dnf-plugins-extras-snapper = %{version}-%{release}
Obsoletes:	dnf-plugins-extras-snapper <= 0.0.4-2
%endif

%description -n python3-dnf-plugins-extras-snapper
Snapper Plugin for DNF, Python 3 version. Creates snapshot every transaction.

%package -n python-dnf-plugins-extras-tracer
Summary:	Tracer Plugin for DNF
Requires:	python-dnf-plugins-extras-common = %{version}-%{release}
Requires:	tracer
%if 0%{?fedora} < 23
Obsoletes:	dnf-plugin-tracer < 0.5.6-2
Provides:	dnf-command(tracer)
Provides:	dnf-plugin-tracer = 1:%{version}-%{release}
Provides:	dnf-plugins-extras-tracer = %{version}-%{release}
Obsoletes:	dnf-plugins-extras-tracer <= 0.0.4-2
%endif

%description -n python-dnf-plugins-extras-tracer
Tracer Plugin for DNF, Python 2 version. Finds outdated running applications in your system
every transaction.

%package -n python3-dnf-plugins-extras-tracer
Summary:	Tracer Plugin for DNF
Requires:	python3-dnf-plugins-extras-common = %{version}-%{release}
Requires:	tracer
%if 0%{?fedora} >= 23
Obsoletes:	dnf-plugin-tracer < 0.5.6-2
Provides:	dnf-command(tracer)
Provides:	dnf-plugin-tracer = 1:%{version}-%{release}
Provides:	dnf-plugins-extras-tracer = %{version}-%{release}
Obsoletes:	dnf-plugins-extras-tracer <= 0.0.4-2
%endif

%description -n python3-dnf-plugins-extras-tracer
Tracer Plugin for DNF, Python 3 version. Finds outdated running applications in
your system every transaction.

%package -n python-dnf-plugins-extras-versionlock
Summary:	Versionlock Plugin for DNF
Requires:	python-dnf-plugins-extras-common = %{version}-%{release}
%if 0%{?fedora} < 23
Provides:	dnf-command(versionlock)
Provides:	dnf-plugin-versionlock = 1:%{version}-%{release}
Provides:	dnf-plugins-extras-versionlock = %{version}-%{release}
%endif

%description -n python-dnf-plugins-extras-versionlock
Versionlock plugin takes a set of name/versions for packages and excludes all other
versions of those packages. This allows you to e.g. protect packages from being
updated by newer versions.

%package -n python3-dnf-plugins-extras-versionlock
Summary:	Versionlock Plugin for DNF
Requires:	python3-dnf-plugins-extras-common = %{version}-%{release}
%if 0%{?fedora} >= 23
Provides:	dnf-command(versionlock)
Provides:	dnf-plugin-versionlock = 1:%{version}-%{release}
Provides:	dnf-plugins-extras-versionlock = %{version}-%{release}
%endif

%description -n python3-dnf-plugins-extras-versionlock
Versionlock plugin takes a set of name/versions for packages and excludes all other
versions of those packages. This allows you to e.g. protect packages from being
updated by newer versions.

%prep
%setup -q
rm -rf py3
mkdir ../py3
cp -a . ../py3/
mv ../py3 ./

%build
%cmake .
make %{?_smp_mflags}
make doc-man
pushd py3
%cmake -DPYTHON_DESIRED:str=3 .
make %{?_smp_mflags}
make doc-man
popd

%install
%make_install
%find_lang %{name}
pushd py3
%make_install
popd

%if 0%{?fedora} <= 21
rm -f %{buildroot}%{python3_sitelib}/dnf-plugins/rpm_conf.*
rm -f %{buildroot}%{python3_sitelib}/dnf-plugins/__pycache__/rpm_conf.*
rm -f %{buildroot}%{_mandir}/man8/dnf.plugin.rpmconf.*
%endif

%if %{without py3_kickstart}
rm -rf %{buildroot}%{python3_sitelib}/dnf-plugins/kickstart.*
rm -rf %{buildroot}%{python3_sitelib}/dnf-plugins/__pycache__/kickstart.*
%endif

%check
PYTHONPATH=./plugins /usr/bin/nosetests-2.* -s tests/
PYTHONPATH=./plugins /usr/bin/nosetests-3.* -s tests/

%files -n python-dnf-plugins-extras-common -f %{name}.lang
%doc AUTHORS COPYING README.rst
%{python_sitelib}/dnfpluginsextras/

%files -n python3-dnf-plugins-extras-common -f %{name}.lang
%doc AUTHORS COPYING README.rst
%{python3_sitelib}/dnfpluginsextras/
%dir %{python3_sitelib}/dnf-plugins/__pycache__/

%files -n python-dnf-plugins-extras-debug
%{python_sitelib}/dnf-plugins/debug.*
%{_mandir}/man8/dnf.plugin.debug.*

%files -n python3-dnf-plugins-extras-debug
%{python3_sitelib}/dnf-plugins/debug.*
%{python3_sitelib}/dnf-plugins/__pycache__/debug.*
%{_mandir}/man8/dnf.plugin.debug.*

%files -n python-dnf-plugins-extras-leaves
%{python_sitelib}/dnf-plugins/leaves.*
%{_mandir}/man8/dnf.plugin.leaves.*

%files -n python3-dnf-plugins-extras-leaves
%{python3_sitelib}/dnf-plugins/leaves.*
%{python3_sitelib}/dnf-plugins/__pycache__/leaves.*
%{_mandir}/man8/dnf.plugin.leaves.*

%files -n python-dnf-plugins-extras-local
%config %{_sysconfdir}/dnf/plugins/local.conf
%{python_sitelib}/dnf-plugins/local.*
%{_mandir}/man8/dnf.plugin.local.*

%files -n python3-dnf-plugins-extras-local
%config %{_sysconfdir}/dnf/plugins/local.conf
%{python3_sitelib}/dnf-plugins/local.*
%{python3_sitelib}/dnf-plugins/__pycache__/local.*
%{_mandir}/man8/dnf.plugin.local.*

%files -n python-dnf-plugins-extras-migrate
%{python_sitelib}/dnf-plugins/migrate.*
%{_mandir}/man8/dnf.plugin.migrate.*

%files -n python-dnf-plugins-extras-kickstart
%{python_sitelib}/dnf-plugins/kickstart.*
%{_mandir}/man8/dnf.plugin.kickstart.*

%if 0%{?fedora} >= 23
%if %{with py3_kickstart}
%files -n python3-dnf-plugins-extras-kickstart
%{python3_sitelib}/dnf-plugins/kickstart.*
%{python3_sitelib}/dnf-plugins/__pycache__/kickstart.*
%{_mandir}/man8/dnf.plugin.kickstart.*
%endif
%endif

%files -n python-dnf-plugins-extras-repoclosure
%{python_sitelib}/dnf-plugins/repoclosure.*
%{_mandir}/man8/dnf.plugin.repoclosure.*

%files -n python3-dnf-plugins-extras-repoclosure
%{python3_sitelib}/dnf-plugins/repoclosure.*
%{python3_sitelib}/dnf-plugins/__pycache__/repoclosure.*
%{_mandir}/man8/dnf.plugin.repoclosure.*

%files -n python-dnf-plugins-extras-repograph
%{python_sitelib}/dnf-plugins/repograph.*
%{_mandir}/man8/dnf.plugin.repograph.*

%files -n python3-dnf-plugins-extras-repograph
%{python3_sitelib}/dnf-plugins/repograph.*
%{python3_sitelib}/dnf-plugins/__pycache__/repograph.*
%{_mandir}/man8/dnf.plugin.repograph.*

%files -n python-dnf-plugins-extras-repomanage
%{python_sitelib}/dnf-plugins/repomanage.*
%{_mandir}/man8/dnf.plugin.repomanage.*

%files -n python3-dnf-plugins-extras-repomanage
%{python3_sitelib}/dnf-plugins/repomanage.*
%{python3_sitelib}/dnf-plugins/__pycache__/repomanage.*
%{_mandir}/man8/dnf.plugin.repomanage.*

%if 0%{?fedora} > 21
%files -n python3-dnf-plugins-extras-rpmconf
%{python3_sitelib}/dnf-plugins/rpm_conf.*
%{python3_sitelib}/dnf-plugins/__pycache__/rpm_conf.*
%{_mandir}/man8/dnf.plugin.rpmconf.*
%endif

%files -n python-dnf-plugins-extras-show-leaves
%{python_sitelib}/dnf-plugins/show_leaves.*
%{_mandir}/man8/dnf.plugin.show-leaves.*

%files -n python3-dnf-plugins-extras-show-leaves
%{python3_sitelib}/dnf-plugins/show_leaves.*
%{python3_sitelib}/dnf-plugins/__pycache__/show_leaves.*
%{_mandir}/man8/dnf.plugin.show-leaves.*

%files -n python-dnf-plugins-extras-snapper
%{python_sitelib}/dnf-plugins/snapper.*
%{_mandir}/man8/dnf.plugin.snapper.*

%files -n python3-dnf-plugins-extras-snapper
%{python3_sitelib}/dnf-plugins/snapper.*
%{python3_sitelib}/dnf-plugins/__pycache__/snapper.*
%{_mandir}/man8/dnf.plugin.snapper.*

%files -n python-dnf-plugins-extras-tracer
%{python_sitelib}/dnf-plugins/tracer.*
%{_mandir}/man8/dnf.plugin.tracer.*

%files -n python3-dnf-plugins-extras-tracer
%{python3_sitelib}/dnf-plugins/tracer.*
%{python3_sitelib}/dnf-plugins/__pycache__/tracer.*
%{_mandir}/man8/dnf.plugin.tracer.*

%files -n python-dnf-plugins-extras-versionlock
%config %{_sysconfdir}/dnf/plugins/versionlock.conf
%config %{_sysconfdir}/dnf/plugins/versionlock.list
%{python_sitelib}/dnf-plugins/versionlock.*
%{_mandir}/man8/dnf.plugin.versionlock.*

%files -n python3-dnf-plugins-extras-versionlock
%config %{_sysconfdir}/dnf/plugins/versionlock.conf
%config %{_sysconfdir}/dnf/plugins/versionlock.list
%{python3_sitelib}/dnf-plugins/versionlock.*
%{python3_sitelib}/dnf-plugins/__pycache__/versionlock.*
%{_mandir}/man8/dnf.plugin.versionlock.*

%changelog
* Mon Oct 12 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> 0.0.10-1
- Add BaseCliStub() class to tests/support.py (Neal Gompa (ニール・ゴンパ))
- Disable kickstart plugin for Python 3 (Neal Gompa (ニール・ゴンパ))
- Add kickstart plugin to extra plugins (Neal Gompa (ニール・ゴンパ))
- Add repoclosure --check option (Paul Howarth)
- leaves: fix depth-first search (Emil Renner Berthing)
- snapper: set cleanup type to avoid snapshots accumulating indefinitely
  (RhBug:1263699) (Daniel Miranda)
- snapper: don't run if nothing in transaction (Igor Gnatenko)
- spec: adapt to dnf-1.1.2 packaging in F23 (Jan Silhan)
- tracer: don't run tracer when nothing to do; Fix FrostyX/tracer#38 (Jakub
  Kadlčík)
- migrate: groups: skips not found group (RhBug:1225894) (Jan Silhan)

* Tue Jun 30 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> 0.0.9-1
- repomanage: specify that keep is int (RhBug:1230503) (Igor Gnatenko)
- migrate: hide stderr of yum (RhBug:1225282) (Jan Silhan)
- migrate: don't throw error when yum execution failed (Jan Silhan)
- migrate: stop yum from crushing by setting skip_if_unavailable=1
  (RhBug:1226607) (Jan Silhan)
- implemented package (version)locking (Michael Mraka)
- Initial DNF port of the yum show-leaves plugin (Ville Skyttä)

* Fri May 22 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> 0.0.8-1
- migrate: use Unicodes when migrating YUMDB (RhBug:1223034) (Radek Holy)
- migrate: don't raise error when no groups installed by yum (RhBug:1214807)
  (Jan Silhan)
- migrate: use of LANG C env in yum output (Jan Silhan)
- packaging: allow DNF 1.x.x (Radek Holy)
- packaging: add createrepo_c to requires (RhBug:1211596) (Igor Gnatenko)
- local: drop hook to keep packages cache (Igor Gnatenko)
- packaging: dnf version upper boundaries (Jan Silhan)
- packaging: added plugin command provides (Related:RhBug:1208773) (Jan Silhan)

* Tue Apr 21 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> 0.0.7-1
- doc: release notes 0.0.7 (Igor Gnatenko)
- packaging: fix orphans for leaves subpkg (Igor Gnatenko)
- po: update translations (Igor Gnatenko)
- plugins: rename --repoid to --repo (Michael Mraka)
- tracer: decode subprocess output explicitly from utf8 (Jakub Kadlčík)
- migrate: initialize cursor before commit (Michael Mraka)
- po: update translations (Igor Gnatenko)
- packaging: remove main package which requires others (Igor Gnatenko)
- packaging: fix url for new releases (Igor Gnatenko)
- migrate: do not convert group types (Jan Silhan)
- packaging: migrate requires python-dnf (Jan Silhan)
- migrate: trans_end record may not exist (RhBug:1209043) (Michael Mraka)
- plugins: rename orphans to leaves (RhBug:1209864) (Igor Gnatenko)
- Initialized to use tito. (Igor Gnatenko)
- local: fix crashing if plugin disabled in main section (RhBug:1208614) (Igor Gnatenko)

* Tue Mar 31 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.0.6-2
- migrate: set LANG env to C in system calls (Jan Silhan)
- migrate: added logging to history and groups process (Jan Silhan)
- doc: migrate: changed arguments to dnf migrate [all|groups|history|yumdb] (Radek Holy)
- migrate: added YUMDB support (Radek Holy)
- migrate: added groups support (Jan Silhan)

* Tue Mar 31 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.0.6-1
- doc: include orphans plugin to index (Igor Gnatenko)
- po: update translations (Igor Gnatenko)
- plugins: add migrate plugin (Michael Mraka)
- orphans: use Kosaraju's algorithm (Emil Renner Berthing)
- plugins: add orphans plugin (Emil Renner Berthing)
- tracer: don't print 'nothing to restart' when traceback occurs (RhBug:1201471) (Jakub Kadlčík)

* Mon Mar 02 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.0.5-4
- packaging: properly obsolete common subpkg for f23+ (Igor Gnatenko)

* Fri Feb 27 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.0.5-3
- packaging: add real package python-dnf-plugins-extras (Igor Gnatenko)

* Fri Feb 27 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.0.5-2
- packaging: handle tracer and snapper plugins (Igor Gnatenko)

* Fri Feb 27 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.0.5-1
- po: update translations (Igor Gnatenko)
- packaging: adapt to dnf 0.6.4-2 package split (Jan Silhan)
- plugins: add debug plugin (Michael Mraka)
- tracer: fix printing binary on py3 (RhBug:1192779) (Igor Gnatenko)
- tracer: define installed, erased vars (RhBug:1187763) (Igor Gnatenko)

* Fri Feb 13 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.0.4-1
- packaging: require rpmconf plugin only for f22+ (Igor Gnatenko)
- build: simple script to build test package (Michael Mraka)
- build: more standard way to find out latest commit (Michael Mraka)
- packaging: let gitrev be specified on rpmbuild commandline (Michael Mraka)
- doc: include man pages (Igor Gnatenko)

* Thu Jan 29 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.0.3-1
- po: update translations (Igor Gnatenko)
- packaging: include rpmconf plugin only for F22+ (Igor Gnatenko)
- trivial: drop note about bug (Igor Gnatenko)
- local: prefer verbose option on quiet (Igor Gnatenko)
- local: simplidy parsing code (Igor Gnatenko)
- local: fix output from spawning createrepo (Igor Gnatenko)
- doc: improve documentation for local plugin (Igor Gnatenko)
- repoclosure: store requirements as is (Igor Gnatenko)
- repoclosure: optimize performance and memory usage (Igor Gnatenko)
- build: distribute forgotten files (Igor Gnatenko)
- po: update translations (Igor Gnatenko)
- plugins: add repoclosure plugin (Igor Gnatenko)
- packaging: fix files for common subpkg after one of merges (Igor Gnatenko)
- local: use createrepo_c instead of createrepo (Igor Gnatenko)
- plugins: add local plugin (RhBug:991014) (Igor Gnatenko)
- repograph: set decimal places to 12 for colors (Igor Gnatenko)
- tests: fix indentation in repograph (Igor Gnatenko)
- plugins: add repograph plugin (Igor Gnatenko)
- repomanage: replace dnfpluginscore with dnfpluginsextras (Igor Gnatenko)
- plugins: fix typo in if/else (Igor Gnatenko)
- doc: add note that --new by default for repomanage (Igor Gnatenko)
- snapper: don't make snapshots if user removing snapper (RhBug:1177631) (Igor Gnatenko)
- tests: add tests for repomanage (Igor Gnatenko)
- tests: add initial framework (Igor Gnatenko)
- repomanage: use native pkg.location without path join (Igor Gnatenko)
- packaging: obsolete and provide dnf-plugin-tracer correctly (Igor Gnatenko)

* Sun Jan 25 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.0.2-1
- po: update translations (Igor Gnatenko)
- Revert "rename rpm_conf to rpmconf" (Igor Gnatenko)
- po: update translations (Igor Gnatenko)
- packaging: update descriptions with tracer plugin (Igor Gnatenko)
- plugins: add repomanage plugin (RhBug:1048541) (Igor Gnatenko)
- Don't run tracer if --installroot is set; Fix FrostyX/tracer#15 (Jakub Kadlčík)
- po: update translations (Igor Gnatenko)
- packaging: obsolete dnf-plugin-tracer by dnf-plugins-extras-tracer (Igor Gnatenko)
- doc: include rpmconf to index (Igor Gnatenko)
- packaging: add tracer plugin to distribute (Igor Gnatenko)
- plugins: tracer plugin (Jakub Kadlčík)
- packaging: include rpmconf as Requires for main package (Igor Gnatenko)
- rpmconf: fix super-init-not-called (Igor Gnatenko)
- po: update translations (Igor Gnatenko)
- packaging: archive script the same as in dnf (Igor Gnatenko)
- rename rpm_conf to rpmconf (Igor Gnatenko)
- Add rpmconf plugin (Igor Gnatenko)
- snapper: set description snapshot as command line (Igor Gnatenko)
- packaging: fix requires and email (Igor Gnatenko)
- snapper: change log level for debug stage to debug (Igor Gnatenko)
- snapper: don't do any with snapper config (Igor Gnatenko)
- packaging: split into subpackages (Igor Gnatenko)
- packaging: handle all python files (Igor Gnatenko)
- transifex update (Igor Gnatenko)

* Wed Dec 17 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.0.1-2
- Fix Requires for py3 dbus
- Fix email address in changelog

* Fri Dec 12 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.0.1-1
- The initial package version.
