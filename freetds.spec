#
# Conditional build:
%bcond_with	msdblib		# use MS-style dblib instead of SYB-style
#
# %%define tdsver - default protocol version; valid versions:
# 4.2 (used by Sybase SQLServer <= 10 and MS SQL Server 6.5)
# 4.6
# 5.0 (used by Sybase SQLServer >= 11)
# 7.0 (used by MS SQL Server 7.0) [spec default]
# 8.0

%{!?tdsver:%define tdsver 7.0}

Summary:	Free implementation of Sybase's db-lib
Summary(pl.UTF-8):	Wolnodostępna implementacja db-lib firmy Sybase
Name:		freetds
Version:	0.82
Release:	2
License:	LGPL
Group:		Libraries
Source0:	ftp://ftp.ibiblio.org/pub/Linux/ALPHA/freetds/stable/%{name}-%{version}.tar.gz
# Source0-md5:	3df6b2e83fd420e90f1becbd1162990a
Patch0:		%{name}-cvs-fixes.patch
URL:		http://www.freetds.org/
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
BuildRequires:	gettext
BuildRequires:	libltdl-devel
BuildRequires:	libtool
BuildRequires:	openssl-devel
BuildRequires:	unixODBC-devel
Requires(post):	/sbin/ldconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/tds

%description
FreeTDS is a free (open source) implementation of Sybase's db-lib,
ct-lib, and ODBC libraries (which can be used also to work with MS SQL
databases). Currently, dblib and ctlib are most mature. Both of these
libraries have several programs known to compile and run against them.
ODBC is not quite as mature, but may work depending on your needs.

%description -l pl.UTF-8
FreeTDS to wolnodostępna (z otwartymi źródłami) implementacja
bibliotek db-lib, ct-lib i ODBC firmy Sybase (których można używać
także do pracy z bazami MS SQL). Aktualnie najlepiej działają dblib i
ctlib - istnieje trochę programów, o których wiadomo, że kompilują się
i działają z tymi bibliotekami. ODBC nie jest jeszcze na tyle
skończony, ale może działać w zależności od potrzeb.

%package devel
Summary:	FreeTDS header files
Summary(pl.UTF-8):	Pliki nagłówkowe FreeTDS
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	openssl-devel

%description devel
FreeTDS header files.

%description devel -l pl.UTF-8
Pliki nagłówkowe FreeTDS.

%package static
Summary:	FreeTDS static libraries
Summary(pl.UTF-8):	Statyczne biblioteki FreeTDS
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
FreeTDS static libraries.

%description static -l pl.UTF-8
Statyczne biblioteki FreeTDS.

%package odbc
Summary:	FreeTDS ODBC driver for unixODBC
Summary(pl.UTF-8):	Sterownik ODBC FreeTDS dla unixODBC
Group:		Libraries
Requires(post):	/sbin/ldconfig
Requires(post):	/usr/bin/odbcinst
Requires:	%{name} = %{version}-%{release}
Requires:	unixODBC

%description odbc
FreeTDS ODBC driver for unixODBC.

%description odbc -l pl.UTF-8
Sterownik ODBC FreeTDS dla unixODBC.

%prep
%setup -q
%patch0 -p1

%build
# hack for libtool 2.2
cp -f /usr/share/gettext/config.rpath .
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-tdsver=%{tdsver} \
	%{?with_msdblib:--with-msdblib} \
	--with-openssl \
	--with-unixodbc=/usr

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	ETC=$RPM_BUILD_ROOT%{_sysconfdir}

mv -f src/pool/BUGS BUGS.pool
mv -f src/pool/README README.pool
mv -f src/pool/TODO TODO.pool

# ODBC driver, dlopen()ed
rm -f $RPM_BUILD_ROOT%{_libdir}/libtdsodbc.{la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
if [ -f /etc/freetds.conf ]; then
	mv -f /etc/freetds.conf %{_sysconfdir}/freetds.conf
fi

%postun	-p /sbin/ldconfig

%post odbc
/sbin/ldconfig
/usr/bin/odbcinst -i -d -r <<EOF
[FreeTDS]
Description = FreeTDS unixODBC Driver
Driver = %{_libdir}/libtdsodbc.so.0
Setup = %{_libdir}/libtdsodbc.so.0
EOF
/usr/bin/odbcinst -i -d -r <<EOF
[SQL Server]
Description = FreeTDS unixODBC Driver
Driver = %{_libdir}/libtdsodbc.so.0
Setup = %{_libdir}/libtdsodbc.so.0
EOF

%postun odbc -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS* ChangeLog NEWS README* TODO*
%attr(755,root,root) %{_bindir}/bsqldb
%attr(755,root,root) %{_bindir}/datacopy
%attr(755,root,root) %{_bindir}/defncopy
%attr(755,root,root) %{_bindir}/fisql
%attr(755,root,root) %{_bindir}/freebcp
%attr(755,root,root) %{_bindir}/tdspool
%attr(755,root,root) %{_bindir}/tsql
%attr(755,root,root) %{_libdir}/libct.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libct.so.4
%attr(755,root,root) %{_libdir}/libsybdb.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsybdb.so.5
%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/freetds.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/locales.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pool.conf
%{_mandir}/man1/bsqldb.1*
%{_mandir}/man1/datacopy.1*
%{_mandir}/man1/defncopy.1*
%{_mandir}/man1/fisql.1*
%{_mandir}/man1/freebcp.1*
%{_mandir}/man1/tsql.1*
%{_mandir}/man5/freetds.conf.5*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libct.so
%attr(755,root,root) %{_libdir}/libsybdb.so
%{_libdir}/libct.la
%{_libdir}/libsybdb.la
%{_includedir}/*.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libct.a
%{_libdir}/libsybdb.a

%files odbc
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/bsqlodbc
%attr(755,root,root) %{_bindir}/osql
%attr(755,root,root) %{_libdir}/libtdsodbc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtdsodbc.so.0
%attr(755,root,root) %{_libdir}/libtdsodbc.so
%{_mandir}/man1/bsqlodbc.1*
%{_mandir}/man1/osql.1*
