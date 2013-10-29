# TODO:
#  - provide proper $DISPLAY for PGO (Xvfb, Xdummy...) for unattended builds
#
# Conditional build:
%bcond_with	tests		# enable tests (whatever they check)
%bcond_without	kerberos	# disable krb5 support
%bcond_without	xulrunner	# build with system xulrunner
%bcond_with	pgo		# PGO-enabled build (requires working $DISPLAY == :100)

# convert firefox release number to platform version: 19.0.x -> 19.0.x
%define		xulrunner_main	23.0.1
%define		xulrunner_ver	%(v=%{version}; echo %{xulrunner_main}${v#23.0.1})

%if %{without xulrunner}
# The actual sqlite version (see RHBZ#480989):
%define		sqlite_build_version %(pkg-config --silence-errors --modversion sqlite3 2>/dev/null || echo ERROR)
%endif

%define		nspr_ver	4.9.5
%define		nss_ver		3.14.3

Summary:	Iceweasel web browser
Summary(hu.UTF-8):	Iceweasel web böngésző
Summary(pl.UTF-8):	Iceweasel - przeglądarka WWW
Name:		iceweasel
Version:	25.0
Release:	1
License:	MPL 1.1 or GPL v2+ or LGPL v2.1+
Group:		X11/Applications/Networking
Source0:	http://releases.mozilla.org/pub/mozilla.org/firefox/releases/%{version}/source/firefox-%{version}.source.tar.bz2
# Source0-md5:	90ac047e83079a9046192c732e195329
Source1:	%{name}-branding.tar.bz2
# Source1-md5:	513af080c920d916362b607a872adf00
Source2:	%{name}-rm_nonfree.sh
Source3:	%{name}.desktop
Source4:	%{name}.sh
Source5:	vendor.js
Source6:	vendor-ac.js
Patch0:		%{name}-branding.patch
Patch2:		%{name}-gcc3.patch
Patch7:		%{name}-prefs.patch
Patch8:		%{name}-pld-branding.patch
Patch9:		%{name}-no-subshell.patch

Patch11:	%{name}-middle_click_paste.patch
Patch12:	%{name}-packaging.patch
# Edit patch below and restore --system-site-packages when system virtualenv gets 1.7 upgrade
Patch13:	system-virtualenv.patch
Patch14:	gyp-slashism.patch
Patch15:	Disable-Firefox-Health-Report.patch
URL:		http://www.pld-linux.org/Packages/Iceweasel
BuildRequires:	GConf2-devel >= 1.2.1
BuildRequires:	OpenGL-devel
BuildRequires:	ImageMagick
BuildRequires:	ImageMagick-coder-png
BuildRequires:	alsa-lib-devel
BuildRequires:	automake
BuildRequires:	bzip2-devel
BuildRequires:	cairo-devel >= 1.10.2-5
BuildRequires:	dbus-glib-devel >= 0.60
BuildRequires:	glib2-devel >= 1:2.20
BuildRequires:	gtk+2-devel >= 2:2.14
%{?with_kerberos:BuildRequires:	heimdal-devel >= 0.7.1}
BuildRequires:	hunspell-devel
BuildRequires:	libIDL-devel >= 0.8.0
BuildRequires:	libdnet-devel
BuildRequires:	libevent-devel >= 1.4.7
# standalone libffi 3.0.9 or gcc's from 4.5(?)+
BuildRequires:	libffi-devel >= 6:3.0.9
BuildRequires:	libiw-devel
# requires libjpeg-turbo implementing at least libjpeg 6b API
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	libjpeg-turbo-devel
BuildRequires:	libnotify-devel >= 0.4
BuildRequires:	libpng(APNG)-devel >= 0.10
BuildRequires:	libpng-devel >= 1.5.13
BuildRequires:	libstdc++-devel
BuildRequires:	libvpx-devel >= 1.0.0
BuildRequires:	nspr-devel >= 1:%{nspr_ver}
BuildRequires:	nss-devel >= 1:%{nss_ver}
BuildRequires:	pango-devel >= 1:1.14.0
BuildRequires:	perl-modules >= 5.004
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(libffi) >= 3.0.9
BuildRequires:	python-modules
%{?with_pgo:BuildRequires:	python-modules-sqlite}
BuildRequires:	python-virtualenv
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpmbuild(macros) >= 1.601
BuildRequires:	sqlite3-devel >= 3.7.15.2
BuildRequires:	startup-notification-devel >= 0.8
BuildRequires:	xorg-lib-libXScrnSaver-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXt-devel
%if %{with xulrunner}
BuildRequires:	xulrunner-devel >= 2:%{xulrunner_ver}
%endif
BuildRequires:	zip
BuildRequires:	zlib-devel >= 1.2.3
Requires(post):	mktemp >= 1.5-18
Requires:	desktop-file-utils
Requires:	hicolor-icon-theme
%if %{with xulrunner}
%requires_eq_to	xulrunner xulrunner-devel
%else
Requires:	browser-plugins >= 2.0
Requires:	cairo >= 1.10.2-5
Requires:	dbus-glib >= 0.60
Requires:	glib2 >= 1:2.20
Requires:	gtk+2 >= 2:2.14
Requires:	libjpeg-turbo
Requires:	libpng >= 1.5.13
Requires:	libpng(APNG) >= 0.10
Requires:	myspell-common
Requires:	nspr >= 1:%{nspr_ver}
Requires:	nss >= 1:%{nss_ver}
Requires:	pango >= 1:1.14.0
Requires:	sqlite3 >= %{sqlite_build_version}
Requires:	startup-notification >= 0.8
%endif
Provides:	wwwbrowser
Obsoletes:	mozilla-firebird
Obsoletes:	mozilla-firefox
Obsoletes:	mozilla-firefox-lang-en < 2.0.0.8-3
Obsoletes:	mozilla-firefox-libs
Conflicts:	iceweasel-lang-resources < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		filterout_cpp		-D_FORTIFY_SOURCE=[0-9]+

# don't satisfy other packages
%define		_noautoprovfiles	%{_libdir}/%{name}
%if %{without xulrunner}
# and as we don't provide them, don't require either
%define		_noautoreq	libmozalloc.so libmozjs.so libxpcom.so libxul.so
%endif

%description
Iceweasel is an open-source web browser, designed for standards
compliance, performance and portability.

%description -l hu.UTF-8
Iceweasel egy nyílt forrású webböngésző, hatékonyságra és
hordozhatóságra tervezve.

%description -l pl.UTF-8
Iceweasel jest przeglądarką WWW rozpowszechnianą zgodnie z ideami
ruchu otwartego oprogramowania oraz tworzoną z myślą o zgodności ze
standardami, wydajnością i przenośnością.

%prep
%setup -qc
mv -f mozilla-release mozilla
%setup -q -T -D -a1
cd mozilla
/bin/sh %{SOURCE2}

%patch0 -p1

%if "%{cc_version}" < "3.4"
%patch2 -p2
%endif

%patch7 -p1
%patch8 -p1
%patch9 -p2

%patch11 -p2
%patch12 -p2
%patch13 -p2
%patch14 -p2
%patch15 -p1

# config/rules.mk is patched by us and js/src/config/rules.mk
# is supposed to be exact copy
cp -a config/rules.mk js/src/config/rules.mk

%if %{with pgo}
sed -i -e 's@__BROWSER_PATH__@"../../dist/bin/iceweasel-bin"@' build/automation.py.in
%endif

%build
cd mozilla
cp -f %{_datadir}/automake/config.* build/autoconf

cat << EOF > .mozconfig
. \$topsrcdir/browser/config/mozconfig

mk_add_options MOZ_OBJDIR=@TOPSRCDIR@/obj-%{_target_cpu}
# parallel build fails on _xpidlgen/
%if %{without xulrunner}
mk_add_options MOZ_MAKE_FLAGS=%{_smp_mflags}
%endif
mk_add_options PROFILE_GEN_SCRIPT='@PYTHON@ @MOZ_OBJDIR@/_profile/pgo/profileserver.py'

# Options for 'configure' (same as command-line options).
ac_add_options --build=%{_target_platform}
ac_add_options --host=%{_target_platform}
ac_add_options --prefix=%{_prefix}
ac_add_options --exec-prefix=%{_exec_prefix}
ac_add_options --bindir=%{_bindir}
ac_add_options --sbindir=%{_sbindir}
ac_add_options --sysconfdir=%{_sysconfdir}
ac_add_options --datadir=%{_datadir}
ac_add_options --includedir=%{_includedir}
ac_add_options --libdir=%{_libdir}
ac_add_options --libexecdir=%{_libexecdir}
ac_add_options --localstatedir=%{_localstatedir}
ac_add_options --sharedstatedir=%{_sharedstatedir}
ac_add_options --mandir=%{_mandir}
ac_add_options --infodir=%{_infodir}
%if %{?debug:1}0
ac_add_options --disable-optimize
ac_add_options --enable-debug
ac_add_options --enable-debug-modules
ac_add_options --enable-debugger-info-modules
ac_add_options --enable-crash-on-assert
%else
ac_add_options --disable-debug
ac_add_options --disable-debug-modules
ac_add_options --disable-logging
ac_add_options --enable-optimize="%{rpmcflags} -Os"
%endif
ac_add_options --disable-strip
ac_add_options --disable-strip-libs
ac_add_options --disable-install-strip
%if %{with tests}
ac_add_options --enable-tests
%else
ac_add_options --disable-tests
%endif
%if %{with xulrunner}
ac_add_options --with-libxul-sdk=$(pkg-config --variable=sdkdir libxul)
%endif
ac_add_options --disable-crashreporter
ac_add_options --disable-elf-dynstr-gc
ac_add_options --disable-gconf
ac_add_options --disable-gnomeui
ac_add_options --disable-gnomevfs
ac_add_options --disable-installer
ac_add_options --disable-javaxpcom
ac_add_options --disable-long-long-warning
ac_add_options --disable-pedantic
ac_add_options --disable-updater
ac_add_options --disable-xterm-updates
ac_add_options --enable-canvas
ac_add_options --enable-default-toolkit=cairo-gtk2
ac_add_options --enable-extensions="default,permissions,gio"
ac_add_options --enable-gio
ac_add_options --enable-libxul
ac_add_options --enable-mathml
ac_add_options --enable-pango
ac_add_options --enable-readline
ac_add_options --enable-shared-js
ac_add_options --enable-startup-notification
ac_add_options --enable-svg
ac_add_options --enable-system-cairo
ac_add_options --enable-system-ffi
ac_add_options --enable-system-hunspell
ac_add_options --enable-system-sqlite
ac_add_options --enable-url-classifier
ac_add_options --with-branding=iceweasel/branding
ac_add_options --with-default-mozilla-five-home=%{_libdir}/%{name}
ac_add_options --with-distribution-id=org.pld-linux
ac_add_options --with-pthreads
ac_add_options --with-system-bz2
ac_add_options --with-system-jpeg
ac_add_options --with-system-libevent
ac_add_options --with-system-libvpx
ac_add_options --with-system-nspr
ac_add_options --with-system-nss
ac_add_options --with-system-ply
ac_add_options --with-system-png
ac_add_options --with-system-zlib
ac_add_options --with-x
EOF

%if %{with pgo}
export DISPLAY=:100
%{__make} -f client.mk profiledbuild \
	DESTDIR=obj-%{_target_cpu}/dist \
	STRIP="/bin/true" \
	CC="%{__cc}" \
	CXX="%{__cxx}"
%else
%{__make} -f client.mk build \
	STRIP="/bin/true" \
	CC="%{__cc}" \
	CXX="%{__cxx}"
%endif

%install
rm -rf $RPM_BUILD_ROOT
cd mozilla
install -d \
	$RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_libdir}} \
	$RPM_BUILD_ROOT%{_desktopdir} \
	$RPM_BUILD_ROOT%{_datadir}/%{name}/browser \
	$RPM_BUILD_ROOT%{_libdir}/%{name}/browser/plugins \

