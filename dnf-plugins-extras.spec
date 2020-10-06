%{!?dnf_lowest_compatible: %global dnf_lowest_compatible 4.2.19}
%global dnf_plugins_extra_obsolete 2.0.0

%undefine __cmake_in_source_build

Name:           dnf-plugins-extras
Version:        4.0.11
Release:        1%{?dist}
Summary:        Extras Plugins for DNF
License:        GPLv2+
URL:            https://github.com/rpm-software-management/%{name}
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  cmake
BuildRequires:  gettext
BuildRequires:  python3-devel
BuildRequires:  python3-dnf >= %{dnf_lowest_compatible}
BuildRequires:  python3-nose
BuildRequires:  python3-sphinx

%description
Extras Plugins for DNF.

%package -n python3-%{name}-common
Summary:        Common files for Extras Plugins for DNF
Requires:       python3-dnf >= %{dnf_lowest_compatible}
%{?python_provide:%python_provide python3-%{name}-common}
Provides:       %{name}-common = %{version}-%{release}
Obsoletes:      %{name}-common < %{version}-%{release}
Obsoletes:      python3-%{name}-common < %{version}-%{release}
Obsoletes:      %{name} < %{version}-%{release}
Obsoletes:      %{name}-common-data < %{version}-%{release}

%description -n python3-%{name}-common
Common files for Extras Plugins for DNF.

%package -n python3-dnf-plugin-kickstart
Summary:        Kickstart Plugin for DNF
Requires:       python3-%{name}-common = %{version}-%{release}
%{?python_provide:%python_provide python3-%{name}-kickstart}
BuildRequires:  python3-kickstart
Requires:       python3-kickstart
Provides:       dnf-command(kickstart)
Provides:       %{name}-kickstart = %{version}-%{release}
Provides:       dnf-plugin-kickstart = %{version}-%{release}
Provides:       python3-%{name}-kickstart = %{version}-%{release}
Conflicts:      python2-dnf-plugin-kickstart < %{version}-%{release}
Obsoletes:      python3-%{name}-kickstart < %{dnf_plugins_extra_obsolete}

%description -n python3-dnf-plugin-kickstart
Kickstart Plugin for DNF, Python 3 version. Install packages listed in a
Kickstart file.

%package -n python3-dnf-plugin-rpmconf
Summary:        RpmConf Plugin for DNF
BuildRequires:  python3-rpmconf
Requires:       python3-%{name}-common = %{version}-%{release}
%{?python_provide:%python_provide python3-%{name}-rpmconf}
Requires:       python3-rpmconf
Provides:       %{name}-rpmconf = %{version}-%{release}
Provides:       dnf-plugin-rpmconf = %{version}-%{release}
Provides:       python3-%{name}-rpmconf = %{version}-%{release}
Obsoletes:      python3-%{name}-rpmconf < %{dnf_plugins_extra_obsolete}

%description -n python3-dnf-plugin-rpmconf
RpmConf Plugin for DNF, Python 3 version. Handles .rpmnew, .rpmsave every
transaction.

%package -n python3-dnf-plugin-snapper
Summary:        Snapper Plugin for DNF
Requires:       python3-%{name}-common = %{version}-%{release}
%{?python_provide:%python_provide python3-%{name}-snapper}
Requires:       python3-dbus
Requires:       snapper
Provides:       %{name}-snapper = %{version}-%{release}
Provides:       dnf-plugin-snapper = %{version}-%{release}
Provides:       python3-%{name}-snapper = %{version}-%{release}
Conflicts:      python2-dnf-plugin-snapper < %{version}-%{release}
Obsoletes:      python3-%{name}-snapper < %{dnf_plugins_extra_obsolete}

%description -n python3-dnf-plugin-snapper
Snapper Plugin for DNF, Python 3 version. Creates snapshot every transaction.

%package -n python3-dnf-plugin-system-upgrade
Summary:        System Upgrade Plugin for DNF
Requires:       python3-%{name}-common = %{version}-%{release}
Requires:       python3-systemd
%{?python_provide:%python_provide python3-%{name}-system-upgrade}
Provides:       dnf-command(system-upgrade)
Provides:       %{name}-system-upgrade = %{version}-%{release}
Provides:       system-upgrade = %{version}-%{release}
Provides:       dnf-plugin-system-upgrade = %{version}-%{release}
Provides:       python3-%{name}-system-upgrade = %{version}-%{release}
Obsoletes:      python3-%{name}-system-upgrade < %{dnf_plugins_extra_obsolete}
Obsoletes:      fedup < 0.9.4
Obsoletes:      dnf-plugin-system-upgrade < 0.10
Conflicts:      python2-dnf-plugin-system-upgrade < %{version}-%{release}
BuildRequires:  pkgconfig(systemd)
BuildRequires:  systemd
BuildRequires:  python3-systemd
%{?systemd_requires}

%description -n python3-dnf-plugin-system-upgrade
System Upgrade Plugin for DNF, Python 3 version. Enables offline system upgrades
using the "dnf system-upgrade" command.

