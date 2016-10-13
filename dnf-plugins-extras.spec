%{!?dnf_lowest_compatible: %global dnf_lowest_compatible 1.1.2}
%{!?dnf_not_compatible: %global dnf_not_compatible 2.0}

%bcond_with py3_kickstart

Name:           dnf-plugins-extras
Version:        0.0.12
Release:        1%{?dist}
Summary:        Extras Plugins for DNF
License:        GPLv2+
URL:            https://github.com/rpm-software-management/dnf-plugins-extras
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  cmake
BuildRequires:  gettext
# py2
%if 0%{?fedora} < 23
BuildRequires:  python-dnf >= %{dnf_lowest_compatible}
BuildRequires:  python-dnf < %{dnf_not_compatible}
%else
BuildRequires:  python2-dnf >= %{dnf_lowest_compatible}
BuildRequires:  python2-dnf < %{dnf_not_compatible}
%endif
BuildRequires:  python2-nose
BuildRequires:  python-sphinx
BuildRequires:  python2-devel
%if 0%{?fedora} >= 23
BuildRequires:  python-kickstart
%else
BuildRequires:  pykickstart
%endif
# py3
BuildRequires:  python3-devel
BuildRequires:  python3-dnf >= %{dnf_lowest_compatible}
BuildRequires:  python3-dnf < %{dnf_not_compatible}
BuildRequires:  python3-nose
BuildRequires:  python3-sphinx
%if 0%{?fedora} >= 23
BuildRequires:  python3-kickstart
%endif

%description
Extras Plugins for DNF.

%package -n python-dnf-plugins-extras-common
Summary:        Common files for Extras Plugins for DNF
%if 0%{?fedora} < 23
Requires:       python-dnf >= %{dnf_lowest_compatible}
Requires:       python-dnf < %{dnf_not_compatible}
Provides:       dnf-plugins-extras-common = %{version}-%{release}
Obsoletes:      dnf-plugins-extras-common <= 0.0.4-2
Obsoletes:      dnf-plugins-extras < 0.0.6-3
%else
Requires:       python2-dnf >= %{dnf_lowest_compatible}
Requires:       python2-dnf < %{dnf_not_compatible}
%endif
Obsoletes:      python-dnf-plugins-extras < 0.0.6-3

%description -n python-dnf-plugins-extras-common
Common files for Extras Plugins, Python 2 version.

%package -n python3-dnf-plugins-extras-common
Summary:        Common files for Extras Plugins for DNF
Requires:       python3-dnf >= %{dnf_lowest_compatible}
Requires:       python3-dnf < %{dnf_not_compatible}
%if 0%{?fedora} >= 23
Provides:       dnf-plugins-extras-common = %{version}-%{release}
Obsoletes:      dnf-plugins-extras-common <= 0.0.4-2
Obsoletes:      dnf-plugins-extras < 0.0.6-3
%endif
Obsoletes:      python3-dnf-plugins-extras < 0.0.6-3

%description -n python3-dnf-plugins-extras-common
Common files for Extras Plugins for DNF, Python 3 version.

%package -n python-dnf-plugins-extras-debug
Summary:        Debug Plugin for DNF
Requires:       python-dnf-plugins-extras-common = %{version}-%{release}
%if 0%{?fedora} < 23
Provides:       dnf-command(debug-dump)
Provides:       dnf-command(debug-restore)
Provides:       dnf-plugins-extras-debug = %{version}-%{release}
Obsoletes:      dnf-plugins-extras-debug <= 0.0.4-2
%endif

%description -n python-dnf-plugins-extras-debug
Debug Plugin for DNF, Python 2 version. Writes system RPM configuration to a dump file
and restores it.

%package -n python3-dnf-plugins-extras-debug
Summary:	Debug Plugin for DNF
Requires:	python3-dnf-plugins-extras-common = %{version}-%{release}
%if 0%{?fedora} >= 23
Provides:       dnf-command(debug-dump)
Provides:       dnf-command(debug-restore)
Provides:       dnf-plugins-extras-debug = %{version}-%{release}
Obsoletes:      dnf-plugins-extras-debug <= 0.0.4-2
%endif

