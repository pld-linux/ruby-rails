# TODO:
# - Very rough upgrade to 3.x, need to review sub package architecture in light
#   of upstream api re-write.
# - Package various ruby packages as separate subpackages istead of lumping files
#   together under railtiles? (action_view, action_mailer, etc...)
#   Or just set provides?
# - Review deletion of some docs, fix brute force * approach to packaging docs
# - Fix Source0, can be fetched with wget from:
#   http://github.com/rails/rails/tarball/v3.0.1
#
%bcond_without  doc # skip (time-consuming) docs generating; intended for speed up test builds

%define pkgname rails
Summary:	Web-application framework with template engine, control-flow layer, and ORM
Name:		ruby-%{pkgname}
Version:	3.0.1
Release:	0.1
License:	MIT
Group:		Development/Languages
Source0:	http://download.github.com/rails-%{pkgname}-v%{version}-0-gbac6ba9.tar.gz
# Source0-md5:	0e83bc92ac8d1f8c64b0f6eb70772511
URL:		http://www.rubyonrails.org/
BuildRequires:	rpmbuild(macros) >= 1.277
BuildRequires:	ruby-bundler >= 1.0.3
BuildRequires:	ruby-modules >= 1.9.2
Requires:	ruby-modules >= 1.9.2
Requires:	ruby-railties = %{version}-%{release}
Obsoletes:	railties
Obsoletes:	ruby-Rails
#BuildArch:	noarch
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
#Provides:	ruby-abstractcontroller
#Provides:	ruby-actioncontroller
#Provides:	ruby-actiondispatch
#Provides:	ruby-actionmailer
#Provides:	ruby-actionpack
#Provides:	ruby-actionview
#Provides:	ruby-activemodel
#Provides:	ruby-activerecord
#Provides:	ruby-activeresource
#Provides:	ruby-activesupport
Obsoletes:	ruby-actioncontroller
Obsoletes:	ruby-actiondispatch
Obsoletes:	ruby-actionmailer
Obsoletes:	ruby-actionpack
Obsoletes:	ruby-actionview
Obsoletes:	ruby-activemodel
Obsoletes:	ruby-activerecord
Obsoletes:	ruby-activeresource
Obsoletes:	ruby-activesupport

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
%setup -q -n rails-rails-98a44e1
find -newer README.rdoc  -o -print | xargs touch --reference %{SOURCE0}

%{__grep} -rl '/usr/bin/env' . | xargs %{__sed} -i -e '
	s,%{_bindir}/env ruby,%{__ruby},
s,%{_bindir}/env spawn-fcgi,%{_sbindir}/spawn-fcgi,
	s,%{_bindir}/env \(#{File.expand_path(\$0)}\),\1,
'

%build
%if %{with doc}
rdoc --ri --op ri
rdoc --op rdoc
# TODO: why are we selectivly deleting api documentation?
rm -r ri/{\<,ActiveSupport,CGI,CodeStatistics,Object,Plugin,RecursiveHTTPFetcher}
rm ri/created.rid
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{pkgname}} \
	$RPM_BUILD_ROOT{%{ruby_rubylibdir},%{ruby_ridir},%{ruby_rdocdir}}

cp -a {actionmailer,actionpack,activemodel,activerecord,activeresource,activesupport,railties}/lib/* $RPM_BUILD_ROOT%{ruby_rubylibdir}
%if %{with doc}
cp -a ri/* $RPM_BUILD_ROOT%{ruby_ridir}
cp -a rdoc $RPM_BUILD_ROOT%{ruby_rdocdir}/%{name}-%{version}
%endif
cp -a bin $RPM_BUILD_ROOT%{_datadir}/%{pkgname}
install -p bin/rails $RPM_BUILD_ROOT%{_bindir}/rails

cat <<'EOF' > $RPM_BUILD_ROOT%{ruby_rubylibdir}/railties_path.rb
RAILTIES_PATH = "%{_datadir}/%{pkgname}"
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rails
%{_datadir}/%{pkgname}
%{ruby_rubylibdir}/%{pkgname}
%{ruby_rubylibdir}/%{pkgname}.rb

%if %{with doc}
%files rdoc
%defattr(644,root,root,755)
%{ruby_rdocdir}/%{name}-%{version}

%files ri
%defattr(644,root,root,755)
%{ruby_ridir}/*
%endif

%files -n ruby-railties
%defattr(644,root,root,755)
%{ruby_rubylibdir}/railties_path.rb
%{ruby_rubylibdir}/abstract_controller
%{ruby_rubylibdir}/abstract_controller.rb
%{ruby_rubylibdir}/action_controller
%{ruby_rubylibdir}/action_controller.rb
%{ruby_rubylibdir}/action_dispatch
%{ruby_rubylibdir}/action_dispatch.rb
%{ruby_rubylibdir}/action_mailer
%{ruby_rubylibdir}/action_mailer.rb
%{ruby_rubylibdir}/action_pack
%{ruby_rubylibdir}/action_pack.rb
%{ruby_rubylibdir}/action_view
%{ruby_rubylibdir}/action_view.rb
%{ruby_rubylibdir}/active_model
%{ruby_rubylibdir}/active_model.rb
%{ruby_rubylibdir}/active_record
%{ruby_rubylibdir}/active_record.rb
%{ruby_rubylibdir}/active_resource
%{ruby_rubylibdir}/active_resource.rb
%{ruby_rubylibdir}/active_support
%{ruby_rubylibdir}/active_support.rb
