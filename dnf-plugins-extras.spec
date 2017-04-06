%{!?dnf_lowest_compatible: %global dnf_lowest_compatible 2.0}
%{!?dnf_not_compatible: %global dnf_not_compatible 3.0}
%global dnf_plugins_extara_obsolete 2.0.0

Name:           dnf-plugins-extras
Version:        2.0.0
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

%package -n python2-%{name}-common
Summary:        Common files for Extras Plugins for DNF
Requires:       python2-dnf >= %{dnf_lowest_compatible}
Requires:       python2-dnf < %{dnf_not_compatible}
%{?python_provide:%python_provide python2-%{name}-common}
Provides:       %{name}-common = %{version}-%{release}
Obsoletes:      %{name}-common < %{version}-%{release}
Obsoletes:      %{name} < %{version}-%{release}
Obsoletes:      %{name}-common-data < %{version}-%{release}
Conflicts:      python3-%{name}-common < %{version}-%{release}

%description -n python2-%{name}-common
Common files for Extras Plugins, Python 2 version.

%package -n python3-%{name}-common
Summary:        Common files for Extras Plugins for DNF
Requires:       python3-dnf >= %{dnf_lowest_compatible}
Requires:       python3-dnf < %{dnf_not_compatible}
%{?python_provide:%python_provide python3-%{name}-common}
Provides:       %{name}-common = %{version}-%{release}
Obsoletes:      %{name}-common < %{version}-%{release}
Obsoletes:      python3-%{name}-common < %{version}-%{release}
Obsoletes:      %{name} < %{version}-%{release}
Obsoletes:      %{name}-common-data < %{version}-%{release}
Conflicts:      python2-%{name}-common < %{version}-%{release}

%description -n python3-%{name}-common
Common files for Extras Plugins for DNF, Python 3 version.

%package -n python2-dnf-plugin-kickstart
Summary:        Kickstart Plugin for DNF
Requires:       python2-%{name}-common = %{version}-%{release}
%{?python_provide:%python_provide python2-%{name}-kickstart}
BuildRequires:  python-kickstart
Requires:       python-kickstart
Provides:       dnf-command(kickstart)
Provides:       %{name}-kickstart = %{version}-%{release}
Provides:       dnf-plugin-kickstart = %{version}-%{release}
Provides:       python2-%{name}-kickstart = %{version}-%{release}
Conflicts:      python3-dnf-plugin-kickstart < %{version}-%{release}
Obsoletes:      python2-%{name}-kickstart < %{dnf_plugins_extra_obsolete}

%description -n python2-dnf-plugin-kickstart
Kickstart Plugin for DNF, Python 2 version. Install packages listed in a
Kickstart file.

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

%package -n python2-dnf-plugin-snapper
Summary:        Snapper Plugin for DNF
Requires:       python2-%{name}-common = %{version}-%{release}
%{?python_provide:%python_provide python2-%{name}-snapper}
Requires:       dbus-python
Requires:       snapper
Provides:       %{name}-snapper = %{version}-%{release}
Provides:       dnf-plugin-snapper = %{version}-%{release}
Provides:       python2-%{name}-snapper = %{version}-%{release}
Conflicts:      python3-dnf-plugin-snapper < %{version}-%{release}
Obsoletes:      python2-%{name}-snapper < %{dnf_plugins_extra_obsolete}

%description -n python2-dnf-plugin-snapper
Snapper Plugin for DNF, Python 2 version. Creates snapshot every transaction.

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

%package -n python2-dnf-plugin-system-upgrade
Summary:        System Upgrade Plugin for DNF
Requires:       python-%{name}-common = %{version}-%{release}
Requires:       python2-systemd
%{?python_provide:%python_provide python2-%{name}-system-upgrade}
Provides:       dnf-command(system-upgrade)
Provides:       %{name}-system-upgrade = %{version}-%{release}
Provides:       system-upgrade = %{version}-%{release}
Provides:       dnf-plugin-system-upgrade = %{version}-%{release}
Provides:       python2-%{name}-system-upgrade = %{version}-%{release}
Obsoletes:      fedup < 0.9.4
Obsoletes:      dnf-plugin-system-upgrade < 0.10
Obsoletes:      python2-dnf-plugin-system-upgrade < %{dnf_plugins_extra_obsolete}
Obsoletes:      python2-%{name}-system-upgrade < %{dnf_plugins_extra_obsolete}
Conflicts:      python3-dnf-plugin-system-upgrade < %{version}-%{release}
BuildRequires:  pkgconfig(systemd)
BuildRequires:  systemd
BuildRequires:  python2-systemd
%{?system_requires}

