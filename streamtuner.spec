%define name	streamtuner
%define version 0.99.99
%define release %mkrel 16

Name: 	 	%{name}
Summary: 	Internet audio stream browser
Version: 	%{version}
Release: 	%{release}

Source:		%{name}-%{version}.tar.bz2
Patch0:		%{name}-%{version}-live365.diff
Patch1:		%{name}-%{version}-helpdir.patch
Patch2:		%{name}-%{version}-xdgconfig.patch
Patch3:		%{name}-%{version}-shoutcast_url.patch
Patch4:		streamtuner-0.99.99-fix-link.patch
URL:		https://www.nongnu.org/streamtuner/
License:	GPL
Group:		Sound
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: 	gtk2-devel, imagemagick, scrollkeeper, curl-devel
BuildRequires:	libxml2-devel
BuildRequires:	gtk-doc intltool
BuildRequires:	taglib-devel
BuildRequires:	pygtk2.0-devel
Requires:	xterm
Requires:	%name-plugins
Requires(post): scrollkeeper
Requires(postun): scrollkeeper

%description
Streamtuner is a stream directory browser. It offers an intuitive and unified
interface to various streaming directories through the use of a plugin system.
Currently, ShoutCast is the only plugin.

%package -n %name-devel
Summary:	Development files from %name
Group:		Development/C
Provides:	%name-devel = %version-%release
Requires:	%name = %version

%description -n %name-devel
Headers and static libraries from %name

%package -n %name-plugins
Summary:	Plugins files for %name
Group:		Sound
Provides:	%name-plugins = %version-%release
Requires:	%name = %version
Requires:	pygtk2.0

%description -n %name-plugins
Plugins file for streamtuner, including Xiph.org station,
Live365, Shoutcast and other...

%prep
%setup -q
%patch0
%patch1 -p1
%patch2
%patch3
%patch4 -b .link

%build
./autogen.sh
%configure2_5x --disable-gtktest
%make

%install
rm -rf %buildroot
%makeinstall_std
rm -fr $RPM_BUILD_ROOT/var/lib
%find_lang %name --with-gnome

#icons
mkdir -p $RPM_BUILD_ROOT/%_liconsdir
convert -size 48x48 art/%name.png $RPM_BUILD_ROOT/%_liconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_iconsdir
convert -size 32x32 art/%name.png $RPM_BUILD_ROOT/%_iconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_miconsdir
convert -size 16x16 art/%name.png $RPM_BUILD_ROOT/%_miconsdir/%name.png

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post
%update_menus
%update_scrollkeeper
%endif
		
%if %mdkversion < 200900
%postun
%clean_menus
%clean_scrollkeeper
%endif

%files -f %name.lang
%defattr(-,root,root)
%doc README COPYING AUTHORS NEWS TODO
%{_bindir}/%{name}*
%{_datadir}/%name
%{_datadir}/help/streamtuner/C
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/*.png
%{_datadir}/omf/%name
%{_liconsdir}/%name.png
%{_iconsdir}/%name.png
%{_miconsdir}/%name.png

%files -n %name-devel
%defattr(-,root,root)
%{_includedir}/%name
%{_libdir}/%name/plugins/*.la
%{_libdir}/%name/plugins/*.a
%{_libdir}/pkgconfig/*.pc
%doc %{_datadir}/gtk-doc/html/%name

%files -n %name-plugins
%defattr(-,root,root)
%{_libdir}/%name/plugins/*.so


