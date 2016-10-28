%{!?dnf_lowest_compatible: %global dnf_lowest_compatible 2.0}
%{!?dnf_not_compatible: %global dnf_not_compatible 3.0}

Name:           dnf-plugins-extras
Version:        0.10
Release:        1%{?dist}
Summary:        Extras Plugins for DNF
License:        GPLv2+
URL:            https://github.com/rpm-software-management/%{name}
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  cmake
BuildRequires:  gettext

BuildRequires:  python2-devel
BuildRequires:  python2-dnf >= %{dnf_lowest_compatible}
BuildRequires:  python2-dnf < %{dnf_not_compatible}
BuildRequires:  python2-nose
BuildRequires:  python2-sphinx

BuildRequires:  python3-devel
BuildRequires:  python3-dnf >= %{dnf_lowest_compatible}
BuildRequires:  python3-dnf < %{dnf_not_compatible}
BuildRequires:  python3-nose
BuildRequires:  python3-sphinx

%description
%{summary}.

%package common
Summary:        Common files for %{name} subpackages
Obsoletes:      %{name} < 0.10

%description common
%{summary}.

%package -n python2-%{name}-common
Summary:        Common files for python2-%{name} subpackages
%{?python_provide:%python_provide python2-%{name}-common}
Requires:       python2-dnf >= %{dnf_lowest_compatible}
Requires:       python2-dnf < %{dnf_not_compatible}

%description -n python2-%{name}-common
%{summary}.

%package -n python3-%{name}-common
Summary:        Common files for python3-%{name} subpackages
%{?python_provide:%python_provide python3-%{name}-common}
Requires:       python3-dnf >= %{dnf_lowest_compatible}
Requires:       python3-dnf < %{dnf_not_compatible}

%description -n python3-%{name}-common
%{summary}.


%package -n python2-%{name}-debug
Summary:        Debug Plugin for DNF
Requires:       python2-%{name}-common = %{?epoch:%{epoch}:}%{version}-%{release}
%{?python_provide:%python_provide python2-%{name}-debug}

%description -n python2-%{name}-debug
Debug Plugin for DNF. Writes system RPM configuration to a dump file and restores
it.

%package -n python3-%{name}-debug
Summary:        Debug Plugin for DNF
Requires:       python3-%{name}-common = %{?epoch:%{?epoch}:}%{version}-%{release}
%{?python_provide:%python_provide python3-%{name}-debug}
Provides:       dnf-command(debug-dump)
Provides:       dnf-command(debug-restore)
Provides:       %{name}-debug = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n python3-%{name}-debug
Debug Plugin for DNF. Writes system RPM configuration to a dump file and restores
it.


%package -n python2-%{name}-leaves
Summary:        Leaves Plugin for DNF
Requires:       python2-%{name}-common = %{?epoch:%{?epoch}:}%{version}-%{release}
%{?python_provide:%python_provide python2-%{name}-leaves}

%description -n python2-%{name}-leaves
Leaves Plugin for DNF. List all installed packages not required by any other
installed package.

%package -n python3-%{name}-leaves
Summary:        Leaves Plugin for DNF
Requires:       python3-%{name}-common = %{?epoch:%{?epoch}:}%{version}-%{release}
%{?python_provide:%python_provide python3-%{name}-leaves}
Provides:       dnf-command(leaves)
Provides:       %{name}-leaves = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n python3-%{name}-leaves
Leaves Plugin for DNF. List all installed packages not required by any other
installed package.


%package -n python2-%{name}-local
Summary:        Local Plugin for DNF
Requires:       /usr/bin/createrepo_c
Requires:       python2-%{name}-common = %{?epoch:%{?epoch}:}%{version}-%{release}
%{?python_provide:%python_provide python2-%{name}-local}


%description -n python2-%{name}-local
Local Plugin for DNF Automatically copy all downloaded packages to a repository
on the local filesystem and generating repo metadata.

%package -n python3-%{name}-local
Summary:        Local Plugin for DNF
Requires:       /usr/bin/createrepo_c
Requires:       python3-%{name}-common = %{?epoch:%{?epoch}:}%{version}-%{release}
%{?python_provide:%python_provide python3-%{name}-local}
Provides:       dnf-command(local)
Provides:       %{name}-local = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n python3-%{name}-local
Local Plugin for DNF. Automatically copy all downloaded packages to a repository
on the local filesystem and generating repo metadata.


%package -n python2-%{name}-migrate
Summary:        Migrate Plugin for DNF
Requires:       yum
Requires:       python2-%{name}-common = %{?epoch:%{?epoch}:}%{version}-%{release}
%{?python_provide:%python_provide python2-%{name}-migrate}

