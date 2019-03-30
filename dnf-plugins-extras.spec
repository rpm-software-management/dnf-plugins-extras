%{!?dnf_lowest_compatible: %global dnf_lowest_compatible 4.2.1}
%global dnf_plugins_extra_obsolete 2.0.0

%if 0%{?rhel} > 7 || 0%{?fedora} > 29
%bcond_with python2
%else
%bcond_without python2
%endif

%if 0%{?rhel} && 0%{?rhel} <= 7
%bcond_with python3
%else
%bcond_without python3
%endif

Name:           dnf-plugins-extras
Version:        4.0.4
Release:        1%{?dist}
Summary:        Extras Plugins for DNF
License:        GPLv2+
URL:            https://github.com/rpm-software-management/%{name}
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  cmake
BuildRequires:  gettext
%if %{with python2}
# py2
BuildRequires:  python2-devel
BuildRequires:  python2-dnf >= %{dnf_lowest_compatible}
BuildRequires:  python2-hypothesis
BuildRequires:  python2-nose
BuildRequires:  python2-sphinx
%endif
%if %{with python3}
# py3
BuildRequires:  python3-devel
BuildRequires:  python3-dnf >= %{dnf_lowest_compatible}
BuildRequires:  python3-hypothesis
BuildRequires:  python3-nose
BuildRequires:  python3-sphinx
%endif

%description
Extras Plugins for DNF.

%if %{with python2}
%package -n python2-%{name}-common
Summary:        Common files for Extras Plugins for DNF
Requires:       python2-dnf >= %{dnf_lowest_compatible}
%{?python_provide:%python_provide python2-%{name}-common}
Provides:       %{name}-common = %{version}-%{release}
Obsoletes:      %{name}-common < %{version}-%{release}
Obsoletes:      %{name} < %{version}-%{release}
Obsoletes:      %{name}-common-data < %{version}-%{release}
Conflicts:      python3-%{name}-common < %{version}-%{release}

%description -n python2-%{name}-common
Common files for Extras Plugins, Python 2 version.
%endif

%if %{with python3}
%package -n python3-%{name}-common
Summary:        Common files for Extras Plugins for DNF
Requires:       python3-dnf >= %{dnf_lowest_compatible}
%{?python_provide:%python_provide python3-%{name}-common}
Provides:       %{name}-common = %{version}-%{release}
Obsoletes:      %{name}-common < %{version}-%{release}
Obsoletes:      python3-%{name}-common < %{version}-%{release}
Obsoletes:      %{name} < %{version}-%{release}
Obsoletes:      %{name}-common-data < %{version}-%{release}
Conflicts:      python2-%{name}-common < %{version}-%{release}

%description -n python3-%{name}-common
Common files for Extras Plugins for DNF, Python 3 version.
%endif

%if %{with python2}
%package -n python2-dnf-plugin-kickstart
Summary:        Kickstart Plugin for DNF
Requires:       python2-%{name}-common = %{version}-%{release}
%{?python_provide:%python_provide python2-%{name}-kickstart}
%if (0%{?fedora} && 0%{?fedora} <= 27) || (0%{?rhel} && 0%{?rhel} <= 7)
BuildRequires:  python-kickstart
Requires:       python-kickstart
%else
BuildRequires:  python2-kickstart
Requires:       python2-kickstart
%endif
%if !%{with python3}
Provides:       dnf-command(kickstart)
Provides:       %{name}-kickstart = %{version}-%{release}
Provides:       dnf-plugin-kickstart = %{version}-%{release}
%endif
Provides:       python2-%{name}-kickstart = %{version}-%{release}
Conflicts:      python3-dnf-plugin-kickstart < %{version}-%{release}
Obsoletes:      python2-%{name}-kickstart < %{dnf_plugins_extra_obsolete}

%description -n python2-dnf-plugin-kickstart
Kickstart Plugin for DNF, Python 2 version. Install packages listed in a
Kickstart file.
%endif

%if %{with python3}
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
%endif

%if %{with python3}
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
%endif

