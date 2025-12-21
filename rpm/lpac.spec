Name: lpac

Summary: C-based eUICC LPA Local Profile Assistant Client (GSMA RSP)
Version: 2.3.0
Release: 1
License: MIT
URL: https://github.com/estkme-group/lpac
Source0: %{name}-%{version}.tar.gz

BuildRequires: cmake
BuildRequires: gcc
BuildRequires: make

BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(json-glib-1.0)
BuildRequires: pkgconfig(libcurl)
BuildRequires: pkgconfig(libpcsclite)
BuildRequires: pkgconfig(libgbinder)
BuildRequires: pkgconfig(libglibutil)
BuildRequires: pkgconfig(openssl)

Requires: pcsc-lite
Requires: pcsc-ccid

%description
LPAC is a Local Profile Assistant Client implementing GSMA RSP (Remote SIM Provisioning)
for eSIM/eUICC management. Supports ES8/ES9/ES10/ES11, PCSC and gbinder.

Upstream repositories:
- https://github.com/estkme-group/lpac
- https://github.com/juanro49/lpac (with SailfishOS fixes and rpm build)


%prep
%autosetup -n %{name}-%{version}/upstream -p1


%build
touch .git
cmake -B build \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_INTERPROCEDURAL_OPTIMIZATION=OFF \
    -DLPAC_WITH_APDU_AT=ON \
    -DLPAC_WITH_APDU_GBINDER=ON \
    -DLPAC_WITH_APDU_PCSC=ON \
    -DLPAC_WITH_HTTP_CURL=ON \
    -L
cmake --build build %{?_smp_mflags}


%install
rm -rf %{buildroot}
DESTDIR=%{buildroot} cmake --install build


%post
/sbin/ldconfig


%postun
/sbin/ldconfig


%files
%{_bindir}/lpac
%{_libdir}/libeuicc.so
%{_libdir}/libeuicc.so.2
%{_libdir}/liblpac-utils.so
%{_libdir}/libeuicc-driver-loader.so
%{_libdir}/libeuicc-driver-loader.so.2
%{_libdir}/libeuicc-drivers.so
%{_libdir}/libeuicc-drivers.so.2
%{_libdir}/lpac/driver/*
%{_libdir}/pkgconfig/libeuicc.pc
%{_libdir}/pkgconfig/libeuicc-driver-loader.pc


# ================
#  DEVEL (headers)
# ================
%package devel
Summary: Development files for LPAC
Requires: %{name} = %{version}-%{release}

%description devel
Development headers and CMake files for LPAC.

%files devel
%{_includedir}/*
%{_libdir}/cmake/*
%{_libdir}/libcjson.a
%{_libdir}/pkgconfig/libcjson.pc