%description -n python3-dnf-plugins-extras-debug
Debug Plugin for DNF, Python 3 version. Writes system RPM configuration to
a dump file and restores it.

%package -n python-dnf-plugins-extras-leaves
Summary:        Leaves Plugin for DNF
Requires:       python-dnf-plugins-extras-common = %{version}-%{release}
%if 0%{?fedora} < 23
Provides:       dnf-command(leaves)
Provides:       dnf-plugins-extras-leaves = %{version}-%{release}
Obsoletes:      dnf-plugins-extras-leaves <= 0.0.4-2
Obsoletes:      dnf-plugins-extras-orphans < 0.0.6-3
Obsoletes:      python-dnf-plugins-extras-orphans < 0.0.6-3
%endif

%description -n python-dnf-plugins-extras-leaves
Leaves Plugin for DNF, Python 2 version. List all installed packages
not required by any other installed package.

%package -n python3-dnf-plugins-extras-leaves
Summary:        Leaves Plugin for DNF
Requires:       python3-dnf-plugins-extras-common = %{version}-%{release}
%if 0%{?fedora} >= 23
Provides:       dnf-command(leaves)
Provides:       dnf-plugins-extras-leaves = %{version}-%{release}
Obsoletes:      dnf-plugins-extras-leaves <= 0.0.4-2
Obsoletes:      dnf-plugins-extras-orphans < 0.0.6-3
Obsoletes:      python3-dnf-plugins-extras-orphans < 0.0.6-3
%endif

%description -n python3-dnf-plugins-extras-leaves
Leaves Plugin for DNF, Python 3 version. List all installed packages
not required by any other installed package.

%package -n python-dnf-plugins-extras-local
Summary:        Local Plugin for DNF
Requires:       python-dnf-plugins-extras-common = %{version}-%{release}
Requires:       /usr/bin/createrepo_c
%if 0%{?fedora} < 23
Provides:       dnf-plugins-extras-local = %{version}-%{release}
Obsoletes:      dnf-plugins-extras-local <= 0.0.4-2
%endif

%description -n python-dnf-plugins-extras-local
Local Plugin for DNF, Python 2 version. Automatically copy all downloaded packages to a
repository on the local filesystem and generating repo metadata.

%package -n python3-dnf-plugins-extras-local
Summary:        Local Plugin for DNF
Requires:       python3-dnf-plugins-extras-common = %{version}-%{release}
Requires:       /usr/bin/createrepo_c
%if 0%{?fedora} >= 23
Provides:       dnf-plugins-extras-local = %{version}-%{release}
Obsoletes:      dnf-plugins-extras-local <= 0.0.4-2
%endif

%description -n python3-dnf-plugins-extras-local
Local Plugin for DNF, Python 3 version. Automatically copy all downloaded
packages to a repository on the local filesystem and generating repo metadata.

%package -n python-dnf-plugins-extras-migrate
Summary:        Migrate Plugin for DNF
Requires:       python-dnf-plugins-extras-common = %{version}-%{release}
Requires:       yum
%if 0%{?fedora} < 23
Requires:       python-dnf >= %{dnf_lowest_compatible}
Provides:       dnf-command(migrate)
Provides:       dnf-plugins-extras-migrate = %{version}-%{release}
Obsoletes:      dnf-plugins-extras-migrate <= 0.0.4-2
%else
Requires:       python2-dnf >= %{dnf_lowest_compatible}
%endif

%description -n python-dnf-plugins-extras-migrate
Migrate Plugin for DNF, Python 2 version. igrates yum's history, group and
yumdb data to dnf.

%package -n python-dnf-plugins-extras-kickstart
Summary:        Kickstart Plugin for DNF
Requires:       python-dnf-plugins-extras-common = %{version}-%{release}
Conflicts:      python-dnf-plugins-core <= 0.1.12
%if 0%{?fedora} >= 23
BuildRequires:  python-kickstart
%else
BuildRequires:  pykickstart
%endif
%if 0%{?fedora} < 23
Provides:       dnf-command(kickstart)
Provides:       dnf-plugins-extras-kickstart = %{version}-%{release}
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
Summary:        Kickstart Plugin for DNF
Requires:       python3-dnf-plugins-extras-common = %{version}-%{release}
Requires:       python3-kickstart
Conflicts:      python3-dnf-plugins-core <= 0.1.12
Provides:       dnf-command(kickstart)
Provides:       dnf-plugins-extras-kickstart = %{version}-%{release}

