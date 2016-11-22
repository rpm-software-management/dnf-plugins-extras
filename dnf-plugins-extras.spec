%{!?dnf_lowest_compatible: %global dnf_lowest_compatible 2.0}
%{!?dnf_not_compatible: %global dnf_not_compatible 3.0}

Name:           dnf-plugins-extras
Version:        0.10.0
Release:        1%{?dist}
Summary:        Extras Plugins for DNF
License:        GPLv2+
URL:            https://github.com/rpm-software-management/%{name}
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  cmake
BuildRequires:  gettext
# py2
BuildRequires:  python2-devel
BuildRequires:  python2-dnf >= %{dnf_lowest_compatible}
BuildRequires:  python2-dnf < %{dnf_not_compatible}
BuildRequires:  python2-nose
BuildRequires:  python2-sphinx
BuildRequires:  python-kickstart
# py3
BuildRequires:  python3-devel
BuildRequires:  python3-dnf >= %{dnf_lowest_compatible}
BuildRequires:  python3-dnf < %{dnf_not_compatible}
BuildRequires:  python3-nose
BuildRequires:  python3-sphinx
BuildRequires:  python3-kickstart

%description
Extras Plugins for DNF.

%package -n %{name}-common-data
Summary:        Common data files for Extras Plugins for DNF

%description -n %{name}-common-data
Common data files for Extras Plugins

%package -n python2-%{name}-common
Summary:        Common files for Extras Plugins for DNF
Requires:       python2-dnf >= %{dnf_lowest_compatible}
Requires:       python2-dnf < %{dnf_not_compatible}
Requires:       %{name}-common-data = %{version}-%{release}
%{?python_provide:%python_provide python2-%{name}-common}

%description -n python2-%{name}-common
Common files for Extras Plugins, Python 2 version.

%package -n python3-%{name}-common
Summary:        Common files for Extras Plugins for DNF
Requires:       python3-dnf >= %{dnf_lowest_compatible}
Requires:       python3-dnf < %{dnf_not_compatible}
Requires:       %{name}-common-data = %{version}-%{release}
%{?python_provide:%python_provide python3-%{name}-common}
Provides:       %{name}-common = %{version}-%{release}
Obsoletes:      %{name}-common < %{version}-%{release}
Obsoletes:      python3-%{name}-common < %{version}-%{release}

%description -n python3-%{name}-common
Common files for Extras Plugins for DNF, Python 3 version.

%package -n python2-%{name}-debug
Summary:        Debug Plugin for DNF
Requires:       python2-%{name}-common = %{version}-%{release}
%{?python_provide:%python_provide python2-%{name}-debug}

%description -n python2-%{name}-debug
Debug Plugin for DNF, Python 2 version. Writes system RPM configuration to a dump file
and restores it.

%package -n python3-%{name}-debug
Summary:	Debug Plugin for DNF
Requires:	python3-%{name}-common = %{version}-%{release}
%{?python_provide:%python_provide python3-%{name}-debug}
Provides:       dnf-command(debug-dump)
Provides:       dnf-command(debug-restore)
Provides:       %{name}-debug = %{version}-%{release}
Obsoletes:      %{name}-debug < %{version}-%{release}

%description -n python3-%{name}-debug
Debug Plugin for DNF, Python 3 version. Writes system RPM configuration to
a dump file and restores it.

%package -n python2-%{name}-leaves
Summary:        Leaves Plugin for DNF
Requires:       python2-%{name}-common = %{version}-%{release}
%{?python_provide:%python_provide python2-%{name}-leaves}

%description -n python2-%{name}-leaves
Leaves Plugin for DNF, Python 2 version. List all installed packages
not required by any other installed package.

%package -n python3-%{name}-leaves
Summary:        Leaves Plugin for DNF
Requires:       python3-%{name}-common = %{version}-%{release}
%{?python_provide:%python_provide python3-%{name}-leaves}
Provides:       dnf-command(leaves)
Provides:       %{name}-leaves = %{version}-%{release}
Obsoletes:      %{name}-leaves < %{version}-%{release}
Obsoletes:      %{name}-orphans < %{version}-%{release}