%description -n python2-%{name}-migrate
Migrate Plugin for DNF. Migrates yum's history, group and yumdb data to dnf.


%package -n python2-%{name}-kickstart
Summary:        Kickstart Plugin for DNF
Requires:       python2-%{name}-common = %{?epoch:%{?epoch}:}%{version}-%{release}
%{?python_provide:%python_provide python2-%{name}-kickstart}

BuildRequires:	python-kickstart

%description -n python2-%{name}-kickstart
Kickstart Plugin for DNF. Install packages listed in a Kickstart file.

%package -n python3-%{name}-kickstart
Summary:        Kickstart Plugin for DNF
Requires:       python3-%{name}-common = %{?epoch:%{?epoch}:}%{version}-%{release}
%{?python_provide:%python_provide python3-%{name}-kickstart}
Requires:       python3-kickstart
Provides:       dnf-command(kickstart)
Provides:       %{name}-kickstart = %{?epoch:%{epoch}:}%{version}-%{release}

BuildRequires:	python3-kickstart

%description -n python3-%{name}-kickstart
Kickstart Plugin for DNF. Install packages listed in a Kickstart file.


%package -n python2-%{name}-repoclosure
Summary:        Repoclosure Plugin for DNF
Requires:       python2-%{name}-common = %{?epoch:%{?epoch}:}%{version}-%{release}
%{?python_provide:%python_provide python2-%{name}-repoclosure}

%description -n python2-%{name}-repoclosure
Repoclosure Plugin for DNF. Display a list of unresolved dependencies for
repositories.

%package -n python3-%{name}-repoclosure
Summary:        Repoclosure Plugin for DNF
Requires:       python3-%{name}-common = %{?epoch:%{?epoch}:}%{version}-%{release}
%{?python_provide:%python_provide python3-%{name}-repoclosure}
Provides:       dnf-command(repoclosure)
Provides:       %{name}-repoclosure = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n python3-%{name}-repoclosure
Repoclosure Plugin for DNF. Display a list of unresolved dependencies for
repositories.


%package -n python2-%{name}-repograph
Summary:        Repograph Plugin for DNF
Requires:       python2-%{name}-common = %{?epoch:%{?epoch}:}%{version}-%{release}
%{?python_provide:%python_provide python2-%{name}-repograph}

%description -n python2-%{name}-repograph
Repograph Plugin for DNF. Output a full package dependency graph in dot format.

%package -n python3-%{name}-repograph
Summary:        Repograph Plugin for DNF
Requires:       python3-%{name}-common = %{?epoch:%{?epoch}:}%{version}-%{release}
%{?python_provide:%python_provide python3-%{name}-repograph}
Provides:       dnf-command(repograph)
Provides:       %{name}-repograph = %{?epoch:%{epoch}:}%{version}-%{release}
%description -n python3-%{name}-repograph
Repograph Plugin for DNF. Output a full package dependency graph in dot format.


%package -n python2-%{name}-repomanage
Summary:        Repomanage Plugin for DNF
Requires:       python2-%{name}-common = %{?epoch:%{?epoch}:}%{version}-%{release}
%{?python_provide:%python_provide python2-%{name}-repomanage}

%description -n python2-%{name}-repomanage
Repomanage Plugin for DNF. Manage a directory of rpm packages.

%package -n python3-%{name}-repomanage
Summary:        Repomanage Plugin for DNF
Requires:       python3-%{name}-common = %{?epoch:%{?epoch}:}%{version}-%{release}
%{?python_provide:%python_provide python3-%{name}-repomanage}
Provides:       dnf-command(repomanage)
Provides:       %{name}-repomanage = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n python3-%{name}-repomanage
Repomanage Plugin for DNF. Manage a directory of rpm packages.


%package -n python3-%{name}-rpmconf
Summary:        RpmConf Plugin for DNF
Requires:       python3-%{name}-common = %{?epoch:%{?epoch}:}%{version}-%{release}
Requires:	python3-rpmconf
%{?python_provide:%python_provide python3-%{name}-rpmconf}
Provides:       dnf-command(rpmconf)
Provides:       %{name}-rpmconf = %{?epoch:%{epoch}:}%{version}-%{release}

BuildRequires:  python3-rpmconf

%description -n python3-%{name}-rpmconf
RpmConf Plugin for DNF. Handles .rpmnew, .rpmsave every transaction.


%package -n python2-%{name}-show-leaves
Summary:        Leaves Plugin for DNF
Requires:       python2-%{name}-common = %{?epoch:%{?epoch}:}%{version}-%{release}
Requires:       python2-%{name}-leaves = %{?epoch:%{?epoch}:}%{version}-%{release}
%{?python_provide:%python_provide python2-%{name}-show-leaves}