%description -n python3-dnf-plugins-extras-kickstart
Kickstart Plugin for DNF, Python 3 version. Install packages listed in a
Kickstart file.

%endif
%endif

%package -n python-dnf-plugins-extras-repoclosure
Summary:        RepoClosure Plugin for DNF
Requires:       python-dnf-plugins-extras-common = %{version}-%{release}
%if 0%{?fedora} < 23
Provides:       dnf-command(repoclosure)
Provides:       dnf-plugins-extras-repoclosure = %{version}-%{release}
Obsoletes:      dnf-plugins-extras-repoclosure <= 0.0.4-2
%endif

%description -n python-dnf-plugins-extras-repoclosure
RepoClosure Plugin for DNF, Python 2 version. Display a list of unresolved dependencies for
repositories.

%package -n python3-dnf-plugins-extras-repoclosure
Summary:        RepoClosure Plugin for DNF
Requires:       python3-dnf-plugins-extras-common = %{version}-%{release}
%if 0%{?fedora} >= 23
Provides:       dnf-command(repoclosure)
Provides:       dnf-plugins-extras-repoclosure = %{version}-%{release}
Obsoletes:      dnf-plugins-extras-repoclosure <= 0.0.4-2
%endif

%description -n python3-dnf-plugins-extras-repoclosure
RepoClosure Plugin for DNF, Python 3 version. Display a list of unresolved
dependencies for repositories.

%package -n python-dnf-plugins-extras-repograph
Summary:        RepoGraph Plugin for DNF
Requires:       python-dnf-plugins-extras-common = %{version}-%{release}
%if 0%{?fedora} < 23
Provides:       dnf-command(repograph)
Provides:       dnf-plugins-extras-repograph = %{version}-%{release}
Obsoletes:      dnf-plugins-extras-repograph <= 0.0.4-2
%endif

%description -n python-dnf-plugins-extras-repograph
RepoGraph Plugin for DNF, Python 2 version. Output a full package dependency graph in dot format.

%package -n python3-dnf-plugins-extras-repograph
Summary:        RepoGraph Plugin for DNF
Requires:       python3-dnf-plugins-extras-common = %{version}-%{release}
%if 0%{?fedora} >= 23
Provides:       dnf-command(repograph)
Provides:       dnf-plugins-extras-repograph = %{version}-%{release}
Obsoletes:      dnf-plugins-extras-repograph <= 0.0.4-2
%endif

%description -n python3-dnf-plugins-extras-repograph
RepoGraph Plugin for DNF, Python 3 version. Output a full package dependency
graph in dot format.

%package -n python-dnf-plugins-extras-repomanage
Summary:        RepoManage Plugin for DNF
Requires:       python-dnf-plugins-extras-common = %{version}-%{release}
%if 0%{?fedora} < 23
Provides:       dnf-command(repomanage)
Provides:       dnf-plugins-extras-repomanage = %{version}-%{release}
Obsoletes:      dnf-plugins-extras-repomanage <= 0.0.4-2
%endif

%description -n python-dnf-plugins-extras-repomanage
RepoManage Plugin for DNF, Python 2 version. Manage a directory of rpm packages.

%package -n python3-dnf-plugins-extras-repomanage
Summary:        RepoManage Plugin for DNF
Requires:       python3-dnf-plugins-extras-common = %{version}-%{release}
%if 0%{?fedora} >= 23
Provides:       dnf-command(repomanage)
Provides:       dnf-plugins-extras-repomanage = %{version}-%{release}
Obsoletes:      dnf-plugins-extras-repomanage <= 0.0.4-2
%endif

%description -n python3-dnf-plugins-extras-repomanage
RepoManage Plugin for DNF, Python 3 version. Manage a directory of rpm packages.

