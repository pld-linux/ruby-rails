%define	ruby_archdir	%(ruby -r rbconfig -e 'print Config::CONFIG["archdir"]')
%define ruby_rubylibdir %(ruby -r rbconfig -e 'print Config::CONFIG["rubylibdir"]')
Summary:	Ruby on Rails setup scripts
Summary(pl):	Skrypty instalacyjne Ruby on Rails
Name:		rails
Version:	0.10.1
Release:	1
License:	GPL
Group:		Development/Languages
Source0:	http://rubyforge.org/frs/download.php/3339/%{name}-%{version}.tgz
# Source0-md5:	0af9dff26117ffeac053332e0efbd52c
Patch0:		%{name}-sanity.patch
URL:		http://www.rubyonrails.com/
BuildRequires:	ruby
BuildRequires:	ruby-devel
Requires:	rake >= 0.4.13
Requires:	ruby-ActionMailer >= 0.7.1
Requires:	ruby-ActionPack >= 1.5.1
Requires:	ruby-ActiveRecord >= 1.8.0
Requires:	ruby-ActiveSupport >= 1.0.1
Requires:	ruby-ActionWebService >= 0.6.0
Requires:	ruby-dev-utils >= 1.0.1
Requires:	ruby-extensions >= 0.6.0
Obsoletes:	railties
Obsoletes:	ruby-Rails
#BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
rails is the scripts that tie the libraries that make up Ruby on Rails 
together.

Ruby on Rails is a rapid development web application platform written in 
Ruby.

%description -l pl
rails to skrypty wi±¿±ce biblioteki tworz±ce razem Ruby on Rails.

Ruby on Rails to platforma WWW do szybkiego tworzenia aplikacji
napisana w jêzyku Ruby.

%prep
%setup -q -n %{name}
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
cd vendor/railties
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{name},%{ruby_rubylibdir}/railties}

rm bin/breakpointer_for_gem
rm environments/shared_for_gem.rb
cp -a configs fresh_rakefile dispatches  environments  helpers \
	$RPM_BUILD_ROOT%{_datadir}/%{name}
cp bin/* $RPM_BUILD_ROOT%{_bindir}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_rubylibdir}/railties

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%{ruby_rubylibdir}/railties
