# Conditional build:
# _with_msdblib - use MS-style dblib
#
# %%define tdsver - protocol version; valid versions:
# 4.2 (used by MS SQL Server 6.0)
# 4.6
# 5.0 (used by Sybase only)
# 7.0 (used by MS SQL Server 7.0) [default]
# 8.0 [only login works now]

%{!?tdsver:%define tdsver 7.0}

Summary:	Free implementation of Sybase's db-lib
Summary(pl):	Wolnodostêpna implementacja db-lib firmy Sybase
Name:		freetds
Version:	0.53
Release:	1
License:	LGPL
Group:		Libraries
Source0:	ftp://ftp.ibiblio.org/pub/Linux/ALPHA/freetds/%{name}-%{version}.tgz
URL:		http://www.freetds.org/
BuildRequires:	autoconf
BuildRequires:	glib-devel
BuildRequires:	unixODBC-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FreeTDS is a free (open source) implementation of Sybase's db-lib,
ct-lib, and ODBC libraries (which can be used also to work with MS SQL
databases). Currently, dblib and ctlib are most mature. Both of these
libraries have several programs known to compile and run against them.
ODBC is not quite as mature, but may work depending on your needs.

%description -l pl
FreeTDS to wolnodostêpna (z otwartymi ¼ród³ami) implementacja
bibliotek db-lib, ct-lib i ODBC firmy Sybase (których mo¿na u¿ywaæ
tak¿e do pracy z bazami MS SQL). Aktualnie najlepiej dzia³aj± dblib i
ctlib - istnieje trochê programów, o których wiadomo, ¿e kompiluj± siê
i dzia³aj± z tymi bibliotekami. ODBC nie jest jeszcze na tyle
skoñczony, ale mo¿e dzia³aæ w zale¿no¶ci od potrzeb.

%package devel
Summary:	FreeTDS header files
Summary(pl):	Pliki nag³ówkowe FreeTDS
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
FreeTDS header files.

%description devel -l pl
Pliki nag³ówkowe FreeTDS.

%package static
Summary:	FreeTDS static libraries
Summary(pl):	Statyczne biblioteki FreeTDS
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
FreeTDS static libraries.

%description static -l pl
Statyczne biblioteki FreeTDS.

%prep
%setup -q

%build
%{__autoconf}
%configure \
	--with-tdsver=%{tdsver} \
	%{?_with_msdblib:--with-msdblib} \
	--with-unixodbc

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	ETC=$RPM_BUILD_ROOT%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS NEWS README TODO
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/freetds.conf

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %{_libdir}/lib*.la
%{_includedir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