%package -n python3-dnf-plugins-extras-rpmconf
Summary:        RpmConf Plugin for DNF
Requires:       python3-dnf-plugins-extras-common = %{version}-%{release}
Requires:       python3-rpmconf
%if 0%{?fedora} >= 23
Provides:       dnf-plugins-extras-rpmconf = %{version}-%{release}
%endif

%description -n python3-dnf-plugins-extras-rpmconf
RpmConf Plugin for DNF, Python 3 version. Handles .rpmnew, .rpmsave every
transaction.

%package -n python-dnf-plugins-extras-show-leaves
Summary:        Leaves Plugin for DNF
Requires:       python-dnf-plugins-extras-common = %{version}-%{release}
Requires:       python-dnf-plugins-extras-leaves = %{version}-%{release}
%if 0%{?fedora} < 23
Provides:       dnf-plugins-extras-show-leaves = %{version}-%{release}
%endif

%description -n python-dnf-plugins-extras-show-leaves
Show-leaves Plugin for DNF, Python 2 version. List all installed
packages that are no longer required by any other installed package
after a transaction.

%package -n python3-dnf-plugins-extras-show-leaves
Summary:        Show-leaves Plugin for DNF
Requires:       python3-dnf-plugins-extras-common = %{version}-%{release}
Requires:       python3-dnf-plugins-extras-leaves = %{version}-%{release}
%if 0%{?fedora} >= 23
Provides:       dnf-plugins-extras-show-leaves = %{version}-%{release}
%endif

%description -n python3-dnf-plugins-extras-show-leaves
Show-leaves Plugin for DNF, Python 3 version. List all installed
packages that are no longer required by any other installed package
after a transaction.

%package -n python-dnf-plugins-extras-snapper
Summary:        Snapper Plugin for DNF
Requires:       python-dnf-plugins-extras-common = %{version}-%{release}
Requires:       dbus-python
Requires:       snapper
%if 0%{?fedora} < 23
Provides:       dnf-plugins-extras-snapper = %{version}-%{release}
Obsoletes:      dnf-plugins-extras-snapper <= 0.0.4-2
%endif

%description -n python-dnf-plugins-extras-snapper
Snapper Plugin for DNF, Python 2 version. Creates snapshot every transaction.

%package -n python3-dnf-plugins-extras-snapper
Summary:        Snapper Plugin for DNF
Requires:       python3-dnf-plugins-extras-common = %{version}-%{release}
Requires:       python3-dbus
Requires:       snapper
%if 0%{?fedora} >= 23
Provides:       dnf-plugins-extras-snapper = %{version}-%{release}
Obsoletes:      dnf-plugins-extras-snapper <= 0.0.4-2
%endif

%description -n python3-dnf-plugins-extras-snapper
Snapper Plugin for DNF, Python 3 version. Creates snapshot every transaction.

%package -n python-dnf-plugins-extras-tracer
Summary:        Tracer Plugin for DNF
Requires:       python-dnf-plugins-extras-common = %{version}-%{release}
Requires:       python2-tracer > 0.6.11
%if 0%{?fedora} < 23
Obsoletes:      dnf-plugin-tracer < 0.5.6-2
Provides:       dnf-command(tracer)
Provides:       dnf-plugin-tracer = 1:%{version}-%{release}
Provides:       dnf-plugins-extras-tracer = %{version}-%{release}
Obsoletes:      dnf-plugins-extras-tracer <= 0.0.4-2
%endif

%description -n python-dnf-plugins-extras-tracer
Tracer Plugin for DNF, Python 2 version. Finds outdated running applications in your system
every transaction.

%package -n python3-dnf-plugins-extras-tracer
Summary:        Tracer Plugin for DNF
Requires:       python3-dnf-plugins-extras-common = %{version}-%{release}
Requires:       python3-tracer > 0.6.11
%if 0%{?fedora} >= 23
Obsoletes:      dnf-plugin-tracer < 0.5.6-2
Provides:       dnf-command(tracer)
Provides:       dnf-plugin-tracer = 1:%{version}-%{release}
Provides:       dnf-plugins-extras-tracer = %{version}-%{release}
Obsoletes:      dnf-plugins-extras-tracer <= 0.0.4-2
%endif

