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
# Source0-md5:	e9f953cbb68a8d139db853f8e3ef0ef0
Patch0:		%{name}-sanity.patch
URL:		http://www.rubyonrails.com/
BuildRequires:	ruby
BuildRequires:	ruby-devel
Requires:	rake >= 0.4.13
Requires:	ruby-ActionMailer >= 0.10.1
Requires:	ruby-ActionPack >= 0.10.1
Requires:	ruby-ActiveRecord >= 0.10.1
Requires:	ruby-ActiveSupport >= 0.10.1
Requires:	ruby-dev-utils >= 1.0.1
Requires:	ruby-extensions >= 0.6.0
Obsoletes:	ruby-Rails
#BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
railties is the scripts that tie Ruby on Rails together.

%description -l pl
railties to skrypty, które wi±¿± Ruby on Rails w ca³o¶æ.

%prep
%setup -q
%patch0 -p1
find . -name '.svn' -print0 | xargs -0 rm -r

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{name},%{ruby_rubylibdir}/%{name}}

rm bin/breakpointer_for_gem
rm environments/shared_for_gem.rb
cp -a * $RPM_BUILD_ROOT%{_datadir}/%{name}
rm $RPM_BUILD_ROOT%{_datadir}/%{name}/bin/rails
cp bin/* $RPM_BUILD_ROOT%{_bindir}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_rubylibdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%{ruby_rubylibdir}/%{name}