%description -n python3-%{name}-leaves
Leaves Plugin for DNF, Python 3 version. List all installed packages
not required by any other installed package.

%package -n python2-%{name}-local
Summary:        Local Plugin for DNF
Requires:       python2-%{name}-common = %{version}-%{release}
Requires:       /usr/bin/createrepo_c
%{?python_provide:%python_provide python2-%{name}-local}

%description -n python2-%{name}-local
Local Plugin for DNF, Python 2 version. Automatically copy all downloaded packages to a
repository on the local filesystem and generating repo metadata.

%package -n python3-%{name}-local
Summary:        Local Plugin for DNF
Requires:       python3-%{name}-common = %{version}-%{release}
Requires:       /usr/bin/createrepo_c
%{?python_provide:%python_provide python3-%{name}-local}
Provides:       %{name}-local = %{version}-%{release}
Obsoletes:      %{name}-local < %{version}-%{release}

%description -n python3-%{name}-local
Local Plugin for DNF, Python 3 version. Automatically copy all downloaded
packages to a repository on the local filesystem and generating repo metadata.

%package -n python2-%{name}-migrate
Summary:        Migrate Plugin for DNF
%{?python_provide:%python_provide python2-%{name}-migrate}
Requires:       python2-%{name}-common = %{version}-%{release}
Requires:       yum
Requires:       python2-dnf >= %{dnf_lowest_compatible}

%description -n python2-%{name}-migrate
Migrate Plugin for DNF, Python 2 version. Migrates history, group and
yumdb data from yum to dnf.

%package -n python2-%{name}-kickstart
Summary:        Kickstart Plugin for DNF
Requires:       python2-%{name}-common = %{version}-%{release}
%{?python_provide:%python_provide python2-%{name}-kickstart}
Conflicts:      python-dnf-plugins-core <= 0.1.12
BuildRequires:  python-kickstart
Requires:       python-kickstart

%description -n python2-%{name}-kickstart
Kickstart Plugin for DNF, Python 2 version. Install packages listed in a
Kickstart file.

%package -n python3-%{name}-kickstart
Summary:        Kickstart Plugin for DNF
Requires:       python3-%{name}-common = %{version}-%{release}
%{?python_provide:%python_provide python3-%{name}-kickstart}
BuildRequires:  python3-kickstart
Requires:       python3-kickstart
Conflicts:      python3-dnf-plugins-core <= 0.1.12
Provides:       dnf-command(kickstart)
Provides:       %{name}-kickstart = %{version}-%{release}

%description -n python3-%{name}-kickstart
Kickstart Plugin for DNF, Python 3 version. Install packages listed in a
Kickstart file.

%package -n python2-%{name}-repoclosure
Summary:        RepoClosure Plugin for DNF
Requires:       python2-%{name}-common = %{version}-%{release}
%{?python_provide:%python_provide python2-%{name}-repoclosure}

%description -n python2-%{name}-repoclosure
RepoClosure Plugin for DNF, Python 2 version. Display a list of unresolved dependencies for
repositories.

%package -n python3-%{name}-repoclosure
Summary:        RepoClosure Plugin for DNF
Requires:       python3-%{name}-common = %{version}-%{release}
%{?python_provide:%python_provide python3-%{name}-repoclosure}
Provides:       dnf-command(repoclosure)
Provides:       %{name}-repoclosure = %{version}-%{release}
Obsoletes:      %{name}-repoclosure < %{version}-%{release}

%description -n python3-%{name}-repoclosure
RepoClosure Plugin for DNF, Python 3 version. Display a list of unresolved
dependencies for repositories.

%package -n python2-%{name}-repograph
Summary:        RepoGraph Plugin for DNF
Requires:       python2-%{name}-common = %{version}-%{release}
%{?python_provide:%python_provide python2-%{name}-repograph}