%description -n python3-dnf-plugins-extras-tracer
Tracer Plugin for DNF, Python 3 version. Finds outdated running applications in
your system every transaction.

%package -n python-dnf-plugins-extras-versionlock
Summary:        Versionlock Plugin for DNF
Requires:       python-dnf-plugins-extras-common = %{version}-%{release}
%if 0%{?fedora} < 23
Provides:       dnf-command(versionlock)
Provides:       dnf-plugin-versionlock = 1:%{version}-%{release}
Provides:       dnf-plugins-extras-versionlock = %{version}-%{release}
%endif

%description -n python-dnf-plugins-extras-versionlock
Versionlock plugin takes a set of name/versions for packages and excludes all other
versions of those packages. This allows you to e.g. protect packages from being
updated by newer versions.

%package -n python3-dnf-plugins-extras-versionlock
Summary:        Versionlock Plugin for DNF
Requires:       python3-dnf-plugins-extras-common = %{version}-%{release}
%if 0%{?fedora} >= 23
Provides:       dnf-command(versionlock)
Provides:       dnf-plugin-versionlock = 1:%{version}-%{release}
Provides:       dnf-plugins-extras-versionlock = %{version}-%{release}
%endif

%description -n python3-dnf-plugins-extras-versionlock
Versionlock plugin takes a set of name/versions for packages and excludes all other
versions of those packages. This allows you to e.g. protect packages from being
updated by newer versions.

%package -n python3-dnf-plugins-extras-torproxy
Summary:	Torproxy Plugin for DNF
Requires:	python3-dnf-plugins-extras-common = %{version}-%{release}
Requires:   python3-pycurl
%if 0%{?fedora} >= 23
Provides:	dnf-plugin-torproxy = %{version}-%{release}
Provides:	dnf-plugins-extras-torproxy = %{version}-%{release}
%endif

%description -n python3-dnf-plugins-extras-torproxy
Torproxy plugin force dnf to use tor to download packages. It make sure that
tor is working and avoid leaking hostname by using the proper sock5 interface.


%prep
%autosetup
mkdir python2 python3

%build
pushd python2
  %cmake ..
  %make_build
  make doc-man
popd
pushd python3
  %cmake -DPYTHON_DESIRED:str=3 ..
  %make_build
  make doc-man
popd

%install
pushd python2
  %make_install
popd
pushd python3
  %make_install
popd

%find_lang %{name}

%if %{without py3_kickstart}
rm -rf %{buildroot}%{python3_sitelib}/dnf-plugins/kickstart.*
rm -rf %{buildroot}%{python3_sitelib}/dnf-plugins/__pycache__/kickstart.*
%endif

%check
PYTHONPATH="%{buildroot}%{python2_sitelib}:%{buildroot}%{python2_sitelib}/dnf-plugins/" nosetests-%{python2_version} -s tests/
PYTHONPATH="%{buildroot}%{python3_sitelib}:%{buildroot}%{python3_sitelib}/dnf-plugins/" nosetests-%{python3_version} -s tests/

%files
%{_mandir}/man8/dnf.plugin.*

%files -n python-dnf-plugins-extras-common -f %{name}.lang
%license COPYING
%doc AUTHORS README.rst
%{python2_sitelib}/dnfpluginsextras/

%files -n python3-dnf-plugins-extras-common -f %{name}.lang
%license COPYING
%doc AUTHORS README.rst
%{python3_sitelib}/dnfpluginsextras/
%dir %{python3_sitelib}/dnf-plugins/__pycache__/

%files -n python-dnf-plugins-extras-debug
%{python2_sitelib}/dnf-plugins/debug.*

%files -n python3-dnf-plugins-extras-debug
%{python3_sitelib}/dnf-plugins/debug.*
%{python3_sitelib}/dnf-plugins/__pycache__/debug.*

%files -n python-dnf-plugins-extras-leaves
%{python2_sitelib}/dnf-plugins/leaves.*

%files -n python3-dnf-plugins-extras-leaves
%{python3_sitelib}/dnf-plugins/leaves.*
%{python3_sitelib}/dnf-plugins/__pycache__/leaves.*