%description -n python2-%{name}-show-leaves
Leaves Plugin for DNF. List all installed packages that are no longer required by
any other installed package after a transaction.

%package -n python3-%{name}-show-leaves
Summary:        Leaves Plugin for DNF
Requires:       python3-%{name}-common = %{?epoch:%{?epoch}:}%{version}-%{release}
Requires:       python3-%{name}-leaves = %{?epoch:%{?epoch}:}%{version}-%{release}
%{?python_provide:%python_provide python3-%{name}-show-leaves}
Provides:       dnf-command(show-leaves)
Provides:       %{name}-show-leaves = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n python3-%{name}-show-leaves
Leaves Plugin for DNF. List all installed packages that are no longer required by
any other installed package after a transaction.


%package -n python2-%{name}-snapper
Summary:        Repomanage Plugin for DNF
Requires:       python2-%{name}-common = %{?epoch:%{?epoch}:}%{version}-%{release}
Requires:       dbus-python
Requires:       snapper
%{?python_provide:%python_provide python2-%{name}-snapper}

%description -n python2-%{name}-snapper
Repomanage Plugin for DNF. Creates snapshot every transaction.

%package -n python3-%{name}-snapper
Summary:        Repomanage Plugin for DNF
Requires:       python3-%{name}-common = %{?epoch:%{?epoch}:}%{version}-%{release}
Requires:       python3-dbus
Requires:       snapper
%{?python_provide:%python_provide python3-%{name}-snapper}
Provides:       dnf-command(snapper)
Provides:       %{name}-snapper = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n python3-%{name}-snapper
Repomanage Plugin for DNF. Creates snapshot every transaction.


%package -n python2-%{name}-tracer
Summary:        Tracer Plugin for DNF
Requires:       python2-%{name}-common = %{?epoch:%{?epoch}:}%{version}-%{release}
Requires:       python2-tracer > 0.6.11
%{?python_provide:%python_provide python2-%{name}-tracer}

%description -n python2-%{name}-tracer
Tracer Plugin for DNF. Finds outdated running applications in your system every
transaction.

%package -n python3-%{name}-tracer
Summary:        Tracer Plugin for DNF
Requires:       python3-%{name}-common = %{?epoch:%{?epoch}:}%{version}-%{release}
Requires:       python3-tracer > 0.6.11
%{?python_provide:%python_provide python3-%{name}-tracer}
Provides:       %{name}-tracer = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n python3-%{name}-tracer
Tracer Plugin for DNF. Finds outdated running applications in your system every
transaction.


%package -n python2-%{name}-versionlock
Summary:        Versionlock Plugin for DNF
Requires:       python2-%{name}-common = %{?epoch:%{?epoch}:}%{version}-%{release}
%{?python_provide:%python_provide python2-%{name}-versionlock}

%description -n python2-%{name}-versionlock
Versionlock Plugin for DNF. Versionlock plugin takes a set of name/versions for
packages and excludes all other versions of those packages. This allows you to
e.g. protect packages from being updated by newer versions.

%package -n python3-%{name}-versionlock
Summary:        Versionlock Plugin for DNF
Requires:       python3-%{name}-common = %{?epoch:%{?epoch}:}%{version}-%{release}
%{?python_provide:%python_provide python3-%{name}-versionlock}
Provides:       dnf-command(versionlock)
Provides:       %{name}-versionlock = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n python3-%{name}-versionlock
Versionlock Plugin for DNF. Versionlock plugin takes a set of name/versions for
packages and excludes all other versions of those packages. This allows you to
e.g. protect packages from being updated by newer versions.


%package -n python3-%{name}-torproxy
Summary:        Torproxy Plugin for DNF
Requires:       python3-%{name}-common = %{?epoch:%{?epoch}:}%{version}-%{release}
%{?python_provide:%python_provide python3-%{name}-torproxy}
Provides:       dnf-command(torproxy)
Provides:       %{name}-torproxy = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       python3-pycurl

%description -n python3-%{name}-torproxy
Torproxy Plugin for DNF. This plugin force dnf to use tor to download packages.
It make sure that tor is working and avoid leaking hostname by using the proper
sock5 interface.


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

# no python2-torproxy
rm -rf %{buildroot}%{python2_sitelib}/dnf-plugins/torproxy.*

%find_lang %{name}

%check
PYTHONPATH="%{buildroot}%{python2_sitelib}:%{buildroot}%{python2_sitelib}/dnf-plugins/" nosetests-%{python2_version} -s tests/
PYTHONPATH="%{buildroot}%{python3_sitelib}:%{buildroot}%{python3_sitelib}/dnf-plugins/" nosetests-%{python3_version} -s tests/

