%global gitrev 61e8c5e
%global dnf_version 0.6.3

Name:		dnf-plugins-extras
Version:	0.0.1
Release:	2%{?dist}
Summary:	Extras Plugins for DNF
Group:		System Environment/Base
License:	GPLv2+
URL:		https://github.com/rpm-software-management/dnf-plugins-extras

# source archive is created by running package/archive from a git checkout
Source0:	dnf-plugins-extras-%{gitrev}.tar.xz

BuildArch:	noarch
BuildRequires:	cmake
BuildRequires:	dnf = %{dnf_version}
BuildRequires:	gettext
#BuildRequires:	python-nose
BuildRequires:	python-sphinx
BuildRequires:	python2-devel
Requires:	%{name}-snapper

%description
Extras Plugins for DNF. This package enhance DNF with snapper plugin.

%package -n python3-dnf-plugins-extras
Summary:	Extras Plugins for DNF
Group:		System Environment/Base
BuildRequires:	python3-devel
BuildRequires:	python3-dnf = %{dnf_version}
#BuildRequires:	python3-nose
BuildRequires:	python3-sphinx

Requires:	python3-dnf-plugins-extras-rpmconf
Requires:	python3-dnf-plugins-extras-snapper

%description -n python3-dnf-plugins-extras
Extras Plugins for DNF, Python 3 version. This package enhance DNF with rpmconf
and snapper plugins.

%package common
Summary:	Common files for Extras Plugins for DNF
Requires:	dnf = %{dnf_version}

%description common
Common files for Extras Plugins.

%package -n python3-dnf-plugins-extras-common
Summary:	Common files for Extras Plugins for DNF
Requires:	python3-dnf = %{dnf_version}

%description -n python3-dnf-plugins-extras-common
Common files for Extras Plugins for DNF, Python 3 version.

%package -n python3-dnf-plugins-extras-rpmconf
Summary:	RpmConf Plugin for DNF
Requires:	python3-dnf-plugins-extras-common = %{version}-%{release}
Requires:	python3-rpmconf

%description -n python3-dnf-plugins-extras-rpmconf
RpmConf Plugin for DNF, Python 3 version. Handles .rpmnew, .rpmsave every
transaction.

%package snapper
Summary:	Snapper Plugin for DNF
Requires:	%{name}-common = %{version}-%{release}
Requires:	dbus-python
Requires:	snapper

%description snapper
Snapper Plugin for DNF. Creates snapshot every transaction.

%package -n python3-dnf-plugins-extras-snapper
Summary:	Snapper Plugin for DNF
Requires:	python3-dnf-plugins-extras-common = %{version}-%{release}
Requires:	python3-dbus
Requires:	snapper

%description -n python3-dnf-plugins-extras-snapper
Snapper Plugin for DNF, Python 3 version. Creates snapshot every transaction.

%prep
%setup -q -n dnf-plugins-extras
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

%check
#PYTHONPATH=./plugins /usr/bin/nosetests-2.* -s tests/
#PYTHONPATH=./plugins /usr/bin/nosetests-3.* -s tests/

%files
# No files, metapackage

%files -n python3-dnf-plugins-extras
# No files, metapackage

%files common -f %{name}.lang
%doc AUTHORS COPYING README.rst
%{python_sitelib}/dnfpluginsextras/

%files -n python3-dnf-plugins-extras-common -f %{name}.lang
%doc AUTHORS COPYING README.rst
%{python3_sitelib}/dnfpluginsextras/
%dir %{python3_sitelib}/dnf-plugins/__pycache__/

%files -n python3-dnf-plugins-extras-rpmconf
%{python3_sitelib}/dnf-plugins/rpmconf.*
%{python3_sitelib}/dnf-plugins/__pycache__/rpmconf.*

%files snapper
%{python_sitelib}/dnf-plugins/snapper.*

%files -n python3-dnf-plugins-extras-snapper
%{python3_sitelib}/dnf-plugins/snapper.*
%{python3_sitelib}/dnf-plugins/__pycache__/snapper.*

%changelog

* Wed Dec 17 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.0.1-2
- Fix Requires for py3 dbus
- Fix email address in changelog

* Fri Dec 12 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.0.1-1
- The initial package version.
