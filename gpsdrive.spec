Summary:	GPS based navigation tool
Name:		gpsdrive
Version:	2.11
Release:	4
License:	GPLv2+
Group:		Networking/Other
URL:		http://www.gpsdrive.de/
Source0:	http://www.gpsdrive.de/packages/%{name}-%{version}.tar.gz
Source1:	http://download.sourceforge.net/sourceforge/gpsdrive/openstreetmap-map-icons-minimal.tar.gz
Source2:	%{name}-48.png
Source3:	%{name}-32.png
Source4:	%{name}-16.png
source5:	.abf.yml
Patch0:		gpsdrive-2.10pre6-leaf.patch
Patch1:		gpsdrive-2.10pre7-fedora.patch
Patch2:		gpsdrive-2.10pre7-usepc.patch
Patch3:		gpsdrive-2.10-newgps.patch
Patch4:		gpsdrive-2.10-fix-dso-linking.patch
Patch5:		gpsdrive-2.11-add-gdk-pixbuf2.patch
Patch6:		gpsdrive_no_segfault_on_nan_lat.patch
patch7:		gpsdrive-2.11.mapnik.cpp.patch

BuildRequires:	cmake
BuildRequires:	desktop-file-utils
BuildRequires:	boost-devel
BuildRequires:	curl-devel
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	gpsd-devel
BuildRequires:	mapnik-devel
BuildRequires:	pq-devel
BuildRequires:	speech-dispatcher-devel
BuildRequires:	sqlite3-devel
BuildRequires:	pkgconfig(libxml-2.0)

Provides:	perl(Geo::OSM::EntitiesV3)
Provides:	perl(Geo::OSM::OsmReaderV5)
Provides:	perl(Geo::OSM::EntitiesV5)
Provides:	perl(Geo::OSM::OsmReaderV3)

%description
Gpsdrive is a map-based navigation system. It displays your position on a 
zoomable map provided from a NMEA-capable GPS receiver. The maps are 
autoselected for the best resolution, depending of your position, and the 
displayed image can be zoomed. Maps can be downloaded from the Internet with 
one mouse click. The program provides information about speed, direction, 
bearing, arrival time, actual position, and target position. Speech output 
is also available.

%prep
%setup -q -n %{name}-%{version} -a1
%patch0 -p1 -b .leaf
%patch1 -p1
%patch2 -p1 -b .usepc
%patch3 -p1 -b .newgps
%patch4 -p1 -b .fix-dso-linking
%patch5 -p1 -b .gdk-pixbuf2
%patch6 -p0 -b .nan
%patch7 -p1 -b .mapnikcpp

%build
export CXXFLAGS="%optflags -DBOOST_FILESYSTEM_VERSION=3"
%cmake
%make

%install
%makeinstall_std -C build

rm -rf %{buildroot}%{_datadir}/%{name}/{AUTHORS,FAQ*,LEEME,LISEZMOI,README*,TODO,NMEA*,GPS-*}

install -m644 %{SOURCE2} -D %{buildroot}%{_liconsdir}/%{name}.png
install -m644 %{SOURCE3} -D %{buildroot}%{_iconsdir}/%{name}.png
install -m644 %{SOURCE4} -D %{buildroot}%{_miconsdir}/%{name}.png

#menu entry
desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="GTK" \
  --add-category="Science" \
  --add-category="X-MandrivaLinux-MoreApplications-Sciences-Other" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

install -d %{buildroot}%{_datadir}/icons/map-icons
cp -a usr/share/icons/map-icons/* %{buildroot}%{_datadir}/icons/map-icons/

%find_lang %{name}

%files -f %{name}.lang
%doc AUTHORS README
%{_bindir}/*
%{_mandir}/man1/*.1*
%{_mandir}/es/man1/gpsdrive.1*
%{_mandir}/de/man1/gpsdrive.1*
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/icons/map-icons
%{_datadir}/%{name}
%{_datadir}/applications/*
%{perl_vendorlib}/*


%changelog
* Fri Jun 08 2012 Matthew Dawkins <mattydaw@mandriva.org> 2.11-4
+ Revision: 803621
- rebuild for boost libs
- cleaned up spec

* Tue Mar 15 2011 Funda Wang <fwang@mandriva.org> 2.11-3
+ Revision: 644852
- force filesystem v2
- cleanup BRs

* Sun Oct 31 2010 Olivier Thauvin <nanardon@mandriva.org> 2.11-2mdv2011.0
+ Revision: 590726
- patch6: don't segfault on nan latitude

* Wed Sep 22 2010 Oden Eriksson <oeriksson@mandriva.com> 2.11-1mdv2011.0
+ Revision: 580527
- sync with fedora

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - rebuild
    - drop old menu
    - kill re-definition of %%buildroot on Pixel's request

  + Emmanuel Andry <eandry@mandriva.org>
    - fix br
    - New version 2.10pre7
    - update BR

  + Olivier Blin <blino@mandriva.org>
    - update doc list
    - do not package inexistant pixmaps
    - remove lib packages
    - add more man pages in files list
    - fix build with latest boost
    - build with gda3 and mapnik
    - use cmake
    - update URL
    - 2.10-pre6
    - restore BuildRoot

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers


* Sun Sep 10 2006 Emmanuel Andry <eandry@mandriva.org> 2.09-5mdv2007.0
- Buildrequires desktop-file-utils

* Sun Sep 10 2006 Emmanuel Andry <eandry@mandriva.org> 2.09-4mdv2007.0
- xdg menu (#25478)

* Thu Oct 27 2005 Lenny Cartier <lenny@mandriva.com> 2.09-3mdk
- rebuild for dependencies

* Thu Jul 07 2005 Lenny Cartier <lenny@mandrakesoft.com> 2.09-2mdk
- rebuild

* Thu Mar 11 2004 Lenny Cartier <lenny@mandrakesoft.com> 2.09-1mdk
- 2.09

* Thu Feb 26 2004 Lenny Cartier <lenny@mandrakesoft.com> 2.08-1mdk
- 2.08

* Fri Feb 20 2004 David Baudens <baudens@mandrakesoft.com> 2.07-2mdk
- Fix menu

* Mon Jan 19 2004 Lenny Cartier <lenny@mandrakesoft.com> 2.07-1mdk
- 2.07

* Fri Jan 02 2004 Lenny Cartier <lenny@mandrakesoft.com> 2.06-1mdk
- 2.06

* Sun Dec 14 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 2.04-1mdk
- 2.04
- spec cosmetics
- fix buildrequires (lib64..)
- fix provides
- remove explicit library dependency
- don't bzip2 icons in src.rpm
- don't rm -rf $RPM_BUILD_ROOT in %%prep
- remove .bz2 ending of man pages
- use %%mklibname macro

