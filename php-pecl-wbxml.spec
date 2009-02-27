#
# TODO:
# - compare with php-wbxml.spe
#
%define		_modname	wbxml
%define		_status		stable
Summary:	WBXML to XML conversion
Summary(pl.UTF-8):	Konwersja WBXML do XML
Name:		php-pecl-%{_modname}
Version:	1.0.2
Release:	1
License:	PHP
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	cc38b8388e05153fd0e3b01c713c3e05
URL:		http://pecl.php.net/package/wbxml/
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
BuildRequires:	wbxml2-devel
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This extension provides WBXML (Wireless Binary XML) conversion
capabilities using the libwbxml library.

In PECL status of this extension is: %{_status}.

%description -l pl.UTF-8
Rozszerzenie to udostępnia możliwość konwersji WBXML (Wireless Binary
XML) do XML za pomocą biblioteki libwbxml.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c
mv %{_modname}-%{version}/* .

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc CREDITS README wbxml.php
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