%description -n python2-dnf-plugin-system-upgrade
System Upgrade Plugin for DNF, Python 2 version. Enables offline system upgrades
using the "dnf system-upgrade" command.

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
Obsoletes:      python3-dnf-plugin-system-upgrade < 0.10
Conflicts:      python2-dnf-plugin-system-upgrade < %{version}-%{release}
BuildRequires:  pkgconfig(systemd)
BuildRequires:  systemd
BuildRequires:  python3-systemd
%{?systemd_requires}

%description -n python3-dnf-plugin-system-upgrade
System Upgrade Plugin for DNF, Python 3 version. Enables offline system upgrades
using the "dnf system-upgrade" command.

%package -n python2-dnf-plugin-tracer
Summary:        Tracer Plugin for DNF
Requires:       python2-%{name}-common = %{version}-%{release}
%{?python_provide:%python_provide python2-%{name}-tracer}
Requires:       python2-tracer >= 0.6.12
Provides:       dnf-plugin-tracer = %{version}-%{release}
Provides:       %{name}-tracer = %{version}-%{release}
Provides:       python2-%{name}-tracer = %{version}-%{release}
Conflicts:      python3-dnf-plugin-tracer < %{version}-%{release}
Obsoletes:      python2-%{name}-tracer < %{dnf_plugins_extra_obsolete}

%description -n python2-dnf-plugin-tracer
Tracer Plugin for DNF, Python 2 version. Finds outdated running applications in your system
every transaction.

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

%check
PYTHONPATH="%{buildroot}%{python2_sitelib}:%{buildroot}%{python2_sitelib}/dnf-plugins/" nosetests-%{python2_version} -s tests/
PYTHONPATH="%{buildroot}%{python3_sitelib}:%{buildroot}%{python3_sitelib}/dnf-plugins/" nosetests-%{python3_version} -s tests/

%files -n python2-%{name}-common -f %{name}.lang
%{python2_sitelib}/dnfpluginsextras/
%license COPYING
%doc AUTHORS README.rst

%files -n python3-%{name}-common -f %{name}.lang
%{python3_sitelib}/dnfpluginsextras/
%dir %{python3_sitelib}/dnf-plugins/__pycache__/
%license COPYING
%doc AUTHORS README.rst

%files -n python2-dnf-plugin-kickstart
%{python2_sitelib}/dnf-plugins/kickstart.*
%{_mandir}/man8/dnf.plugin.kickstart.*

%files -n python3-dnf-plugin-kickstart
%{python3_sitelib}/dnf-plugins/kickstart.*
%{python3_sitelib}/dnf-plugins/__pycache__/kickstart.*
%{_mandir}/man8/dnf.plugin.kickstart.*

%files -n python3-dnf-plugin-rpmconf
%config(noreplace) %{_sysconfdir}/dnf/plugins/rpmconf.conf
%{python3_sitelib}/dnf-plugins/rpm_conf.*
%{python3_sitelib}/dnf-plugins/__pycache__/rpm_conf.*
%{_mandir}/man8/dnf.plugin.rpmconf.*

%files -n python2-dnf-plugin-snapper
%{python2_sitelib}/dnf-plugins/snapper.*
%{_mandir}/man8/dnf.plugin.snapper.*

%files -n python3-dnf-plugin-snapper
%{python3_sitelib}/dnf-plugins/snapper.*
%{python3_sitelib}/dnf-plugins/__pycache__/snapper.*
%{_mandir}/man8/dnf.plugin.snapper.*

%files -n python2-dnf-plugin-system-upgrade
%{_unitdir}/dnf-system-upgrade.service
%{_unitdir}/system-update.target.wants/dnf-system-upgrade.service
%{python2_sitelib}/dnf-plugins/system_upgrade.*
%{_mandir}/man8/dnf.plugin.system-upgrade.*

%files -n python3-dnf-plugin-system-upgrade
%{_unitdir}/dnf-system-upgrade.service
%{_unitdir}/system-update.target.wants/dnf-system-upgrade.service
%{python3_sitelib}/dnf-plugins/system_upgrade.py
%{python3_sitelib}/dnf-plugins/__pycache__/system_upgrade.*
%{_mandir}/man8/dnf.plugin.system-upgrade.*

%files -n python2-dnf-plugin-tracer
%{python2_sitelib}/dnf-plugins/tracer.*
%{_mandir}/man8/dnf.plugin.tracer.*

%files -n python3-dnf-plugin-tracer
%{python3_sitelib}/dnf-plugins/tracer.*
%{python3_sitelib}/dnf-plugins/__pycache__/tracer.*
%{_mandir}/man8/dnf.plugin.tracer.*

%files -n python3-dnf-plugin-torproxy
%config(noreplace) %{_sysconfdir}/dnf/plugins/torproxy.conf
%{python3_sitelib}/dnf-plugins/torproxy.*
%{python3_sitelib}/dnf-plugins/__pycache__/torproxy.*
%{_mandir}/man8/dnf.plugin.torproxy.*

%changelog
