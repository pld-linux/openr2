#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	OpenR2 - MFC/R2 signalling over E1 lines
Summary(pl.UTF-8):	OpenR2 - sygnały MFC/R2 po liniach E1
Name:		openr2
Version:	1.3.2
Release:	2
License:	LGPL v2+ (library), GPL v2+ (utilities)
Group:		Libraries
#Source0Download: https://github.com/moises-silva/openr2/releases
Source0:	https://github.com/moises-silva/openr2/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	5858020ad014c111f6f7a8c86758da6c
Patch0:		%{name}-nosvn.patch
Patch1:		%{name}-opt.patch
Patch2:		%{name}-libdir.patch
URL:		https://libopenr2.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dahdi-linux-devel
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenR2 is a library that implements the MFC/R2 signalling over E1
lines using the Zapata Telephony interface (or DAHDI).

%description -l pl.UTF-8
OpenR2 to biblioteka implementująca przesyłanie sygnałów MFC/R2 po
liniach E1 przy użyciu interfejsu Zapata Telephony (lub DAHDI).

%package devel
Summary:	Header files for OpenR2 library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki OpenR2
License:	LGPL v2+
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for OpenR2 library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki OpenR2.

%package static
Summary:	Static OpenR2 library
Summary(pl.UTF-8):	Statyczna biblioteka OpenR2
License:	LGPL v2+
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static OpenR2 library.

%description static -l pl.UTF-8
Statyczna biblioteka OpenR2.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CREDITS ChangeLog NEWS README TODO doc/README.asterisk doc/asterisk
%attr(755,root,root) %{_bindir}/r2dtmf_detect
%attr(755,root,root) %{_bindir}/r2test
%attr(755,root,root) %{_libdir}/libopenr2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopenr2.so.3
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/r2proto.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/r2test.conf
%{_mandir}/man5/r2test.conf.5*
%{_mandir}/man8/r2test.8*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libopenr2.so
%{_libdir}/libopenr2.la
%{_includedir}/openr2
%{_includedir}/openr2.h

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libopenr2.a
%endif