%package -n python3-dnf-plugin-tracer
Summary:        Tracer Plugin for DNF
Requires:       python3-%{name}-common = %{version}-%{release}
%{?python_provide:%python_provide python3-%{name}-tracer}
Requires:       python3-tracer >= 0.6.12
Provides:       dnf-plugin-tracer = %{version}-%{release}
Provides:       %{name}-tracer = %{version}-%{release}
Provides:       python3-%{name}-tracer = %{version}-%{release}
Conflicts:      python2-dnf-plugin-tracer < %{version}-%{release}
Obsoletes:      python3-%{name}-tracer < %{dnf_plugins_extra_obsolete}

%description -n python3-dnf-plugin-tracer
Tracer Plugin for DNF, Python 3 version. Finds outdated running applications in
your system every transaction.

%package -n python3-dnf-plugin-torproxy
Summary:        Tor Proxy Plugin for DNF
Requires:       python3-%{name}-common = %{version}-%{release}
%{?python_provide:%python_provide python3-%{name}-torproxy}
Requires:       python3-pycurl
Provides:       dnf-plugin-torproxy = %{version}-%{release}
Provides:       %{name}-torproxy = %{version}-%{release}
Provides:       python3-%{name}-torproxy = %{version}-%{release}
Obsoletes:      python3-%{name}-torproxy < %{dnf_plugins_extra_obsolete}

%description -n python3-dnf-plugin-torproxy
Tor proxy plugin forces DNF to use Tor to download packages. It makes sure that
Tor is working and avoids leaking the hostname by using the proper SOCKS5 interface.

%package -n python3-dnf-plugin-showvars
Summary:        showvars Plugin for DNF
Requires:       python3-%{name}-common = %{version}-%{release}
%{?python_provide:%python_provide python3-%{name}-showvars}
Provides:       dnf-plugin-showvars = %{version}-%{release}
Provides:       python3-%{name}-showvars = %{version}-%{release}

%description -n python3-dnf-plugin-showvars
This plugin dumps the current value of any defined DNF variables.  For example
$releasever and $basearch.


%prep
%autosetup

%build
  %cmake -DPYTHON_DESIRED:FILEPATH=%{__python3}
  %cmake_build
  %cmake_build --target doc-man

%install
  %cmake_install

mkdir -p %{buildroot}%{_unitdir}/system-update.target.wants/
pushd %{buildroot}%{_unitdir}/system-update.target.wants/
  ln -sr ../dnf-system-upgrade.service
popd

%find_lang %{name}

%check
PYTHONPATH="%{buildroot}%{python3_sitelib}:%{buildroot}%{python3_sitelib}/dnf-plugins/" nosetests-%{python3_version} -s tests/

%files -n python3-%{name}-common -f %{name}.lang
%{python3_sitelib}/dnfpluginsextras/
%dir %{python3_sitelib}/dnf-plugins/__pycache__/
%license COPYING
%doc AUTHORS README.rst

%files -n python3-dnf-plugin-kickstart
%{python3_sitelib}/dnf-plugins/kickstart.*
%{python3_sitelib}/dnf-plugins/__pycache__/kickstart.*
%{_mandir}/man8/dnf-kickstart.*

%files -n python3-dnf-plugin-rpmconf
%config(noreplace) %{_sysconfdir}/dnf/plugins/rpmconf.conf
%{python3_sitelib}/dnf-plugins/rpm_conf.*
%{python3_sitelib}/dnf-plugins/__pycache__/rpm_conf.*
%{_mandir}/man8/dnf-rpmconf.*

%files -n python3-dnf-plugin-snapper
%{python3_sitelib}/dnf-plugins/snapper.*
%{python3_sitelib}/dnf-plugins/__pycache__/snapper.*
%{_mandir}/man8/dnf-snapper.*

%files -n python3-dnf-plugin-system-upgrade
%{_unitdir}/dnf-system-upgrade.service
%{_unitdir}/dnf-system-upgrade-cleanup.service
%{_unitdir}/system-update.target.wants/dnf-system-upgrade.service
%{python3_sitelib}/dnf-plugins/system_upgrade.py
%{python3_sitelib}/dnf-plugins/__pycache__/system_upgrade.*
%{_mandir}/man8/dnf-system-upgrade.*

%files -n python3-dnf-plugin-tracer
%{python3_sitelib}/dnf-plugins/tracer.*
%{python3_sitelib}/dnf-plugins/__pycache__/tracer.*
%{_mandir}/man8/dnf-tracer.*

%files -n python3-dnf-plugin-torproxy
%config(noreplace) %{_sysconfdir}/dnf/plugins/torproxy.conf
%{python3_sitelib}/dnf-plugins/torproxy.*
%{python3_sitelib}/dnf-plugins/__pycache__/torproxy.*
%{_mandir}/man8/dnf-torproxy.*

%files -n python3-dnf-plugin-showvars
%{python3_sitelib}/dnf-plugins/showvars.*
%{python3_sitelib}/dnf-plugins/__pycache__/showvars.*
%{_mandir}/man8/dnf-showvars.*

%changelog