%if %{with python2}
%package -n python2-dnf-plugin-snapper
Summary:        Snapper Plugin for DNF
Requires:       python2-%{name}-common = %{version}-%{release}
%{?python_provide:%python_provide python2-%{name}-snapper}
%if (0%{?fedora} && 0%{?fedora} <= 27) || (0%{?rhel} && 0%{?rhel} <= 7)
Requires:       dbus-python
%else
Requires:       python2-dbus
%endif
Requires:       snapper
%if !%{with python3}
Provides:       %{name}-snapper = %{version}-%{release}
Provides:       dnf-plugin-snapper = %{version}-%{release}
%endif
Provides:       python2-%{name}-snapper = %{version}-%{release}
Conflicts:      python3-dnf-plugin-snapper < %{version}-%{release}
Obsoletes:      python2-%{name}-snapper < %{dnf_plugins_extra_obsolete}

%description -n python2-dnf-plugin-snapper
Snapper Plugin for DNF, Python 2 version. Creates snapshot every transaction.
%endif

%if %{with python3}
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
%endif

%if %{with python2}
%package -n python2-dnf-plugin-system-upgrade
Summary:        System Upgrade Plugin for DNF
Requires:       python2-%{name}-common = %{version}-%{release}
Requires:       python2-systemd
%{?python_provide:%python_provide python2-%{name}-system-upgrade}
%if !%{with python3}
Provides:       dnf-command(system-upgrade)
Provides:       %{name}-system-upgrade = %{version}-%{release}
Provides:       system-upgrade = %{version}-%{release}
Provides:       dnf-plugin-system-upgrade = %{version}-%{release}
Obsoletes:      fedup < 0.9.4
Obsoletes:      dnf-plugin-system-upgrade < 0.10
%endif
Provides:       python2-%{name}-system-upgrade = %{version}-%{release}
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
%endif

%if %{with python3}
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
%endif

%if %{with python2}
%package -n python2-dnf-plugin-offline-upgrade
Summary:        System Upgrade Plugin for DNF
Requires:       python2-%{name}-common = %{version}-%{release}
Requires:       python2-systemd
%{?python_provide:%python_provide python2-%{name}-offline-upgrade}
%if !%{with python3}
Provides:       dnf-command(offline-upgrade)
Provides:       %{name}-offline-upgrade = %{version}-%{release}
Provides:       offline-upgrade = %{version}-%{release}
Provides:       dnf-plugin-offline-upgrade = %{version}-%{release}
Obsoletes:      dnf-plugin-offline-upgrade < 0.10
%endif
Provides:       python2-%{name}-offline-upgrade = %{version}-%{release}
Obsoletes:      python2-dnf-plugin-offline-upgrade < %{dnf_plugins_extra_obsolete}
Obsoletes:      python2-%{name}-offline-upgrade < %{dnf_plugins_extra_obsolete}
Conflicts:      python3-dnf-plugin-offline-upgrade < %{version}-%{release}
BuildRequires:  pkgconfig(systemd)
BuildRequires:  systemd
BuildRequires:  python2-systemd
%{?system_requires}

%description -n python2-dnf-plugin-offline-upgrade
System Upgrade Plugin for DNF, Python 2 version. Enables offline system upgrades
using the "dnf offline-upgrade" command.
%endif

%if %{with python3}
%package -n python3-dnf-plugin-offline-upgrade
Summary:        System Upgrade Plugin for DNF
Requires:       python3-%{name}-common = %{version}-%{release}
Requires:       python3-systemd
%{?python_provide:%python_provide python3-%{name}-offline-upgrade}
Provides:       dnf-command(offline-upgrade)
Provides:       %{name}-offline-upgrade = %{version}-%{release}
Provides:       offline-upgrade = %{version}-%{release}
Provides:       dnf-plugin-offline-upgrade = %{version}-%{release}
Provides:       python3-%{name}-offline-upgrade = %{version}-%{release}
Obsoletes:      python3-%{name}-offline-upgrade < %{dnf_plugins_extra_obsolete}
Obsoletes:      dnf-plugin-offline-upgrade < 0.10
Conflicts:      python2-dnf-plugin-offline-upgrade < %{version}-%{release}
BuildRequires:  pkgconfig(systemd)
BuildRequires:  systemd
BuildRequires:  python3-systemd
%{?systemd_requires}