%browser_plugins_add_browser %{name} -p %{_libdir}/%{name}/browser/plugins

cd obj-%{_target_cpu}
%{__make} -C browser/installer stage-package \
	DESTDIR=$RPM_BUILD_ROOT \
	installdir=%{_libdir}/%{name} \
	PKG_SKIP_STRIP=1

%{__make} -C iceweasel/branding install \
	DESTDIR=$RPM_BUILD_ROOT

cp -a dist/iceweasel/* $RPM_BUILD_ROOT%{_libdir}/%{name}/

%if %{with xulrunner}
# >= 5.0 seems to require this
ln -s ../xulrunner $RPM_BUILD_ROOT%{_libdir}/%{name}/xulrunner
%endif

# move arch independant ones to datadir
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/browser/chrome $RPM_BUILD_ROOT%{_datadir}/%{name}/browser/chrome
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/browser/icons $RPM_BUILD_ROOT%{_datadir}/%{name}/browser/icons
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/browser/searchplugins $RPM_BUILD_ROOT%{_datadir}/%{name}/browser/searchplugins
%if %{without xulrunner}
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/defaults $RPM_BUILD_ROOT%{_datadir}/%{name}/browser/defaults
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/browser/defaults/{pref,preferences}
%else
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/browser/defaults $RPM_BUILD_ROOT%{_datadir}/%{name}/browser/defaults
%endif

ln -s ../../../share/%{name}/browser/chrome $RPM_BUILD_ROOT%{_libdir}/%{name}/browser/chrome
ln -s ../../../share/%{name}/browser/icons $RPM_BUILD_ROOT%{_libdir}/%{name}/browser/icons
ln -s ../../../share/%{name}/browser/searchplugins $RPM_BUILD_ROOT%{_libdir}/%{name}/browser/searchplugins
ln -s ../../../%{_lib}/%{name}/browser/extensions $RPM_BUILD_ROOT%{_datadir}/%{name}/browser/extensions
ln -s ../../../share/%{name}/browser/defaults $RPM_BUILD_ROOT%{_libdir}/%{name}/browser/defaults

%if %{without xulrunner}
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/%{name}/dictionaries
ln -s %{_datadir}/myspell $RPM_BUILD_ROOT%{_libdir}/%{name}/dictionaries
%endif

sed 's,@LIBDIR@,%{_libdir},' %{SOURCE4} > $RPM_BUILD_ROOT%{_bindir}/iceweasel
chmod 755 $RPM_BUILD_ROOT%{_bindir}/iceweasel
ln -s iceweasel $RPM_BUILD_ROOT%{_bindir}/firefox
ln -s iceweasel $RPM_BUILD_ROOT%{_bindir}/mozilla-firefox

# install icons and desktop file
cp iceweasel/branding/{mozicon,default}128.png
for i in 16 32 48 64 128; do
	install -d $RPM_BUILD_ROOT%{_iconsdir}/hicolor/${i}x${i}/apps
	cp -a iceweasel/branding/default${i}.png \
		$RPM_BUILD_ROOT%{_iconsdir}/hicolor/${i}x${i}/apps/iceweasel.png
done

cp -a %{SOURCE3} $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

# install our settings
cp -a %{SOURCE5} $RPM_BUILD_ROOT%{_datadir}/%{name}/browser/defaults/preferences/vendor.js

%if "%{pld_release}" == "ac"
cp -a %{SOURCE6} $RPM_BUILD_ROOT%{_datadir}/%{name}/browser/defaults/preferences/vendor.js
%endif

# files created by iceweasel -register
touch $RPM_BUILD_ROOT%{_libdir}/%{name}/browser/components/compreg.dat
touch $RPM_BUILD_ROOT%{_libdir}/%{name}/browser/components/xpti.dat

cat << 'EOF' > $RPM_BUILD_ROOT%{_sbindir}/%{name}-chrome+xpcom-generate
#!/bin/sh
umask 022
rm -f %{_libdir}/%{name}/browser/components/{compreg,xpti}.dat

# it attempts to touch files in $HOME/.mozilla
# beware if you run this with sudo!!!
export HOME=$(mktemp -d)
# also TMPDIR could be pointing to sudo user's homedir
unset TMPDIR TMP || :

%{_libdir}/%{name}/iceweasel -register

rm -rf $HOME
EOF
chmod 755 $RPM_BUILD_ROOT%{_sbindir}/%{name}-chrome+xpcom-generate

%clean
rm -rf $RPM_BUILD_ROOT

%pretrans
if [ -d %{_datadir}/%{name}/extensions ] && [ ! -L %{_datadir}/%{name}/browser/extensions ]; then
	install -d %{_libdir}/%{name}/browser
	mv -v %{_datadir}/%{name}/extensions %{_libdir}/%{name}/browser/extensions
fi
if [ -d %{_libdir}/%{name}/dictionaries ] && [ ! -L %{_libdir}/%{name}/dictionaries ]; then
	mv -v %{_libdir}/%{name}/dictionaries{,.rpmsave}
fi
exit 0

%post
%{_sbindir}/%{name}-chrome+xpcom-generate
%update_browser_plugins
%update_icon_cache hicolor
%update_desktop_database

%postun
if [ "$1" = 0 ]; then
	%update_browser_plugins
	%update_icon_cache hicolor
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/firefox
%attr(755,root,root) %{_bindir}/mozilla-firefox
%attr(755,root,root) %{_sbindir}/%{name}-chrome+xpcom-generate

# browser plugins v2
%{_browserpluginsconfdir}/browsers.d/%{name}.*
%config(noreplace) %verify(not md5 mtime size) %{_browserpluginsconfdir}/blacklist.d/%{name}.*.blacklist

%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/browser
%dir %{_libdir}/%{name}/browser/components
%dir %{_libdir}/%{name}/browser/extensions
%dir %{_libdir}/%{name}/browser/plugins

%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/browser
%{_datadir}/%{name}/browser/chrome
%{_datadir}/%{name}/browser/icons
%{_datadir}/%{name}/browser/searchplugins

# symlinks
%{_datadir}/%{name}/browser/extensions
%{_libdir}/%{name}/browser/chrome
%{_libdir}/%{name}/browser/icons
%{_libdir}/%{name}/browser/searchplugins
%if %{with xulrunner}
%{_libdir}/%{name}/xulrunner
%endif
%{_libdir}/%{name}/browser/defaults
%{_datadir}/%{name}/browser/defaults

%{_libdir}/%{name}/application.ini
%{_libdir}/%{name}/browser/blocklist.xml
%{_libdir}/%{name}/browser/chrome.manifest
# the signature of the default theme
%{_libdir}/%{name}/browser/extensions/{972ce4c6-7e08-4474-a285-3208198ce6fd}
%{_libdir}/%{name}/browser/omni.ja
%{_libdir}/%{name}/browser/components/components.manifest
%attr(755,root,root) %{_libdir}/%{name}/browser/components/libbrowsercomps.so
%attr(755,root,root) %{_libdir}/%{name}/iceweasel
%attr(755,root,root) %{_libdir}/%{name}/iceweasel-bin
%attr(755,root,root) %{_libdir}/%{name}/run-mozilla.sh
%{_libdir}/%{name}/webapprt
%attr(755,root,root) %{_libdir}/%{name}/webapprt-stub

%{_iconsdir}/hicolor/*/*/iceweasel.png
%{_desktopdir}/iceweasel.desktop

