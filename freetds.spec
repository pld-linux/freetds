#
# Conditional build:
# _with_msdblib - use MS-style dblib
#
# %%define tdsver - protocol version; valid versions:
# 4.2 (used by Sybase SQLServer <= 10 and MS SQL Server 6.5)
# 4.6
# 5.0 (used by Sybase SQLServer >= 11)
# 7.0 (used by MS SQL Server 7.0) [default]
# 8.0 (not finished yet!)

%{!?tdsver:%define tdsver 7.0}

Summary:	Free implementation of Sybase's db-lib
Summary(pl):	Wolnodost�pna implementacja db-lib firmy Sybase
Name:		freetds
Version:	0.60
Release:	2
License:	LGPL
Group:		Libraries
Source0:	ftp://ftp.ibiblio.org/pub/Linux/ALPHA/freetds/stable/%{name}-%{version}.tgz
Patch0:		%{name}-nolibnsl.patch
URL:		http://www.freetds.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	glib-devel
BuildRequires:	libtool
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

%description -l pl
FreeTDS to wolnodost�pna (z otwartymi �r�d�ami) implementacja
bibliotek db-lib, ct-lib i ODBC firmy Sybase (kt�rych mo�na u�ywa�
tak�e do pracy z bazami MS SQL). Aktualnie najlepiej dzia�aj� dblib i
ctlib - istnieje troch� program�w, o kt�rych wiadomo, �e kompiluj� si�
i dzia�aj� z tymi bibliotekami. ODBC nie jest jeszcze na tyle
sko�czony, ale mo�e dzia�a� w zale�no�ci od potrzeb.

%package devel
Summary:	FreeTDS header files
Summary(pl):	Pliki nag��wkowe FreeTDS
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
FreeTDS header files.

%description devel -l pl
Pliki nag��wkowe FreeTDS.

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
%patch -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
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

%post
/sbin/ldconfig
if [ -f /etc/freetds.conf ]; then
	mv -f /etc/freetds.conf %{_sysconfdir}/freetds.conf
fi

%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog README* TODO
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%attr(755,root,root) %{_bindir}/*
%dir %{_sysconfdir}
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/freetds.conf
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/locales.conf
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
