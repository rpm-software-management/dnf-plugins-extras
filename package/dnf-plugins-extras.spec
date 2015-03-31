%{!?gitrev: %global gitrev d42291d}
%{!?dnf_version: %global dnf_version 0.6.4-2}

Name:		dnf-plugins-extras
Version:	0.0.6
Release:	1%{?dist}
Summary:	Extras Plugins for DNF
Group:		System Environment/Base
License:	GPLv2+
URL:		https://github.com/rpm-software-management/dnf-plugins-extras

# source archive is created by running package/archive from a git checkout
Source0:	dnf-plugins-extras-%{gitrev}.tar.xz

BuildArch:	noarch
BuildRequires:	cmake
BuildRequires:	gettext
%if 0%{?fedora} >= 23
Requires:	python3-dnf-plugins-extras = %{version}-%{release}
%else
Requires:	python-dnf-plugins-extras = %{version}-%{release}
%endif

%description
Extras Plugins for DNF. This package enhance DNF with repomanage, snapper and
tracer plugins.

%package -n python-dnf-plugins-extras
Summary:	Extras Plugins for DNF
Group:		System Environment/Base
BuildRequires:	python-dnf >= %{dnf_version}
BuildRequires:	python-nose
BuildRequires:	python-sphinx
BuildRequires:	python2-devel

Requires:	python-dnf-plugins-extras-debug
Requires:	python-dnf-plugins-extras-local
Requires:	python-dnf-plugins-extras-migrate
Requires:	python-dnf-plugins-extras-orphans
Requires:	python-dnf-plugins-extras-repoclosure
Requires:	python-dnf-plugins-extras-repograph
Requires:	python-dnf-plugins-extras-repomanage
Requires:	python-dnf-plugins-extras-snapper
Requires:	python-dnf-plugins-extras-tracer
Obsoletes:	dnf-plugins-extras <= 0.0.4-2

%description -n python-dnf-plugins-extras
Extras Plugins for DNF, Python 2 version. This package enhance DNF with repomanage, snapper and
tracer plugins.

%package -n python3-dnf-plugins-extras
Summary:	Extras Plugins for DNF
Group:		System Environment/Base
BuildRequires:	python3-devel
BuildRequires:	python3-dnf >= %{dnf_version}
BuildRequires:	python3-nose
BuildRequires:	python3-sphinx

Requires:	python3-dnf-plugins-extras-debug
Requires:	python3-dnf-plugins-extras-local
Requires:	python3-dnf-plugins-extras-migrate
Requires:	python3-dnf-plugins-extras-orphans
Requires:	python3-dnf-plugins-extras-repoclosure
Requires:	python3-dnf-plugins-extras-repograph
Requires:	python3-dnf-plugins-extras-repomanage
%if 0%{?fedora} > 21
Requires:	python3-dnf-plugins-extras-rpmconf
%endif
Requires:	python3-dnf-plugins-extras-snapper
Requires:	python3-dnf-plugins-extras-tracer
Obsoletes:	dnf-plugins-extras <= 0.0.4-2

%description -n python3-dnf-plugins-extras
Extras Plugins for DNF, Python 3 version. This package enhance DNF with
repomanage, rpmconf, snapper and tracer plugins.

%package -n python-dnf-plugins-extras-common
Summary:	Common files for Extras Plugins for DNF
Requires:	python-dnf >= %{dnf_version}
%if 0%{?fedora} < 23
Provides:	dnf-plugins-extras-common = %{version}-%{release}
Obsoletes:	dnf-plugins-extras-common <= 0.0.4-2
%endif

%description -n python-dnf-plugins-extras-common
Common files for Extras Plugins, Python 2 version.

%package -n python3-dnf-plugins-extras-common
Summary:	Common files for Extras Plugins for DNF
Requires:	python3-dnf >= %{dnf_version}
%if 0%{?fedora} >= 23
Provides:	dnf-plugins-extras-common = %{version}-%{release}
Obsoletes:	dnf-plugins-extras-common <= 0.0.4-2
%endif

%description -n python3-dnf-plugins-extras-common
Common files for Extras Plugins for DNF, Python 3 version.

%package -n python-dnf-plugins-extras-debug
Summary:	Debug Plugin for DNF
Requires:	python-dnf-plugins-extras-common = %{version}-%{release}
%if 0%{?fedora} < 23
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
Provides:	dnf-plugins-extras-debug = %{version}-%{release}
Obsoletes:	dnf-plugins-extras-debug <= 0.0.4-2
%endif

%description -n python3-dnf-plugins-extras-debug
Debug Plugin for DNF, Python 3 version. Writes system RPM configuration to
a dump file and restores it.

%package -n python-dnf-plugins-extras-local
Summary:	Local Plugin for DNF
Requires:	python-dnf-plugins-extras-common = %{version}-%{release}
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
%if 0%{?fedora} < 23
Provides:	dnf-plugins-extras-migrate = %{version}-%{release}
Obsoletes:	dnf-plugins-extras-migrate <= 0.0.4-2
%endif

