%define pkgname rails
Summary:	Web-application framework with template engine, control-flow layer, and ORM
Name:		ruby-%{pkgname}
Version:	2.0.4
Release:	0.1
License:	MIT
Group:		Development/Languages
Source0:	http://rubyforge.org/frs/download.php/42597/%{pkgname}-%{version}.gem
# Source0-md5:	14b0f7202e0a42230d794b8335588cd7
Patch0:		%{name}-paths.patch
URL:		http://www.rubyonrails.org/
BuildRequires:	rpmbuild(macros) >= 1.277
Requires:	rake >= 0.7.2
Requires:	ruby-TMail
Requires:	ruby-Text-Format
Requires:	ruby-dev-utils >= 1.0.1
Requires:	ruby-extensions >= 0.6.0
Requires:	ruby-modules >= 1.8.4-1
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
Requires:	ruby-ActionMailer >= 2.0.4
Requires:	ruby-ActionPack >= 2.0.4
Requires:	ruby-ActiveRecord >= 2.0.4
Requires:	ruby-ActiveResource >= 2.0.4
Requires:	ruby-ActiveSupport >= 2.0.4

%description -n ruby-railties
Rails is a framework for building web-application using CGI, FCGI,
mod_ruby, or WEBrick on top of either MySQL, PostgreSQL, SQLite, DB2,
SQL Server, or Oracle with eRuby- or Builder-based templates.

This package contains railties module.

%prep
%setup -qcT
%{__tar} xf %{SOURCE0} -O data.tar.gz | %{__tar} xz
find -newer README  -o -print | xargs touch --reference %{SOURCE0}
%patch0 -p1

%{__grep} -rl '/usr/local/bin/ruby' . | xargs %{__sed} -i -e 's,/usr/local/bin/ruby,%{_bindir}/ruby,'
%{__grep} -rl '/usr/bin/env' . | xargs %{__sed} -i -e '
	s,/usr/bin/env ruby,%{_bindir}/ruby,
	s,/usr/bin/env spawn-fcgi,/usr/sbin/spawn-fcgi,
	s,/usr/bin/env \(#{File.expand_path(\$0)}\),\1,
'

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{pkgname},%{ruby_sitelibdir}}
cp -a lib/* $RPM_BUILD_ROOT%ruby_sitelibdir
cp -a bin builtin configs dispatches doc environments helpers html fresh_rakefile README $RPM_BUILD_ROOT%{_datadir}/%{pkgname}
install -p bin/rails $RPM_BUILD_ROOT%{_bindir}/rails
cat <<'EOF' > $RPM_BUILD_ROOT%{ruby_sitelibdir}/railties_path.rb
RAILTIES_PATH = "%{_datadir}/%{pkgname}"
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{pkgname}
%{ruby_sitelibdir}/commands*
%{ruby_sitelibdir}/tasks*
%{ruby_sitelibdir}/console_*.rb
%{ruby_sitelibdir}/*_server.rb

%files -n ruby-railties
%defattr(644,root,root,755)
%{ruby_sitelibdir}/*
%exclude %{ruby_sitelibdir}/commands*
%exclude %{ruby_sitelibdir}/tasks*
%exclude %{ruby_sitelibdir}/console_*.rb
%exclude %{ruby_sitelibdir}/*_server.rb