%files common -f %{name}.lang
%license COPYING
%doc README.rst
%{_mandir}/man8/dnf.plugin.*

%files -n python2-%{name}-common
%{python2_sitelib}/dnfpluginsextras/

%files -n python3-%{name}-common
%{python3_sitelib}/dnfpluginsextras/

%files -n python2-%{name}-debug
%{python2_sitelib}/dnf-plugins/debug.*

%files -n python3-%{name}-debug
%{python3_sitelib}/dnf-plugins/debug.py
%{python3_sitelib}/dnf-plugins/__pycache__/debug.*

%files -n python2-%{name}-leaves
%{python2_sitelib}/dnf-plugins/leaves.*

%files -n python3-%{name}-leaves
%{python3_sitelib}/dnf-plugins/leaves.py
%{python3_sitelib}/dnf-plugins/__pycache__/leaves.*

%files -n python2-%{name}-local
%config %{_sysconfdir}/dnf/plugins/local.conf
%{python2_sitelib}/dnf-plugins/local.*

%files -n python3-%{name}-local
%config %{_sysconfdir}/dnf/plugins/local.conf
%{python3_sitelib}/dnf-plugins/local.py
%{python3_sitelib}/dnf-plugins/__pycache__/local.*

%files -n python2-%{name}-migrate
%{python2_sitelib}/dnf-plugins/migrate.*

%files -n python2-%{name}-kickstart
%{python2_sitelib}/dnf-plugins/kickstart.py*

%files -n python3-%{name}-kickstart
%{python3_sitelib}/dnf-plugins/kickstart.py
%{python3_sitelib}/dnf-plugins/__pycache__/kickstart.*

%files -n python2-%{name}-repoclosure
%{python2_sitelib}/dnf-plugins/repoclosure.*

%files -n python3-%{name}-repoclosure
%{python3_sitelib}/dnf-plugins/repoclosure.py
%{python3_sitelib}/dnf-plugins/__pycache__/repoclosure.*

%files -n python2-%{name}-repograph
%{python2_sitelib}/dnf-plugins/repograph.*

%files -n python3-%{name}-repograph
%{python3_sitelib}/dnf-plugins/repograph.py
%{python3_sitelib}/dnf-plugins/__pycache__/repograph.*

%files -n python2-%{name}-repomanage
%{python2_sitelib}/dnf-plugins/repomanage.*

%files -n python3-%{name}-repomanage
%{python3_sitelib}/dnf-plugins/repomanage.py
%{python3_sitelib}/dnf-plugins/__pycache__/repomanage.*

%files -n python3-%{name}-rpmconf
%config(noreplace) %{_sysconfdir}/dnf/plugins/rpmconf.conf
%{python3_sitelib}/dnf-plugins/rpm_conf.py
%{python3_sitelib}/dnf-plugins/__pycache__/rpm_conf.*

%files -n python2-%{name}-show-leaves
%{python2_sitelib}/dnf-plugins/show_leaves.*

%files -n python3-%{name}-show-leaves
%{python3_sitelib}/dnf-plugins/show_leaves.py
%{python3_sitelib}/dnf-plugins/__pycache__/show_leaves.*

%files -n python2-%{name}-snapper
%{python2_sitelib}/dnf-plugins/snapper.*

%files -n python3-%{name}-snapper
%{python3_sitelib}/dnf-plugins/snapper.py
%{python3_sitelib}/dnf-plugins/__pycache__/snapper.*

%files -n python2-%{name}-tracer
%{python2_sitelib}/dnf-plugins/tracer.*

%files -n python3-%{name}-tracer
%{python3_sitelib}/dnf-plugins/tracer.py
%{python3_sitelib}/dnf-plugins/__pycache__/tracer.*

%files -n python2-%{name}-versionlock
%config(noreplace) %{_sysconfdir}/dnf/plugins/versionlock.conf
%config(noreplace) %{_sysconfdir}/dnf/plugins/versionlock.list
%{python2_sitelib}/dnf-plugins/versionlock.*

%files -n python3-%{name}-versionlock
%config(noreplace) %{_sysconfdir}/dnf/plugins/versionlock.conf
%config(noreplace) %{_sysconfdir}/dnf/plugins/versionlock.list
%{python3_sitelib}/dnf-plugins/versionlock.py
%{python3_sitelib}/dnf-plugins/__pycache__/versionlock.*

%files -n python3-%{name}-torproxy
%config(noreplace) %{_sysconfdir}/dnf/plugins/torproxy.conf
%{python3_sitelib}/dnf-plugins/torproxy.*
%{python3_sitelib}/dnf-plugins/__pycache__/torproxy.*

%changelog