%description -n python2-%{name}-repograph
RepoGraph Plugin for DNF, Python 2 version. Output a full package dependency graph in dot format.

%package -n python3-%{name}-repograph
Summary:        RepoGraph Plugin for DNF
Requires:       python3-%{name}-common = %{version}-%{release}
%{?python_provide:%python_provide python3-%{name}-repograph}
Provides:       dnf-command(repograph)
Provides:       %{name}-repograph = %{version}-%{release}
Obsoletes:      %{name}-repograph < %{version}-%{release}

%description -n python3-%{name}-repograph
RepoGraph Plugin for DNF, Python 3 version. Output a full package dependency
graph in dot format.

%package -n python2-%{name}-repomanage
Summary:        RepoManage Plugin for DNF
Requires:       python2-%{name}-common = %{version}-%{release}
%{?python_provide:%python_provide python2-%{name}-repomanage}

%description -n python2-%{name}-repomanage
RepoManage Plugin for DNF, Python 2 version. Manage a directory of rpm packages.

%package -n python3-%{name}-repomanage
Summary:        RepoManage Plugin for DNF
Requires:       python3-%{name}-common = %{version}-%{release}
%{?python_provide:%python_provide python3-%{name}-repomanage}
Provides:       dnf-command(repomanage)
Provides:       %{name}-repomanage = %{version}-%{release}
Obsoletes:      %{name}-repomanage < %{version}-%{release}

%description -n python3-%{name}-repomanage
RepoManage Plugin for DNF, Python 3 version. Manage a directory of rpm packages.

%package -n python3-%{name}-rpmconf
Summary:        RpmConf Plugin for DNF
BuildRequires:  python3-rpmconf
Requires:       python3-%{name}-common = %{version}-%{release}
%{?python_provide:%python_provide python3-%{name}-rpmconf}
Requires:       python3-rpmconf
Provides:       %{name}-rpmconf = %{version}-%{release}

%description -n python3-%{name}-rpmconf
RpmConf Plugin for DNF, Python 3 version. Handles .rpmnew, .rpmsave every
transaction.

%package -n python2-%{name}-show-leaves
Summary:        Leaves Plugin for DNF
Requires:       python2-%{name}-common = %{version}-%{release}
%{?python_provide:%python_provide python2-%{name}-show-leaves}
Requires:       python2-%{name}-leaves = %{version}-%{release}

%description -n python2-%{name}-show-leaves
Show-leaves Plugin for DNF, Python 2 version. List all installed
packages that are no longer required by any other installed package
after a transaction.

%package -n python3-%{name}-show-leaves
Summary:        Show-leaves Plugin for DNF
Requires:       python3-%{name}-common = %{version}-%{release}
%{?python_provide:%python_provide python3-%{name}-show-leaves}
Requires:       python3-%{name}-leaves = %{version}-%{release}
Provides:       %{name}-show-leaves = %{version}-%{release}
Obsoletes:      %{name}-show-leaves < %{version}-%{release}

%description -n python3-%{name}-show-leaves
Show-leaves Plugin for DNF, Python 3 version. List all installed
packages that are no longer required by any other installed package
after a transaction.

%package -n python2-%{name}-snapper
Summary:        Snapper Plugin for DNF
Requires:       python2-%{name}-common = %{version}-%{release}
%{?python_provide:%python_provide python2-%{name}-snapper}
Requires:       dbus-python
Requires:       snapper

%description -n python2-%{name}-snapper
Snapper Plugin for DNF, Python 2 version. Creates snapshot every transaction.

%package -n python3-%{name}-snapper
Summary:        Snapper Plugin for DNF
Requires:       python3-%{name}-common = %{version}-%{release}
%{?python_provide:%python_provide python3-%{name}-snapper}
Requires:       python3-dbus
Requires:       snapper
Provides:       %{name}-snapper = %{version}-%{release}
Obsoletes:      %{name}-snapper < %{version}-%{release}

%description -n python3-%{name}-snapper
Snapper Plugin for DNF, Python 3 version. Creates snapshot every transaction.

