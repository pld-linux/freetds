#
# Conditional build:
%bcond_with	msdblib		# use MS-style dblib instead of SYB-style
%bcond_without	kerberos5	# Kerberos5 support (via Heimdal)
#
# %%define tdsver - default protocol version; valid versions:
# auto (default)
# 4.2 (used by Sybase SQLServer <= 10 and MS SQL Server 6.5)
# 4.6
# 5.0 (used by Sybase SQLServer >= 11)
# 7.0 (used by MS SQL Server 7.0)
# 7.1 (used by MS SQL Server 2000)
# 7.2 (used by MS SQL Server 2005)
# 7.3 (used by MS SQL Server 2008)
# 7.4 (used by MS SQL Server 2012/2014)

Summary:	Free implementation of Sybase's db-lib
Summary(pl.UTF-8):	Wolnodostępna implementacja db-lib firmy Sybase
Name:		freetds
Version:	1.00.91
Release:	2
License:	LGPL v2+
Group:		Libraries
Source0:	ftp://ftp.freetds.org/pub/freetds/stable/%{name}-%{version}.tar.bz2
# Source0-md5:	8d71f9f29be0fe0637e443dd3807b3fd
Patch0:		%{name}-no-Llibdir.patch
URL:		http://www.freetds.org/
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
BuildRequires:	doxygen
BuildRequires:	gettext-tools
%{?with_kerberos5:BuildRequires:	heimdal-devel}
BuildRequires:	libltdl-devel >= 2:2
BuildRequires:	libtool >= 2:2
BuildRequires:	openssl-devel
BuildRequires:	readline-devel
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
%{?with_kerberos5:Requires:	heimdal-devel}
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
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?with_kerberos5:--enable-krb5=gssapi} \
	--disable-silent-rules \
	%{?with_msdblib:--with-msdblib} \
	--with-openssl \
	%{?tdsver:--with-tdsver=%{tdsver}} \
	--with-unixodbc=/usr

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	ETC=$RPM_BUILD_ROOT%{_sysconfdir}

cp -a src/pool/BUGS BUGS.pool
cp -a src/pool/README README.pool
cp -a src/pool/TODO TODO.pool

# ODBC driver, dlopen()ed
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libtdsodbc.{la,a}

# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

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
%doc AUTHORS BUGS* ChangeLog NEWS README* TODO* doc/userguide
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
%doc doc/reference
%attr(755,root,root) %{_libdir}/libct.so
%attr(755,root,root) %{_libdir}/libsybdb.so
%{_libdir}/libct.la
%{_libdir}/libsybdb.la
%{_includedir}/bkpublic.h
%{_includedir}/cspublic.h
%{_includedir}/cstypes.h
%{_includedir}/ctpublic.h
%{_includedir}/odbcss.h
%{_includedir}/sqldb.h
%{_includedir}/sqlfront.h
%{_includedir}/sybdb.h
%{_includedir}/syberror*.h
%{_includedir}/sybfront.h
%{_includedir}/tds_sysdep_public.h

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
