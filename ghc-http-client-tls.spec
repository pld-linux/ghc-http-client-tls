#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	http-client-tls
Summary:	http-client backend using the connection package and tls library
Name:		ghc-%{pkgname}
Version:	0.3.5.3
Release:	1
License:	MIT
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/http-client-tls
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	e6fcaf662568396d9e385e8a6373bc32
URL:		http://hackage.haskell.org/package/http-client-tls
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-case-insensitive
BuildRequires:	ghc-connection >= 0.2.5
BuildRequires:	ghc-cryptonite
BuildRequires:	ghc-data-default-class
BuildRequires:	ghc-http-client >= 0.5.0
BuildRequires:	ghc-http-types
BuildRequires:	ghc-memory
BuildRequires:	ghc-network >= 2.6
BuildRequires:	ghc-network-uri >= 2.6
BuildRequires:	ghc-tls >= 1.2
%if %{with prof}
BuildRequires:	ghc-prof
BuildRequires:	ghc-case-insensitive-prof
BuildRequires:	ghc-connection-prof >= 0.2.5
BuildRequires:	ghc-cryptonite-prof
BuildRequires:	ghc-data-default-class-prof
BuildRequires:	ghc-http-client-prof >= 0.5.0
BuildRequires:	ghc-http-types-prof
BuildRequires:	ghc-memory-prof
BuildRequires:	ghc-network-prof >= 2.6
BuildRequires:	ghc-network-uri-prof >= 2.6
BuildRequires:	ghc-tls-prof >= 1.2
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires(post,postun):	/usr/bin/ghc-pkg
Requires:	ghc-case-insensitive
Requires:	ghc-connection >= 0.2.5
Requires:	ghc-cryptonite
Requires:	ghc-data-default-class
Requires:	ghc-http-client >= 0.5.0
Requires:	ghc-http-types
Requires:	ghc-memory
Requires:	ghc-network >= 2.6
Requires:	ghc-network-uri >= 2.6
Requires:	ghc-tls >= 1.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
Use the http-client package with the pure-Haskell tls package for
secure connections.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-case-insensitive-prof
Requires:	ghc-connection-prof >= 0.2.5
Requires:	ghc-cryptonite-prof
Requires:	ghc-data-default-class-prof
Requires:	ghc-http-client-prof >= 0.5.0
Requires:	ghc-http-types-prof
Requires:	ghc-memory-prof
Requires:	ghc-network-prof >= 2.6
Requires:	ghc-network-uri-prof >= 2.6
Requires:	ghc-tls-prof >= 1.2

%description prof
Profiling %{pkgname} library for GHC.  Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build %{?_smp_mflags}
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc ChangeLog.md README.md %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a

%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/HTTP
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/HTTP/Client
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/HTTP/Client/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/HTTP/Client/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Network/HTTP/Client/*.p_hi
%endif
