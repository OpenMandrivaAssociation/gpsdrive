%define	name 	gpsdrive
%define	version	2.09
%define	release	%mkrel 5

%define	major	2
%define	libname	%mklibname fly %{major}

Summary:	GPS based navigation tool
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Url:		http://www.kraftvoll.at/software/
Group:		Networking/Other
Source0:	%{name}-%{version}.tar.bz2
Source1:	%{name}-48.png
Source2:	%{name}-32.png
Source3:	%{name}-16.png
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	gdk-pixbuf-devel >= 0.11
BuildRequires:	gtk+2-devel >= 2.1
BuildRequires:	pcre-devel
BuildRequires:	desktop-file-utils
Requires:	gdk-pixbuf >= 0.11

%description
Gpsdrive is a map-based navigation system. It displays your position on a 
zoomable map provided from a NMEA-capable GPS receiver. The maps are 
autoselected for the best resolution, depending of your position, and the 
displayed image can be zoomed. Maps can be downloaded from the Internet with 
one mouse click. The program provides information about speed, direction, 
bearing, arrival time, actual position, and target position. Speech output 
is also available.

%package -n %libname
Summary:	Gpsdrive needed library
Group:		System/Libraries

%description -n %libname
Gpsdrive needed library

%package -n %libname-devel
Summary:	Gpsdrive needed library
Group:		Development/C
Requires:	%libname = %version
Provides:	libfly-devel = %{version}-%{release}
Provides:	fly-devel = %{version}-%{release}

%description -n %libname-devel
Development files.


%prep
%setup -q

%build
%configure
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

rm -rf $RPM_BUILD_ROOT/%_datadir/%name/{AUTHORS,FAQ*,LEEME,LISEZMOI,README*,TODO,NMEA*,GPS-*}

install -m644 %{SOURCE1} -D $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png
install -m644 %{SOURCE2} -D $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
install -m644 %{SOURCE3} -D $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png

#menu entry
mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat << EOF > $RPM_BUILD_ROOT%{_menudir}/%{name}
?package(%{name}): \
needs="x11" \ 
section="More Applications/Sciences/Other" \
title="GpsDrive" \
longtitle="A GPS based navigation tool for Gnome" \
command="%{_bindir}/%{name}" \
icon="gpsdrive.png" \
xdg="true"
EOF

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="GTK" \
  --add-category="Science" \
  --add-category="X-MandrivaLinux-MoreApplications-Sciences-Other" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_menus
   
%postun
%clean_menus

%post -n %libname -p /sbin/ldconfig

%postun -n %libname -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%doc GPS-receivers AUTHORS TODO README LEEME
%{_bindir}/*
%{_mandir}/man1/gpsdrive.1*
%{_mandir}/es/man1/gpsdrive.1*
%{_mandir}/de/man1/gpsdrive.1*
%{_menudir}/%{name}
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%_datadir/%name
%_datadir/applications/*
%_datadir/pixmaps/*

%files -n %libname
%defattr(-,root,root)
%_libdir/*.so.*

%files -n %libname-devel
%defattr(-,root,root)
%_libdir/*.so
%_libdir/*.*a