# files created by iceweasel -register
%ghost %{_libdir}/%{name}/browser/components/compreg.dat
%ghost %{_libdir}/%{name}/browser/components/xpti.dat

%if %{with crashreporter}
%{_libdir}/%{name}/crashreporter
%{_libdir}/%{name}/crashreporter-override.ini
%{_libdir}/%{name}/crashreporter.ini
%{_libdir}/%{name}/Throbber-small.gif
%endif

%if %{without xulrunner}
%{_libdir}/%{name}/dependentlibs.list
%{_libdir}/%{name}/platform.ini
%dir %{_libdir}/%{name}/components
%{_libdir}/%{name}/components/components.manifest
%attr(755,root,root) %{_libdir}/%{name}/components/libdbusservice.so
%attr(755,root,root) %{_libdir}/%{name}/components/libmozgnome.so
%attr(755,root,root) %{_libdir}/%{name}/libmozalloc.so
%attr(755,root,root) %{_libdir}/%{name}/libmozjs.so
%attr(755,root,root) %{_libdir}/%{name}/libxul.so
%attr(755,root,root) %{_libdir}/%{name}/mozilla-xremote-client
%attr(755,root,root) %{_libdir}/%{name}/plugin-container
%{_libdir}/%{name}/dictionaries
%{_libdir}/%{name}/chrome.manifest
%{_libdir}/%{name}/omni.ja
%endif