%description -n python-dnf-plugins-extras-migrate
Migrate Plugin for DNF, Python 2 version. igrates yum's history, group and
yumdb data to dnf.

%package -n python3-dnf-plugins-extras-migrate
Summary:	Migrate Plugin for DNF
Requires:	python3-dnf-plugins-extras-common = %{version}-%{release}
%if 0%{?fedora} >= 23
Provides:	dnf-plugins-extras-migrate = %{version}-%{release}
Obsoletes:	dnf-plugins-extras-migrate <= 0.0.4-2
%endif

%description -n python3-dnf-plugins-extras-migrate
Migrate Plugin for DNF, Python 3 version. igrates yum's history, group and
yumdb data to dnf.

%package -n python-dnf-plugins-extras-orphans
Summary:	Orphans Plugin for DNF
Requires:	python-dnf-plugins-extras-common = %{version}-%{release}
%if 0%{?fedora} < 23
Provides:	dnf-plugins-extras-orphans = %{version}-%{release}
Obsoletes:	dnf-plugins-extras-orphans <= 0.0.4-2
%endif

%description -n python-dnf-plugins-extras-orphans
Orphans Plugin for DNF, Python 2 version. List all installed packages
not required by any other installed package.

%package -n python3-dnf-plugins-extras-orphans
Summary:	Orphans Plugin for DNF
Requires:	python3-dnf-plugins-extras-common = %{version}-%{release}
%if 0%{?fedora} >= 23
Provides:	dnf-plugins-extras-orphans = %{version}-%{release}
Obsoletes:	dnf-plugins-extras-orphans <= 0.0.4-2
%endif

%description -n python3-dnf-plugins-extras-orphans
Orphans Plugin for DNF, Python 3 version. List all installed packages
not required by any other installed package.

%package -n python-dnf-plugins-extras-repoclosure
Summary:	RepoClosure Plugin for DNF
Requires:	python-dnf-plugins-extras-common = %{version}-%{release}
%if 0%{?fedora} < 23
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
Provides:	dnf-plugins-extras-repograph = %{version}-%{release}
Obsoletes:	dnf-plugins-extras-repograph <= 0.0.4-2
%endif

%description -n python-dnf-plugins-extras-repograph
RepoGraph Plugin for DNF, Python 2 version. Output a full package dependency graph in dot format.

%package -n python3-dnf-plugins-extras-repograph
Summary:	RepoGraph Plugin for DNF
Requires:	python3-dnf-plugins-extras-common = %{version}-%{release}
%if 0%{?fedora} >= 23
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
Provides:	dnf-plugins-extras-repomanage = %{version}-%{release}
Obsoletes:	dnf-plugins-extras-repomanage <= 0.0.4-2
%endif

%description -n python-dnf-plugins-extras-repomanage
RepoManage Plugin for DNF, Python 2 version. Manage a directory of rpm packages.

%package -n python3-dnf-plugins-extras-repomanage
Summary:	RepoManage Plugin for DNF
Requires:	python3-dnf-plugins-extras-common = %{version}-%{release}
%if 0%{?fedora} >= 23
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
Provides:	dnf-plugin-tracer = 1:%{version}-%{release}
Provides:	dnf-plugins-extras-tracer = %{version}-%{release}
Obsoletes:	dnf-plugins-extras-tracer <= 0.0.4-2
%endif

%description -n python3-dnf-plugins-extras-tracer
Tracer Plugin for DNF, Python 3 version. Finds outdated running applications in
your system every transaction.

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

%if 0%{?fedora} <= 21
rm -f %{buildroot}%{python3_sitelib}/dnf-plugins/rpm_conf.*
rm -f %{buildroot}%{python3_sitelib}/dnf-plugins/__pycache__/rpm_conf.*
rm -f %{buildroot}%{_mandir}/man8/dnf.plugin.rpmconf.*
%endif

%check
PYTHONPATH=./plugins /usr/bin/nosetests-2.* -s tests/
PYTHONPATH=./plugins /usr/bin/nosetests-3.* -s tests/

%files
# No files, metapackage

%files -n python-dnf-plugins-extras
# No files, metapackage

%files -n python3-dnf-plugins-extras
# No files, metapackage

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

%files -n python3-dnf-plugins-extras-migrate
%{python3_sitelib}/dnf-plugins/migrate.*
%{python3_sitelib}/dnf-plugins/__pycache__/migrate.*
%{_mandir}/man8/dnf.plugin.migrate.*

%files -n python-dnf-plugins-extras-orphans
%{python_sitelib}/dnf-plugins/orphans.*
%{_mandir}/man8/dnf.plugin.orphans.*

%files -n python3-dnf-plugins-extras-orphans
%{python3_sitelib}/dnf-plugins/orphans.*
%{python3_sitelib}/dnf-plugins/__pycache__/orphans.*
%{_mandir}/man8/dnf.plugin.orphans.*

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

%changelog
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
