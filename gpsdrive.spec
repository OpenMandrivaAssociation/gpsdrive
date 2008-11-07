%define	name 	gpsdrive
%define	version	2.10
%define beta	pre6
%define rel	1
%if %{beta}
%define	release	%mkrel 0.%{beta}.%{rel}
%define distname %{name}-%{version}%{beta}
%else
%define	release	%mkrel %{rel}
%define distname %{name}-%{version}
%endif

Summary:	GPS based navigation tool
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Url:		http://www.gpsdrive.de/
Group:		Networking/Other
Source0:	%{distname}.tar.gz
Source1:	%{name}-48.png
Source2:	%{name}-32.png
Source3:	%{name}-16.png
Patch0:		gpsdrive-2.10pre6-leaf.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	gdk-pixbuf-devel >= 0.11
BuildRequires:	gtk+2-devel >= 2.1
BuildRequires:	pcre-devel
BuildRequires:	desktop-file-utils
BuildRequires:	cmake
BuildRequires:	libgdamm3-devel
BuildRequires:	mapnik-devel
Requires:	gdk-pixbuf >= 0.11

%description
Gpsdrive is a map-based navigation system. It displays your position on a 
zoomable map provided from a NMEA-capable GPS receiver. The maps are 
autoselected for the best resolution, depending of your position, and the 
displayed image can be zoomed. Maps can be downloaded from the Internet with 
one mouse click. The program provides information about speed, direction, 
bearing, arrival time, actual position, and target position. Speech output 
is also available.

%prep
%setup -q -n %{distname}
%patch0 -p1 -b .leaf
mkdir build

%build
pushd build
cmake -D CMAKE_INSTALL_PREFIX=%{_prefix} .. 
%make
popd

%install
rm -rf %{buildroot}
pushd build
%makeinstall_std
popd

rm -rf %{buildroot}%_datadir/%name/{AUTHORS,FAQ*,LEEME,LISEZMOI,README*,TODO,NMEA*,GPS-*}

install -m644 %{SOURCE1} -D %{buildroot}%{_liconsdir}/%{name}.png
install -m644 %{SOURCE2} -D %{buildroot}%{_iconsdir}/%{name}.png
install -m644 %{SOURCE3} -D %{buildroot}%{_miconsdir}/%{name}.png

#menu entry

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="GTK" \
  --add-category="Science" \
  --add-category="X-MandrivaLinux-MoreApplications-Sciences-Other" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

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
%doc GPS-receivers AUTHORS TODO README LEEME
%{_bindir}/*
%{_mandir}/man1/*.1*
%{_mandir}/es/man1/gpsdrive.1*
%{_mandir}/de/man1/gpsdrive.1*
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%_datadir/%name
%_datadir/applications/*
