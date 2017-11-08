%?mingw_package_header

Name:           mingw-openblas
Version:        0.2.20
Release:        1%{?dist}
Summary:        MinGW port of OpenBLAS

License:        BSD
URL:            https://github.com/xianyi/OpenBLAS
Source0:        https://github.com/xianyi/OpenBLAS/archive/v%{version}.tar.gz

BuildRequires:  mingw32-filesystem
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-gfortran

BuildRequires:  mingw64-filesystem
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-gcc-gfortran

BuildArch:      noarch

%description
MinGW Windows port of OpenBLAS.

# Win32
%package -n mingw32-openblas
Summary:        32-bit version of OpenBLAS for Windows

%description -n mingw32-openblas
%mingw32_description

# Win64
%package -n mingw64-openblas
Summary:        64-bit version of OpenBLAS for Windows

%description -n mingw64-openblas
%mingw64_description

%?mingw_debug_package

%prep
%setup -qcT
tar -xzf %{SOURCE0}

for arch in win{64,32}; do
    cp -ar OpenBLAS-%{version} serial-"$arch"
    cp -ar OpenBLAS-%{version} threaded-"$arch"
    cp -ar OpenBLAS-%{version} openmp-"$arch"
done

%build
# Generic options for Win32/64
nmax="NUM_THREADS=128"
target="TARGET=CORE2 DYNAMIC_ARCH=1"

# Win32
cross_suffix=%{mingw32_target}-
cross_cc=${cross_suffix}gcc
cross_fc=${cross_suffix}gfortran

common="%{mingw32_cflags}"
fcommon="$common -frecursive"
make -C serial-win32 \
    "$nmax" $target BINARY=32 USE_THREAD=0 USE_OPENMP=0 \
    HOSTCC=gcc CROSS=1 CROSS_SUFFIX="$cross_suffix" \
    CC="$cross_cc" FC="$cross_fc" \
    COMMON_OPT="$common" FCOMMON_OPT="$fcommon" LIBPREFIX="libopenblas"
make -C threaded-win32 \
    "$nmax" $target BINARY=32 USE_THREAD=1 USE_OPENMP=0 \
    HOSTCC=gcc CROSS=1 CROSS_SUFFIX="$cross_suffix" \
    CC="$cross_cc" FC="$cross_fc" \
    COMMON_OPT="$common" FCOMMON_OPT="$fcommon" LIBPREFIX="libopenblasp"

common="%{mingw32_cflags} -fopenmp -pthread"
fcommon="$common -frecursive"
make -C openmp-win32 \
    "$nmax" $target BINARY=32 USE_THREAD=1 USE_OPENMP=1 \
    HOSTCC=gcc CROSS=1 CROSS_SUFFIX="$cross_suffix" \
    CC="$cross_cc" FC="$cross_fc" \
    COMMON_OPT="$common" FCOMMON_OPT="$fcommon" LIBPREFIX="libopenblaso"

# Win64
cross_suffix=%{mingw64_target}-
cross_cc=${cross_suffix}gcc
cross_fc=${cross_suffix}gfortran

common="%{mingw64_cflags}"
fcommon="$common -frecursive"
make -C serial-win64 \
    "$nmax" $target BINARY=64 USE_THREAD=0 USE_OPENMP=0 \
    HOSTCC=gcc CROSS=1 CROSS_SUFFIX="$cross_suffix" \
    CC="$cross_cc" FC="$cross_fc" \
    COMMON_OPT="$common" FCOMMON_OPT="$fcommon" LIBPREFIX="libopenblas"
make -C threaded-win64 \
    "$nmax" $target BINARY=64 USE_THREAD=1 USE_OPENMP=0 \
    HOSTCC=gcc CROSS=1 CROSS_SUFFIX="$cross_suffix" \
    CC="$cross_cc" FC="$cross_fc" \
    COMMON_OPT="$common" FCOMMON_OPT="$fcommon" LIBPREFIX="libopenblasp"

common="%{mingw64_cflags} -fopenmp -pthread"
fcommon="$common -frecursive"
make -C openmp-win64 \
    "$nmax" $target BINARY=64 USE_THREAD=1 USE_OPENMP=1 \
    HOSTCC=gcc CROSS=1 CROSS_SUFFIX="$cross_suffix" \
    CC="$cross_cc" FC="$cross_fc" \
    COMMON_OPT="$common" FCOMMON_OPT="$fcommon" LIBPREFIX="libopenblaso"