%package -n python2-%{name}-tracer
Summary:        Tracer Plugin for DNF
Requires:       python2-%{name}-common = %{version}-%{release}
%{?python_provide:%python_provide python2-%{name}-tracer}
Requires:       python2-tracer >= 0.6.12

%description -n python2-%{name}-tracer
Tracer Plugin for DNF, Python 2 version. Finds outdated running applications in your system
every transaction.

%package -n python3-%{name}-tracer
Summary:        Tracer Plugin for DNF
Requires:       python3-%{name}-common = %{version}-%{release}
%{?python_provide:%python_provide python3-%{name}-tracer}
Requires:       python3-tracer >= 0.6.12
Obsoletes:      dnf-plugin-tracer < 0.5.6-2
Provides:       dnf-plugin-tracer = 1:%{version}-%{release}
Provides:       %{name}-tracer = %{version}-%{release}
Obsoletes:      %{name}-tracer < %{version}-%{release}

%description -n python3-%{name}-tracer
Tracer Plugin for DNF, Python 3 version. Finds outdated running applications in
your system every transaction.

%package -n python2-%{name}-versionlock
Summary:        Version Lock Plugin for DNF
Requires:       python2-%{name}-common = %{version}-%{release}
%{?python_provide:%python_provide python2-%{name}-versionlock}

%description -n python2-%{name}-versionlock
Version lock plugin takes a set of name/versions for packages and excludes all other
versions of those packages. This allows you to e.g. protect packages from being
updated by newer versions.

%package -n python3-%{name}-versionlock
Summary:        Version Lock Plugin for DNF
Requires:       python3-%{name}-common = %{version}-%{release}
%{?python_provide:%python_provide python3-%{name}-versionlock}
Provides:       dnf-command(versionlock)
Provides:       dnf-plugin-versionlock = 1:%{version}-%{release}
Provides:       %{name}-versionlock = %{version}-%{release}

%description -n python3-%{name}-versionlock
Version lock plugin takes a set of name/versions for packages and excludes all other
versions of those packages. This allows you to e.g. protect packages from being
updated by newer versions.

%package -n python3-%{name}-torproxy
Summary:        Tor Proxy Plugin for DNF
Requires:       python3-%{name}-common = %{version}-%{release}
%{?python_provide:%python_provide python3-%{name}-torproxy}
Requires:       python3-pycurl
Provides:       %{name}-torproxy = %{version}-%{release}

%description -n python3-%{name}-torproxy
Tor proxy plugin forces DNF to use Tor to download packages. It makes sure that
Tor is working and avoids leaking the hostname by using the proper SOCKS5 interface.


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

mkdir -p %{buildroot}%{_unitdir}/system-update.target.wants/
pushd %{buildroot}%{_unitdir}/system-update.target.wants/
  ln -sr ../dnf-system-upgrade.service
popd

%find_lang %{name}

# no python2-torproxy
rm -rf %{buildroot}%{python2_sitelib}/dnf-plugins/torproxy.*

%check
PYTHONPATH="%{buildroot}%{python2_sitelib}:%{buildroot}%{python2_sitelib}/dnf-plugins/" nosetests-%{python2_version} -s tests/
PYTHONPATH="%{buildroot}%{python3_sitelib}:%{buildroot}%{python3_sitelib}/dnf-plugins/" nosetests-%{python3_version} -s tests/

%files -n %{name}-common-data -f %{name}.lang
%{_mandir}/man8/dnf.plugin.*
%license COPYING
%doc AUTHORS README.rst

%files -n python2-%{name}-common
%{python2_sitelib}/dnfpluginsextras/

%files -n python3-%{name}-common
%{python3_sitelib}/dnfpluginsextras/
%dir %{python3_sitelib}/dnf-plugins/__pycache__/

%files -n python2-%{name}-debug
%{python2_sitelib}/dnf-plugins/debug.*

%files -n python3-%{name}-debug
%{python3_sitelib}/dnf-plugins/debug.*
%{python3_sitelib}/dnf-plugins/__pycache__/debug.*