%files -n python-dnf-plugins-extras-local
%config %{_sysconfdir}/dnf/plugins/local.conf
%{python2_sitelib}/dnf-plugins/local.*

%files -n python3-dnf-plugins-extras-local
%config %{_sysconfdir}/dnf/plugins/local.conf
%{python3_sitelib}/dnf-plugins/local.*
%{python3_sitelib}/dnf-plugins/__pycache__/local.*

%files -n python-dnf-plugins-extras-migrate
%{python2_sitelib}/dnf-plugins/migrate.*

%files -n python-dnf-plugins-extras-kickstart
%{python2_sitelib}/dnf-plugins/kickstart.*

%if 0%{?fedora} >= 23
%if %{with py3_kickstart}
%files -n python3-dnf-plugins-extras-kickstart
%{python3_sitelib}/dnf-plugins/kickstart.*
%{python3_sitelib}/dnf-plugins/__pycache__/kickstart.*
%endif
%endif

%files -n python-dnf-plugins-extras-repoclosure
%{python2_sitelib}/dnf-plugins/repoclosure.*

%files -n python3-dnf-plugins-extras-repoclosure
%{python3_sitelib}/dnf-plugins/repoclosure.*
%{python3_sitelib}/dnf-plugins/__pycache__/repoclosure.*

%files -n python-dnf-plugins-extras-repograph
%{python2_sitelib}/dnf-plugins/repograph.*

%files -n python3-dnf-plugins-extras-repograph
%{python3_sitelib}/dnf-plugins/repograph.*
%{python3_sitelib}/dnf-plugins/__pycache__/repograph.*

%files -n python-dnf-plugins-extras-repomanage
%{python2_sitelib}/dnf-plugins/repomanage.*

%files -n python3-dnf-plugins-extras-repomanage
%{python3_sitelib}/dnf-plugins/repomanage.*
%{python3_sitelib}/dnf-plugins/__pycache__/repomanage.*

%files -n python3-dnf-plugins-extras-rpmconf
%config %{_sysconfdir}/dnf/plugins/rpmconf.conf
%{python3_sitelib}/dnf-plugins/rpm_conf.*
%{python3_sitelib}/dnf-plugins/__pycache__/rpm_conf.*

%files -n python-dnf-plugins-extras-show-leaves
%{python2_sitelib}/dnf-plugins/show_leaves.*

%files -n python3-dnf-plugins-extras-show-leaves
%{python3_sitelib}/dnf-plugins/show_leaves.*
%{python3_sitelib}/dnf-plugins/__pycache__/show_leaves.*

%files -n python-dnf-plugins-extras-snapper
%{python2_sitelib}/dnf-plugins/snapper.*

%files -n python3-dnf-plugins-extras-snapper
%{python3_sitelib}/dnf-plugins/snapper.*
%{python3_sitelib}/dnf-plugins/__pycache__/snapper.*

%files -n python-dnf-plugins-extras-tracer
%{python2_sitelib}/dnf-plugins/tracer.*

%files -n python3-dnf-plugins-extras-tracer
%{python3_sitelib}/dnf-plugins/tracer.*
%{python3_sitelib}/dnf-plugins/__pycache__/tracer.*

%files -n python-dnf-plugins-extras-versionlock
%config %{_sysconfdir}/dnf/plugins/versionlock.conf
%config %{_sysconfdir}/dnf/plugins/versionlock.list
%{python2_sitelib}/dnf-plugins/versionlock.*

%files -n python3-dnf-plugins-extras-versionlock
%config %{_sysconfdir}/dnf/plugins/versionlock.conf
%config %{_sysconfdir}/dnf/plugins/versionlock.list
%{python3_sitelib}/dnf-plugins/versionlock.*
%{python3_sitelib}/dnf-plugins/__pycache__/versionlock.*

%files -n python3-dnf-plugins-extras-torproxy
%config %{_sysconfdir}/dnf/plugins/torproxy.conf
%{python3_sitelib}/dnf-plugins/torproxy.*
%{python3_sitelib}/dnf-plugins/__pycache__/torproxy.*


%changelog
