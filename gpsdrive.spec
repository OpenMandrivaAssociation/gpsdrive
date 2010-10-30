Summary:	GPS based navigation tool
Name:		gpsdrive
Version:	2.11
Release:	%mkrel 2
License:	GPLv2+
Group:		Networking/Other
URL:		http://www.gpsdrive.de/
Source0:	http://www.gpsdrive.de/packages/%{name}-%{version}.tar.gz
Source1:	http://download.sourceforge.net/sourceforge/gpsdrive/openstreetmap-map-icons-minimal.tar.gz
Source2:	%{name}-48.png
Source3:	%{name}-32.png
Source4:	%{name}-16.png
Patch0:		gpsdrive-2.10pre6-leaf.patch
Patch1:		gpsdrive-2.10pre7-fedora.patch
Patch2:		gpsdrive-2.10pre7-usepc.patch
Patch3:		gpsdrive-2.10-newgps.patch
Patch4:		gpsdrive-2.10-fix-dso-linking.patch
Patch5:		gpsdrive-2.11-add-gdk-pixbuf2.patch
Patch6:     gpsdrive_no_segfault_on_nan_lat.patch
BuildRequires:	boost-devel
BuildRequires:	cairo-devel
BuildRequires:	cmake
BuildRequires:	curl-devel
BuildRequires:	desktop-file-utils
BuildRequires:	gda2.0-devel
BuildRequires:	gettext
BuildRequires:	gettext-devel
BuildRequires:	gpsd-devel
BuildRequires:	gtk+2-devel >= 2.1
BuildRequires:	icu-devel
BuildRequires:	intltool
BuildRequires:	libgdk_pixbuf2.0-devel
BuildRequires:	libtool-devel
BuildRequires:	libxml2-devel
BuildRequires:	mapnik-devel
BuildRequires:	pango-devel
BuildRequires:	pcre-devel
BuildRequires:	postgresql-devel
BuildRequires:	speech-dispatcher-devel
BuildRequires:	sqlite-devel
Provides:	perl(Geo::OSM::EntitiesV3)
Provides:	perl(Geo::OSM::OsmReaderV5)
Provides:	perl(Geo::OSM::EntitiesV5)
Provides:	perl(Geo::OSM::OsmReaderV3)
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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

%build
%cmake -D CMAKE_INSTALL_PREFIX=%{_prefix} .. 
%make VERBOSE=1

%install
rm -rf %{buildroot}
pushd build
%makeinstall_std
popd

rm -rf %{buildroot}%_datadir/%name/{AUTHORS,FAQ*,LEEME,LISEZMOI,README*,TODO,NMEA*,GPS-*}

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

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS README
%{_bindir}/*
%{_mandir}/man1/*.1*
%{_mandir}/es/man1/gpsdrive.1*
%{_mandir}/de/man1/gpsdrive.1*
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/icons/map-icons
%_datadir/%name
%_datadir/applications/*
%{perl_vendorlib}/*