%files -n python2-%{name}-leaves
%{python2_sitelib}/dnf-plugins/leaves.*

%files -n python3-%{name}-leaves
%{python3_sitelib}/dnf-plugins/leaves.*
%{python3_sitelib}/dnf-plugins/__pycache__/leaves.*

%files -n python2-%{name}-local
%config %{_sysconfdir}/dnf/plugins/local.conf
%{python2_sitelib}/dnf-plugins/local.*

%files -n python3-%{name}-local
%config %{_sysconfdir}/dnf/plugins/local.conf
%{python3_sitelib}/dnf-plugins/local.*
%{python3_sitelib}/dnf-plugins/__pycache__/local.*

%files -n python2-%{name}-migrate
%{python2_sitelib}/dnf-plugins/migrate.*

%files -n python2-%{name}-kickstart
%{python2_sitelib}/dnf-plugins/kickstart.*

%files -n python3-%{name}-kickstart
%{python3_sitelib}/dnf-plugins/kickstart.*
%{python3_sitelib}/dnf-plugins/__pycache__/kickstart.*

%files -n python2-%{name}-repoclosure
%{python2_sitelib}/dnf-plugins/repoclosure.*

%files -n python3-%{name}-repoclosure
%{python3_sitelib}/dnf-plugins/repoclosure.*
%{python3_sitelib}/dnf-plugins/__pycache__/repoclosure.*

%files -n python2-%{name}-repograph
%{python2_sitelib}/dnf-plugins/repograph.*

%files -n python3-%{name}-repograph
%{python3_sitelib}/dnf-plugins/repograph.*
%{python3_sitelib}/dnf-plugins/__pycache__/repograph.*

%files -n python2-%{name}-repomanage
%{python2_sitelib}/dnf-plugins/repomanage.*

%files -n python3-%{name}-repomanage
%{python3_sitelib}/dnf-plugins/repomanage.*
%{python3_sitelib}/dnf-plugins/__pycache__/repomanage.*

%files -n python3-%{name}-rpmconf
%config %{_sysconfdir}/dnf/plugins/rpmconf.conf
%{python3_sitelib}/dnf-plugins/rpm_conf.*
%{python3_sitelib}/dnf-plugins/__pycache__/rpm_conf.*

%files -n python2-%{name}-show-leaves
%{python2_sitelib}/dnf-plugins/show_leaves.*

%files -n python3-%{name}-show-leaves
%{python3_sitelib}/dnf-plugins/show_leaves.*
%{python3_sitelib}/dnf-plugins/__pycache__/show_leaves.*

%files -n python2-%{name}-snapper
%{python2_sitelib}/dnf-plugins/snapper.*

%files -n python3-%{name}-snapper
%{python3_sitelib}/dnf-plugins/snapper.*
%{python3_sitelib}/dnf-plugins/__pycache__/snapper.*

%files -n python2-%{name}-tracer
%{python2_sitelib}/dnf-plugins/tracer.*

%files -n python3-%{name}-tracer
%{python3_sitelib}/dnf-plugins/tracer.*
%{python3_sitelib}/dnf-plugins/__pycache__/tracer.*

%files -n python2-%{name}-versionlock
%config %{_sysconfdir}/dnf/plugins/versionlock.conf
%config %{_sysconfdir}/dnf/plugins/versionlock.list
%{python2_sitelib}/dnf-plugins/versionlock.*

%files -n python3-%{name}-versionlock
%config %{_sysconfdir}/dnf/plugins/versionlock.conf
%config %{_sysconfdir}/dnf/plugins/versionlock.list
%{python3_sitelib}/dnf-plugins/versionlock.*
%{python3_sitelib}/dnf-plugins/__pycache__/versionlock.*

%files -n python3-%{name}-torproxy
%config %{_sysconfdir}/dnf/plugins/torproxy.conf
%{python3_sitelib}/dnf-plugins/torproxy.*
%{python3_sitelib}/dnf-plugins/__pycache__/torproxy.*


%changelog
