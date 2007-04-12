%define name fast-user-switch-applet
%define version 2.17.4
%define release %mkrel 2

Summary: Fast User-Switching Applet for GNOME
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://ftp.gnome.org/pub/GNOME/sources/%name/%{name}-%{version}.tar.bz2
License: GPL
Group: Graphical desktop/GNOME
Url: http://ignore-your.tv/fusa/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: gnome-panel-devel
BuildRequires: perl-XML-Parser
BuildRequires: gnome-doc-utils
BuildRequires: avahi-glib-devel avahi-client-devel
BuildRequires: libxslt-proc
BuildRequires: libxmu-devel
Requires(post): scrollkeeper
Requires(postun): scrollkeeper

%description
The Fast User-Switching Applet is an applet for the GNOME panel which
provides a menu to switch between users. It integrates with GDM to switch
between existing X11 sessions or create new ones as needed, and will show
the same users as the GDM face browser.

%prep
%setup -q -n %{name}-%{version}

%build
%configure2_5x	--with-users-admin=/usr/bin/userdrake \
		--with-gdm-setup=/usr/bin/gdmsetup \
		--with-gdm-config=/etc/X11/gdm/gdm.conf --disable-scrollkeeper
%make

%install
rm -rf $RPM_BUILD_ROOT %name.lang
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std

%find_lang %name
for omf in %buildroot%_datadir/omf/*/*-{??,??_??}.omf;do
echo "%lang($(basename $omf|sed -e s/.*-// -e s/.omf//)) $(echo $omf|sed s!%buildroot!!)" >> %name.lang
done

%clean
rm -rf $RPM_BUILD_ROOT

%post
%post_install_gconf_schemas %name
%update_scrollkeeper

%preun
%preun_uninstall_gconf_schemas %name

%postun
%clean_scrollkeeper


%files -f %name.lang
%defattr(-,root,root)
%doc NEWS AUTHORS ChangeLog
%_sysconfdir/gconf/schemas/%name.schemas
%_libdir/bonobo/servers/GNOME_FastUserSwitchApplet.server
%_libexecdir/%name
%_datadir/%name
%_datadir/gnome-2.0/ui/GNOME_FastUserSwitchApplet.xml
%_datadir/gnome/help/%name/
%dir %_datadir/omf/%name/
%_datadir/omf/%name/*-C.omf


