
Summary:	A daemon to record and keep track of system up times
Name:		uptimed
Version:	0.4.0
Release:	6%{?dist}
License:	GPLv2
Group:		System Environment/Daemons
URL:		https://github.com/rpodgorny/uptimed/
Source0:	https://github.com/rpodgorny/%{name}/archive/v%{version}.tar.gz
# https://github.com/rpodgorny/uptimed/pull/6
Patch0:		uptimed-0001-systemd-unit-run-as-daemon-user-not-root.patch
BuildRequires:	systemd-units
BuildRequires:	autoconf, automake, libtool
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description
Uptimed is an up time record daemon keeping track of the highest
up times the system ever had.

Uptimed has the ability to inform you of records and milestones
though syslog and e-mail, and comes with a console front end to
parse the records, which can also easily be used to show your
records on your Web page

%package devel
Summary:	Development header and library for uptimed
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Development header and library for uptimed.

%prep
%setup -q
# remove bundled getopt
rm -rf src/getopt.[ch]
sed --in-place -e 's/AC_REPLACE_FUNCS(getopt)//' configure.ac
%patch0 -p1

%build
./autogen.sh
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
# remove superflous file
rm %{buildroot}/%{_libdir}/libuptimed.la
# Debian ships urec.h as uptimed.h since 2005
mkdir %{buildroot}%{_includedir}
cp libuptimed/urec.h %{buildroot}%{_includedir}/uptimed.h
install -m 755 -d %{buildroot}%{_pkgdocdir}/sample-cgi
install -m 644 sample-cgi/uprecords.* %{buildroot}%{_pkgdocdir}/sample-cgi
mv %{buildroot}/etc/uptimed.conf-dist %{buildroot}/etc/uptimed.conf
mkdir -p %{buildroot}%{_localstatedir}/spool/uptimed

%post
/sbin/ldconfig
%systemd_post %{name}.service
systemctl enable %{name}.service

%post devel -p /sbin/ldconfig

%postun
/sbin/ldconfig
%systemd_postun_with_restart %{name}.service

%postun devel -p /sbin/ldconfig

%preun
%systemd_preun %{name}.service

%files
%defattr(-,root,root,-)
%doc AUTHORS CREDITS ChangeLog INSTALL.cgi INSTALL.upgrade README.md README.unsupported TODO sample-cgi/
%license COPYING
%config(noreplace) %{_sysconfdir}/uptimed.conf
%{_sbindir}/uptimed
%{_bindir}/uprecords
%{_mandir}/*/*
%{_libdir}/libuptimed.so.*
%{_unitdir}/uptimed.service
%dir %attr(-,daemon,daemon) %{_localstatedir}/spool/uptimed

%files devel
%defattr(-,root,root,-)
%{_libdir}/libuptimed.so
%{_includedir}/uptimed.h

%changelog
* Sat Jul 15 2017 Tomasz Torcz <ttorcz@fedoraproject.org> - 0.4.0-6
- establish EPEL7 branch based on fedora rawhide (f27) (rhbz#1470857)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 13 2015 Tomasz Torcz <ttorcz@fedoraproject.org> - 0.4.0-2
- switch to running as 'daemon' user

* Wed Apr 29 2015 Tomasz Torcz <ttorcz@fedoraproject.org> - 0.4.0-1
- new upstream release

* Wed Dec 03 2014 Tomasz Torcz <ttorcz@fedoraproject.org> - 0.3.18-1
- new upstream release 0.3.18

* Wed Oct 22 2014 Tomasz Torcz <ttorcz@fedoraproject.org> - 0.3.17.20141021hg29bd8b1eb43d-1
- package snapshot
- use upstream systemd units

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.17-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.17-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Jul 27 2013 Tomasz Torcz <ttorcz@fedoraproject.org> - 0.3.17-5
- use _pkgdocdir (https://fedoraproject.org/wiki/Changes/UnversionedDocdirs)

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Aug 23 2012 Tomasz Torcz <ttorcz@fedoraproject.org> 0.3.17-3
- bring systemd unit in-line with upstream (until new version is released)
- use systemd macros
- do not use macros for system executables (rm, sed)

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 03 2012 Tomasz Torcz <ttorcz@fedoraproject.org> 0.3.17-1
- new upstream version
- do not regenerate auto* stuff

* Sat Feb 11 2012 Tomasz Torcz <ttorcz@fedoraproject.org> 0.3.16-9
- remove bundled getopt

* Thu Feb 09 2012 Tomasz Torcz <ttorcz@fedoraproject.org> 0.3.16-8
- start Description= in unit file with uppercase
- provide defattr for -devel files

* Sun Jan 29 2012 Tomasz Torcz <ttorcz@fedoraproject.org> 0.3.16-7
- remove epoch for -devel Requires

* Sat Jan 14 2012 Tomasz Torcz <ttorcz@fedoraproject.org> 0.3.16-6
- add missing percentage sign to -devel Requires

* Sat Jan 14 2012 Tomasz Torcz <ttorcz@fedoraproject.org> 0.3.16-5
- add _isa to -devel Requires
- mention header in -devel description and summary

* Mon Jan  9 2012 Tomasz Torcz <ttorcz@fedoraproject.org> 0.3.16-4
- ship urec.h as uptimed.h in -devel

* Sun Jan  1 2012 Tomasz Torcz <ttorcz@fedoraproject.org> 0.3.16-3
- correct review issues (#770283):
  - dropped BuildRoot:, clean and rm -rf "{buildroot}" from install
  - use defattr(-,root,root,-) instead of defattr(-,root,root)
  - use dir {_localstatedir}/spool/uptimed/ in files
  - don't package uptimed.la

* Wed Dec 28 2011 Tomasz Torcz <ttorcz@fedoraproject.org> 0.3.16-2
- added Group: and Requires: to -devel

* Sun Dec 25 2011 Tomasz Torcz <ttorcz@fedoraproject.org> 0.3.16-1
- Initial version based on .spec shipped with source 