%description -n python3-dnf-plugin-offline-upgrade
System Upgrade Plugin for DNF, Python 3 version. Enables offline system upgrades
using the "dnf offline-upgrade" command.
%endif

%if %{with python2}
%package -n python2-dnf-plugin-tracer
Summary:        Tracer Plugin for DNF
Requires:       python2-%{name}-common = %{version}-%{release}
%{?python_provide:%python_provide python2-%{name}-tracer}
Requires:       python2-tracer >= 0.6.12
%if !%{with python3}
Provides:       dnf-plugin-tracer = %{version}-%{release}
Provides:       %{name}-tracer = %{version}-%{release}
%endif
Provides:       python2-%{name}-tracer = %{version}-%{release}
Conflicts:      python3-dnf-plugin-tracer < %{version}-%{release}
Obsoletes:      python2-%{name}-tracer < %{dnf_plugins_extra_obsolete}

%description -n python2-dnf-plugin-tracer
Tracer Plugin for DNF, Python 2 version. Finds outdated running applications in your system
every transaction.
%endif

%if %{with python3}
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
%endif

%if %{with python3}
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
%endif

%if %{with python3}
%package -n python3-dnf-plugin-showvars
Summary:        showvars Plugin for DNF
Requires:       python3-%{name}-common = %{version}-%{release}
%{?python_provide:%python_provide python3-%{name}-showvars}
Provides:       dnf-plugin-showvars = %{version}-%{release}
Provides:       python3-%{name}-showvars = %{version}-%{release}

%description -n python3-dnf-plugin-showvars
This plugin dumps the current value of any defined DNF variables.  For example
$releasever and $basearch.
%endif


%prep
%autosetup
sed -ri 's/^(OFFLINE_UPGRADE_PLUGIN_VERSION) *=.*/\1 = "%{version}-%{release}"/' plugins/offline_upgrade.py
%if %{with python2}
mkdir python2
%endif
%if %{with python3}
mkdir python3
%endif

%build
%if %{with python2}
pushd python2
  %cmake .. -DPYTHON_DESIRED:FILEPATH=%{__python2}
  %make_build
  make doc-man
popd
%endif
%if %{with python3}
pushd python3
  %cmake .. -DPYTHON_DESIRED:FILEPATH=%{__python3}
  %make_build
  make doc-man
popd
%endif

%install
%if %{with python2}
pushd python2
  %make_install
popd
%endif
%if %{with python3}
pushd python3
  %make_install
popd
%endif

mkdir -p %{buildroot}%{_unitdir}/system-update.target.wants/
pushd %{buildroot}%{_unitdir}/system-update.target.wants/
  ln -sr ../dnf-system-upgrade.service
  ln -sr ../dnf-offline-upgrade.service
popd

%find_lang %{name}

%check
%if %{with python2}
PYTHONPATH="%{buildroot}%{python2_sitelib}:%{buildroot}%{python2_sitelib}/dnf-plugins/" nosetests-%{python2_version} -s tests/
%endif
%if %{with python3}
PYTHONPATH="%{buildroot}%{python3_sitelib}:%{buildroot}%{python3_sitelib}/dnf-plugins/" nosetests-%{python3_version} -s tests/
%endif

%if %{with python2}
%files -n python2-%{name}-common -f %{name}.lang
%{python2_sitelib}/dnfpluginsextras/
%license COPYING
%doc AUTHORS README.rst
%endif

%if %{with python3}
%files -n python3-%{name}-common -f %{name}.lang
%{python3_sitelib}/dnfpluginsextras/
%dir %{python3_sitelib}/dnf-plugins/__pycache__/
%license COPYING
%doc AUTHORS README.rst
%endif

%if %{with python2}
%files -n python2-dnf-plugin-kickstart
%{python2_sitelib}/dnf-plugins/kickstart.*
%{_mandir}/man8/dnf.plugin.kickstart.*
%endif

%if %{with python3}
%files -n python3-dnf-plugin-kickstart
%{python3_sitelib}/dnf-plugins/kickstart.*
%{python3_sitelib}/dnf-plugins/__pycache__/kickstart.*
%{_mandir}/man8/dnf.plugin.kickstart.*
%endif

