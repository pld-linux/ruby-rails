%bcond_without  doc # skip (time-consuming) docs generating; intended for speed up test builds

%define		pkgname		rails
Summary:	Web-application framework with template engine, control-flow layer, and ORM
Name:		ruby-%{pkgname}
Version:	3.2.19
Release:	1
License:	MIT
Group:		Development/Languages
Source0:	http://rubygems.org/downloads/railties-%{version}.gem
# Source0-md5:	541a47ca3d89fb1103dc2a54b41f86ff
Source1:	http://rubygems.org/downloads/rails-%{version}.gem
# Source1-md5:	3545800bc87637a368eb9614b5309a4e
URL:		http://www.rubyonrails.org/
Patch0:		system-bundle.patch
Patch1:		disable-sprockets.patch
Patch2:		bogus-deps.patch
BuildRequires:	rpmbuild(macros) >= 1.277
BuildRequires:	ruby-bundler >= 1.0.3
BuildRequires:	ruby-modules >= 1.9.2
Requires:	ruby-actionmailer = %{version}
Requires:	ruby-actionpack = %{version}
Requires:	ruby-activerecord = %{version}
Requires:	ruby-activeresource = %{version}
Requires:	ruby-activesupport = %{version}
Requires:	ruby-arel >= 3.0.2
Requires:	ruby-builder >= 3.0.0
Requires:	ruby-erubis >= 2.7.0
Requires:	ruby-i18n >= 0.6.4
Requires:	ruby-journey >= 1.0.4
Requires:	ruby-mail >= 2.5.4
Requires:	ruby-modules >= 1.9.2
Requires:	ruby-multi_json >= 1.0
Requires:	ruby-polyglot >= 0.3.1
Requires:	ruby-rack >= 1.4.5
Requires:	ruby-rack-cache >= 1.2
Requires:	ruby-rack-test >= 0.6.1
Requires:	ruby-railties = %{version}-%{release}
Requires:	ruby-treetop >= 1.4.8
Requires:	ruby-tzinfo >= 0.3.29
Conflicts:	ruby-arel >= 3.1
Conflicts:	ruby-builder >= 4.0
Conflicts:	ruby-erubis >= 2.8.0
Conflicts:	ruby-i18n >= 1.0
Conflicts:	ruby-journey >= 1.1
Conflicts:	ruby-mail >= 2.6
Conflicts:	ruby-multi_json >= 2.0
Conflicts:	ruby-rack >= 1.5
Conflicts:	ruby-rack-cache >= 2.0
Conflicts:	ruby-rack-test >= 0.7
Conflicts:	ruby-treetop >= 1.5
Conflicts:	ruby-tzinfo >= 0.4
Obsoletes:	railties
Obsoletes:	ruby-Rails
BuildArch:	noarch
%{?ruby_mod_ver_requires_eq}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# nothing to be placed there. we're not noarc only because of ruby packaging
%define		_enable_debug_packages	0

%description
Rails is a framework for building web-application using CGI, FCGI,
mod_ruby, or WEBrick on top of either MySQL, PostgreSQL, SQLite, DB2,
SQL Server, or Oracle with eRuby- or Builder-based templates.

%description -l pl.UTF-8
rails to skrypty wiążące biblioteki tworzące razem Ruby on Rails.

Ruby on Rails to platforma WWW do szybkiego tworzenia aplikacji
napisana w języku Ruby.

This package contains development tools.

%package -n ruby-railties
Summary:	Gluing the Engine to the Rails
Group:		Development/Languages
Requires:	ruby-rails = %{version}-%{release}
Requires:	ruby-coffee-rails >= 3.2.1
Requires:	ruby-jquery-rails
Requires:	ruby-sass-rails >= 3.2.3
Requires:	ruby-sqlite3
#Suggests:	ruby-uglifier >= 1.0.3
#Suggests:	ruby-sprockets >= 2.2.1
#Conflicts:	ruby-sprockets >= 2.3
Conflicts:	ruby-coffee-rails >= 3.3
Conflicts:	sass-rails >= 3.3

%description -n ruby-railties
Rails is a framework for building web-application using CGI, FCGI,
mod_ruby, or WEBrick on top of either MySQL, PostgreSQL, SQLite, DB2,
SQL Server, or Oracle with eRuby- or Builder-based templates.

This package contains railties module.

%package rdoc
Summary:	HTML documentation for %{pkgname}
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla %{pkgname}
Group:		Documentation
Requires:	ruby >= 1:1.8.7-4

%description rdoc
HTML documentation for %{pkgname}.

%description rdoc -l pl.UTF-8
Dokumentacja w formacie HTML dla %{pkgname}.

%package ri
Summary:	ri documentation for %{pkgname}
Summary(pl.UTF-8):	Dokumentacja w formacie ri dla %{pkgname}
Group:		Documentation
Requires:	ruby

%description ri
ri documentation for %{pkgname}.

%description ri -l pl.UTF-8
Dokumentacji w formacie ri dla %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}
install -d railgem
%{__tar} xf %{SOURCE1} -C railgem/

%patch0 -p1
%patch1 -p1

# write .gemspec
cd railgem
%__gem_helper spec
cd ..
%__gem_helper spec
%patch2 -p1

find -newer README.rdoc -o -print | xargs touch --reference %{SOURCE0}

%{__grep} -rl '/usr/bin/env' . | xargs %{__sed} -i -e '
	s,/usr/bin/env ruby,%{__ruby},
	s,/usr/bin/env spawn-fcgi,/usr/sbin/spawn-fcgi,
	s,/usr/bin/env \(#{File.expand_path(\$0)}\),\1,
'

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%build
%{__sed} -i -e 's/\(.*s.add_dependency.*rdoc.*\)~>\(.*3.4.*\)/\1>\2/g' \
	railties*.gemspec

%if %{with doc}
rdoc --ri --op ri lib
rdoc --op rdoc lib
rm -r ri/{ActiveSupport,Object,Plugin,RecursiveHTTPFetcher}
rm ri/created.rid
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{pkgname}} \
	$RPM_BUILD_ROOT{%{ruby_rubylibdir},%{ruby_ridir},%{ruby_rdocdir}} \
	$RPM_BUILD_ROOT%{ruby_specdir}

cp -a lib/* $RPM_BUILD_ROOT%{ruby_rubylibdir}
%if %{with doc}
cp -a ri/* $RPM_BUILD_ROOT%{ruby_ridir}
cp -a rdoc $RPM_BUILD_ROOT%{ruby_rdocdir}/%{name}-%{version}
%endif
#-cp -a bin builtin configs dispatches doc environments helpers html fresh_rakefile README $RPM_BUILD_ROOT%{_datadir}/%{pkgname}
cp -a bin $RPM_BUILD_ROOT%{_datadir}/%{pkgname}
install -p bin/rails $RPM_BUILD_ROOT%{_bindir}/rails

cp -p railties-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}
cp -p railgem/%{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

cat <<'EOF' > $RPM_BUILD_ROOT%{ruby_rubylibdir}/railties_path.rb
RAILTIES_PATH = "%{_datadir}/%{pkgname}"
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rails
%{_datadir}/%{pkgname}
%{ruby_specdir}/%{pkgname}-%{version}.gemspec

%if %{with doc}
%files rdoc
%defattr(644,root,root,755)
%{ruby_rdocdir}/%{name}-%{version}

%files ri
%defattr(644,root,root,755)
%{ruby_ridir}/Rails*
%endif

%files -n ruby-railties
%defattr(644,root,root,755)
%{ruby_rubylibdir}/*
%{ruby_specdir}/railties-%{version}.gemspec