%install
# Win32
make -C serial-win32 \
    DESTDIR="%{buildroot}" \
    OPENBLAS_LIBRARY_DIR=%{mingw32_libdir} \
    OPENBLAS_INCLUDE_DIR=%{mingw32_includedir}/openblas \
    OPENBLAS_BINARY_DIR=%{mingw32_bindir} LIBPREFIX="libopenblas" install
make -C threaded-win32 \
    DESTDIR="%{buildroot}" \
    OPENBLAS_LIBRARY_DIR=%{mingw32_libdir} \
    OPENBLAS_INCLUDE_DIR=%{mingw32_includedir}/openblas \
    OPENBLAS_BINARY_DIR=%{mingw32_bindir} LIBPREFIX="libopenblasp" install
make -C openmp-win32 \
    DESTDIR="%{buildroot}" \
    OPENBLAS_LIBRARY_DIR=%{mingw32_libdir} \
    OPENBLAS_INCLUDE_DIR=%{mingw32_includedir}/openblas \
    OPENBLAS_BINARY_DIR=%{mingw32_bindir} LIBPREFIX="libopenblaso" install

# Win64
make -C serial-win64 \
    DESTDIR="%{buildroot}" \
    OPENBLAS_LIBRARY_DIR=%{mingw64_libdir} \
    OPENBLAS_INCLUDE_DIR=%{mingw64_includedir}/openblas \
    OPENBLAS_BINARY_DIR=%{mingw64_bindir} LIBPREFIX="libopenblas" install
make -C threaded-win64 \
    DESTDIR="%{buildroot}" \
    OPENBLAS_LIBRARY_DIR=%{mingw64_libdir} \
    OPENBLAS_INCLUDE_DIR=%{mingw64_includedir}/openblas \
    OPENBLAS_BINARY_DIR=%{mingw64_bindir} LIBPREFIX="libopenblasp" install
make -C openmp-win64 \
    DESTDIR="%{buildroot}" \
    OPENBLAS_LIBRARY_DIR=%{mingw64_libdir} \
    OPENBLAS_INCLUDE_DIR=%{mingw64_includedir}/openblas \
    OPENBLAS_BINARY_DIR=%{mingw64_bindir} LIBPREFIX="libopenblaso" install

rm -rf %{buildroot}%{mingw32_libdir}/{cmake,pkgconfig}
rm -rf %{buildroot}%{mingw64_libdir}/{cmake,pkgconfig}

# Win32
%files -n mingw32-openblas
%{mingw32_bindir}/libopenblas.dll
%{mingw32_bindir}/libopenblasp.dll
%{mingw32_bindir}/libopenblaso.dll
%{mingw32_includedir}/openblas/
%{mingw32_libdir}/libopenblas.dll.a
%{mingw32_libdir}/libopenblasp.dll.a
%{mingw32_libdir}/libopenblaso.dll.a
%{mingw32_libdir}/libopenblas.a
%{mingw32_libdir}/libopenblasp.a
%{mingw32_libdir}/libopenblaso.a
%{mingw32_libdir}/libopenblas-r%{version}.a
%{mingw32_libdir}/libopenblaspp-r%{version}.a
%{mingw32_libdir}/libopenblasop-r%{version}.a

# Win64
%files -n mingw64-openblas
%{mingw64_bindir}/libopenblas.dll
%{mingw64_bindir}/libopenblasp.dll
%{mingw64_bindir}/libopenblaso.dll
%{mingw64_includedir}/openblas/
%{mingw64_libdir}/libopenblas.dll.a
%{mingw64_libdir}/libopenblasp.dll.a
%{mingw64_libdir}/libopenblaso.dll.a
%{mingw64_libdir}/libopenblas.a
%{mingw64_libdir}/libopenblasp.a
%{mingw64_libdir}/libopenblaso.a
%{mingw64_libdir}/libopenblas-r%{version}.a
%{mingw64_libdir}/libopenblaspp-r%{version}.a
%{mingw64_libdir}/libopenblasop-r%{version}.a

%changelog
* Thu Nov 10 2017 Jajauma's Packages <jajauma@yandex.ru> - 0.2.20-1
- Initial release
