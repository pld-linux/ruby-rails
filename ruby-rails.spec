# TODO
# - error:php-pear-Text_Highlighter-0.6.5-1 (cnfl rails = 0.12.1-1) conflicts with installed rails-0.12.1-1
Summary:	Ruby on Rails setup scripts
Summary(pl):	Skrypty instalacyjne Ruby on Rails
Name:		rails
Version:	1.0.0
Release:	1
License:	GPL
Group:		Development/Languages
Source0:	http://rubyforge.org/frs/download.php/7654/%{name}-%{version}.tgz
# Source0-md5:	6ea1941564ec1f2372a01aa8c192ad2b
Source1:	%{name}-replacement-generate
Patch0:		%{name}-sanity.patch
URL:		http://www.rubyonrails.com/
BuildRequires:	rpmbuild(macros) >= 1.277
BuildRequires:	ruby-devel
Requires:	rake >= 0.5.4
Requires:	ruby-modules >= 1.8.4-1
Requires:	ruby-ActionMailer >= 1.1.5
Requires:	ruby-ActionPack >= 1.11.2
Requires:	ruby-ActionWebService >= 1.0.0
Requires:	ruby-ActiveRecord >= 1.13.2
Requires:	ruby-ActiveSupport >= 1.2.5
Requires:	ruby-TMail
Requires:	ruby-Text-Format
Requires:	ruby-dev-utils >= 1.0.1
Requires:	ruby-extensions >= 0.6.0
Obsoletes:	railties
Obsoletes:	ruby-Rails
#BuildArch:	noarch
%{?ruby_mod_ver_requires_eq}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
rails is the scripts that tie the libraries that make up Ruby on Rails
together.

Ruby on Rails is a rapid development web application platform written
in Ruby.

%description -l pl
rails to skrypty wi±¿±ce biblioteki tworz±ce razem Ruby on Rails.

Ruby on Rails to platforma WWW do szybkiego tworzenia aplikacji
napisana w jêzyku Ruby.

%prep
%setup -q -n %{name}
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{name}/bin,%{ruby_rubylibdir}/railties}

cd vendor/rails/railties
cp -a configs fresh_rakefile dispatches  environments  helpers html\
	$RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a bin/* \
   $RPM_BUILD_ROOT%{_datadir}/%{name}/bin
install %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/%{name}/bin/generate
cp README \
   $RPM_BUILD_ROOT%{_datadir}/%{name}/README
install bin/rails $RPM_BUILD_ROOT%{_bindir}
install bin/generate $RPM_BUILD_ROOT%{_bindir}/rails-generate
cp -a doc $RPM_BUILD_ROOT%{_datadir}/%{name}/doc
cp -a lib/* $RPM_BUILD_ROOT%{ruby_rubylibdir}/railties

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%{ruby_rubylibdir}/railties
