#
# TODO:
# - compare with php-wbxml.spec
#
%define		php_name	php%{?php_suffix}
%define		modname	wbxml
%define		status	stable
Summary:	WBXML to XML conversion
Summary(pl.UTF-8):	Konwersja WBXML do XML
Name:		%{php_name}-pecl-%{modname}
Version:	1.0.3
Release:	9
License:	PHP
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	9c6a4d347f9a2b4002ea0c83e4b14082
Patch0:		wbxml-1.0.2-format_not_a_string_literal_and_no_format_arguments.diff
Patch1:		wbxml-1.0.3-expat_fix.diff
Patch2:		libwbxml.patch
Patch3:		x32.patch
URL:		http://pecl.php.net/package/wbxml/
BuildRequires:	%{php_name}-devel >= 4:5.0.4
BuildRequires:	libwbxml-devel >= 0.11
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Provides:	php(%{modname}) = %{version}
Obsoletes:	php-pecl-wbxml < 1.0.3-7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This extension provides WBXML (Wireless Binary XML) conversion
capabilities using the libwbxml library.

In PECL status of this extension is: %{status}.

%description -l pl.UTF-8
Rozszerzenie to udostępnia możliwość konwersji WBXML (Wireless Binary
XML) do XML za pomocą biblioteki libwbxml.

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -qc
mv %{modname}-%{version}/* .
%patch -P0 -p0
%patch -P1 -p0
%patch -P2 -p1
%patch -P3 -p1

%build
export CFLAGS="%{rpmcflags} `pkg-config --cflags libwbxml2`"
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

%{__make} install \
	EXTENSION_DIR=%{php_extensiondir} \
	INSTALL_ROOT=$RPM_BUILD_ROOT
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
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
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