%if %{with python3}
%files -n python3-dnf-plugin-rpmconf
%config(noreplace) %{_sysconfdir}/dnf/plugins/rpmconf.conf
%{python3_sitelib}/dnf-plugins/rpm_conf.*
%{python3_sitelib}/dnf-plugins/__pycache__/rpm_conf.*
%{_mandir}/man8/dnf.plugin.rpmconf.*
%endif

%if %{with python2}
%files -n python2-dnf-plugin-snapper
%{python2_sitelib}/dnf-plugins/snapper.*
%{_mandir}/man8/dnf.plugin.snapper.*
%endif

%if %{with python3}
%files -n python3-dnf-plugin-snapper
%{python3_sitelib}/dnf-plugins/snapper.*
%{python3_sitelib}/dnf-plugins/__pycache__/snapper.*
%{_mandir}/man8/dnf.plugin.snapper.*
%endif

%if %{with python2}
%files -n python2-dnf-plugin-system-upgrade
%{_unitdir}/dnf-system-upgrade.service
%{_unitdir}/dnf-system-upgrade-cleanup.service
%{_unitdir}/system-update.target.wants/dnf-system-upgrade.service
%{python2_sitelib}/dnf-plugins/system_upgrade.*
%{_mandir}/man8/dnf.plugin.system-upgrade.*
%endif

%if %{with python3}
%files -n python3-dnf-plugin-system-upgrade
%{_unitdir}/dnf-system-upgrade.service
%{_unitdir}/dnf-system-upgrade-cleanup.service
%{_unitdir}/system-update.target.wants/dnf-system-upgrade.service
%{python3_sitelib}/dnf-plugins/system_upgrade.py
%{python3_sitelib}/dnf-plugins/__pycache__/system_upgrade.*
%{_mandir}/man8/dnf.plugin.system-upgrade.*
%endif

%if %{with python2}
%files -n python2-dnf-plugin-offline-upgrade
%{_unitdir}/dnf-offline-upgrade.service
%{_unitdir}/dnf-offline-upgrade-cleanup.service
%{_unitdir}/system-update.target.wants/dnf-offline-upgrade.service
%{python2_sitelib}/dnf-plugins/offline_upgrade.*
%{_mandir}/man8/dnf.plugin.offline-upgrade.*
%endif

%if %{with python3}
%files -n python3-dnf-plugin-offline-upgrade
%{_unitdir}/dnf-offline-upgrade.service
%{_unitdir}/dnf-offline-upgrade-cleanup.service
%{_unitdir}/system-update.target.wants/dnf-offline-upgrade.service
%{python3_sitelib}/dnf-plugins/offline_upgrade.py
%{python3_sitelib}/dnf-plugins/__pycache__/offline_upgrade.*
%{_mandir}/man8/dnf.plugin.offline-upgrade.*
%endif

%if %{with python2}
%files -n python2-dnf-plugin-tracer
%{python2_sitelib}/dnf-plugins/tracer.*
%{_mandir}/man8/dnf.plugin.tracer.*
%endif

%if %{with python3}
%files -n python3-dnf-plugin-tracer
%{python3_sitelib}/dnf-plugins/tracer.*
%{python3_sitelib}/dnf-plugins/__pycache__/tracer.*
%{_mandir}/man8/dnf.plugin.tracer.*
%endif

%if %{with python3}
%files -n python3-dnf-plugin-torproxy
%config(noreplace) %{_sysconfdir}/dnf/plugins/torproxy.conf
%{python3_sitelib}/dnf-plugins/torproxy.*
%{python3_sitelib}/dnf-plugins/__pycache__/torproxy.*
%{_mandir}/man8/dnf.plugin.torproxy.*
%endif

%if %{with python3}
%files -n python3-dnf-plugin-showvars
%{python3_sitelib}/dnf-plugins/showvars.*
%{python3_sitelib}/dnf-plugins/__pycache__/showvars.*
%{_mandir}/man8/dnf.plugin.showvars.*
%endif

%changelog
