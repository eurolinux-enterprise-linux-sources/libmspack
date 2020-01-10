Name:           libmspack
Version:        0.5
Release:        0.7.alpha%{?dist}
Summary:        Library for CAB and related files compression and decompression

Group:          System Environment/Libraries
License:        LGPLv2
URL:            http://www.cabextract.org.uk/libmspack/
Source0:        http://www.cabextract.org.uk/libmspack/%{name}-%{version}alpha.tar.gz
Patch0:         %{name}-0.4alpha-doc.patch
BuildRequires:  doxygen

# Fixes for CVE-2018-14679 CVE-2018-14680 CVE-2018-14681 CVE-2018-14682
Patch1:         0001-Fix-off-by-one-bounds-check-on-CHM-PMGI-PMGL-chunk-n.patch
Patch2:         0002-kwaj_read_headers-fix-handling-of-non-terminated-str.patch
Patch3:         0003-Fix-off-by-one-error-in-chmd-TOLOWER-fallback.patch
# Fixes for CVE-2018-18584 CVE-2018-18585
Patch4:         0004-CAB-block-input-buffer-is-one-byte-too-small-for-max.patch
Patch5:         0005-Avoid-returning-CHM-file-entries-that-are-blank-beca.patch

# Patch 2 has a bunch of binary files that cannot be applied using
# plain patch.  So I removed them and packaged them separately in this
# source tarball.
Source2:        kwajd.tar.gz

# We need to rerun autotools after applying the patches above.
BuildRequires:  autoconf, automake, libtool

%description
The purpose of libmspack is to provide both compression and decompression of
some loosely related file formats used by Microsoft.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Obsoletes:      %{name}-doc < 0.2

%description    devel
The %{name}-devel package contains libraries, header files and documentation
for developing applications that use %{name}.


%prep
%setup -q -n %{name}-%{version}alpha
%patch0 -p1
%patch1 -p3
%patch2 -p3
%patch3 -p3
%patch4 -p3
%patch5 -p3
pushd test
zcat %{SOURCE2} | tar xvf -
popd

chmod a-x mspack/mspack.h

autoreconf -i


%build
CFLAGS="%{optflags} -fno-strict-aliasing" \
%configure --disable-static --disable-silent-rules
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'
rm $RPM_BUILD_ROOT%{_libdir}/libmspack.la

iconv -f ISO_8859-1 -t utf8 ChangeLog --output Changelog.utf8
touch -r ChangeLog Changelog.utf8
mv Changelog.utf8 ChangeLog

pushd doc
doxygen
find html -type f | xargs touch -r %{SOURCE0}
rm -f html/installdox
popd


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc README TODO COPYING.LIB ChangeLog AUTHORS
%{_libdir}/*.so.*

%files devel
%doc doc/html
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Fri Dec  7 2018 Richard W.M. Jones <rjones@redhat.com> - 0.5-0.7.alpha
- Fixes for CVE-2018-18584 CVE-2018-18585.
  resolves: rhbz#1648384 rhbz#1648385

* Thu Aug  2 2018 Richard W.M. Jones <rjones@redhat.com> - 0.5-0.6.alpha
- Fixes for CVE-2018-14679 CVE-2018-14680 CVE-2018-14681 CVE-2018-14682
- resolves: rhbz#1611550 rhbz#1611551 rhbz#1611552 rhbz#1611553

* Thu Mar 16 2017 Richard W.M. Jones <rjones@redhat.com> - 0.5-0.5.alpha
- Remove ExclusiveArch
  resolves: rhbz#1422266

* Thu Jul 30 2015 Richard W.M. Jones <rjones@redhat.com> - 0.5-0.4.alpha
- Avoid 'test/md5.c:126:3: warning: dereferencing type-punned pointer
  will break strict-aliasing rules' by adding -fno-strict-aliasing flag.

* Wed Jul 29 2015 Richard W.M. Jones <rjones@redhat.com> - 0.5-0.3.alpha
- Import into RHEL 7.2.
- Add ExcludeArch x86_64
- resolves: rhbz#1223486

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-0.2.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 03 2015 Dan Horák <dan[at]danny.cz> - 0.5-0.1.alpha
- updated to 0.5alpha

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-0.4.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-0.3.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-0.2.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 28 2013 Dan Horák <dan[at]danny.cz> - 0.4-0.1.alpha
- updated to 0.4alpha

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-0.4.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-0.3.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-0.2.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon May 16 2011 Dan Horák <dan[at]danny.cz> - 0.3-0.1.alpha
- updated to 0.3alpha

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-0.2.20100723alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Aug 30 2010 Dan Horák <dan[at]danny.cz> - 0.2-0.1.20100723alpha
- updated to 0.2alpha released 2010/07/23
- merged the doc subpackage with devel

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0-0.7.20060920alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0-0.6.20060920alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 13 2008 Marc Wiriadisastra <marc@mwiriadi.id.au> - 0.0-0.5-20060920alpha
- Rebuild for gcc4.3

* Sun Jan 20 2008 Marc Wiriadisastra <marc@mwiriadi.id.au> - 0.0-0.4.20060920alpha
- installed documentation into html subdir
- manually installed doc's for main package

* Sun Jan 20 2008 Marc Wiriadisastra <marc@mwiriadi.id.au> - 0.0-0.3.20060920alpha
- Got source using wget -N
- Removed some doc's
- Shifted doc line for doc package
- Added install -p

* Sun Jan 20 2008 Marc Wiriadisastra <marc@mwiriadi.id.au> - 0.0-0.2.20060920alpha
- Changed install script for doc package
- Fixed rpmlint issue with debug package

* Fri Jan 18 2008 Marc Wiriadisastra <marc@mwiriadi.id.au> - 20060920cvs.a-1
- Initial release
