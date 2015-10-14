# TODO:
# - consider --enable-libproxy
#
# Conditional build:
%bcond_with	tests		# enable tests (whatever they check)
%bcond_with	gtk3		# GTK+ 3.x instead of 2.x
%bcond_without	kerberos	# disable krb5 support
%bcond_without	pgo		# PGO-enabled build (requires working $DISPLAY == :100)
# - disabled shared_js - https://bugzilla.mozilla.org/show_bug.cgi?id=1039964
%bcond_with	shared_js	# shared libmozjs library [broken]

# On updating version, grab CVE links from:
# https://www.mozilla.org/security/known-vulnerabilities/firefox.html

# The actual sqlite version (see RHBZ#480989):
%define		sqlite_build_version %(pkg-config --silence-errors --modversion sqlite3 2>/dev/null || echo ERROR)

%define		nspr_ver	4.10.8
%define		nss_ver		3.19.2

Summary:	Iceweasel web browser
Summary(hu.UTF-8):	Iceweasel web böngésző
Summary(pl.UTF-8):	Iceweasel - przeglądarka WWW
Name:		iceweasel
Version:	41.0.1
Release:	1
License:	MPL v2.0
Group:		X11/Applications/Networking
Source0:	http://releases.mozilla.org/pub/mozilla.org/firefox/releases/%{version}/source/firefox-%{version}.source.tar.xz
# Source0-md5:	d53d863642b34b446ee7600bdad000a1
Source1:	%{name}-branding.tar.xz
# Source1-md5:	aacc7e8298a3e6aa3ef2a3613a62f635
Source2:	%{name}-rm_nonfree.sh
Source3:	%{name}.desktop
Source4:	%{name}.sh
Source5:	vendor.js
Source6:	vendor-ac.js
Patch0:		%{name}-branding.patch
Patch1:		idl-parser.patch
Patch2:		xulrunner-new-libxul.patch
Patch3:		xulrunner-paths.patch
Patch4:		xulrunner-pc.patch
Patch5:		install-pc-files.patch
Patch6:		%{name}-prefs.patch
Patch7:		%{name}-pld-branding.patch
Patch8:		%{name}-no-subshell.patch
Patch9:		%{name}-middle_click_paste.patch
Patch10:	%{name}-packaging.patch
Patch11:	system-virtualenv.patch
Patch12:	Disable-Firefox-Health-Report.patch
Patch13:	no-logging.patch
Patch14:	freetype.patch
URL:		http://www.pld-linux.org/Packages/Iceweasel
BuildRequires:	OpenGL-devel
BuildRequires:	ImageMagick
BuildRequires:	ImageMagick-coder-png
BuildRequires:	alsa-lib-devel
BuildRequires:	automake
BuildRequires:	bzip2-devel
BuildRequires:	cairo-devel >= 1.10.2-5
BuildRequires:	dbus-glib-devel >= 0.60
BuildRequires:	freetype-devel >= 1:2.1.8
BuildRequires:	gcc-c++ >= 6:4.4
BuildRequires:	glib2-devel >= 1:2.22
BuildRequires:	gstreamer-devel >= 1.0
BuildRequires:	gstreamer-plugins-base-devel >= 1.0
%{!?with_gtk3:BuildRequires:	gtk+2-devel >= 2:2.18.0}
%{?with_gtk3:BuildRequires:	gtk+3-devel >= 3.4.0}
%{?with_kerberos:BuildRequires:	heimdal-devel >= 0.7.1}
BuildRequires:	hunspell-devel >= 1.2.3
BuildRequires:	libIDL-devel >= 0.8.0
# DECnet (dnprogs.spec), not dummy net (libdnet.spec)
#BuildRequires:	libdnet-devel
BuildRequires:	libevent-devel >= 1.4.7
# standalone libffi 3.0.9 or gcc's from 4.5(?)+
BuildRequires:	libffi-devel >= 6:3.0.9
BuildRequires:	libicu-devel >= 50.1
# requires libjpeg-turbo implementing at least libjpeg 6b API
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	libjpeg-turbo-devel
# for rsvg-convert
BuildRequires:	librsvg
BuildRequires:	libpng(APNG)-devel >= 0.10
BuildRequires:	libpng-devel >= 2:1.6.16
BuildRequires:	libstdc++-devel >= 6:4.4
BuildRequires:	libvpx-devel >= 1.3.0
BuildRequires:	nspr-devel >= 1:%{nspr_ver}
BuildRequires:	nss-devel >= 1:%{nss_ver}
BuildRequires:	pango-devel >= 1:1.22.0
BuildRequires:	pixman-devel >= 0.19.2
BuildRequires:	perl-modules >= 5.004
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(libffi) >= 3.0.9
BuildRequires:	pulseaudio-devel
BuildRequires:	python-modules >= 1:2.5
%{?with_pgo:BuildRequires:	python-modules-sqlite}
BuildRequires:	python-simplejson
BuildRequires:	python-virtualenv >= 1.9.1-4
BuildRequires:	readline-devel
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpmbuild(macros) >= 1.601
BuildRequires:	sed >= 4.0
BuildRequires:	sqlite3-devel >= 3.8.11.1-3
BuildRequires:	startup-notification-devel >= 0.8
BuildRequires:	xorg-lib-libXScrnSaver-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXt-devel
%{?with_pgo:BuildRequires:	xorg-xserver-Xvfb}
BuildRequires:	zip
BuildRequires:	zlib-devel >= 1.2.3
BuildConflicts:	%{name}-devel < %{version}
Requires(post):	mktemp >= 1.5-18
Requires:	browser-plugins >= 2.0
Requires:	desktop-file-utils
Requires:	hicolor-icon-theme
Requires:	myspell-common
Requires:	nspr >= 1:%{nspr_ver}
Requires:	nss >= 1:%{nss_ver}
Requires:	%{name}-libs = %{version}-%{release}
Provides:	wwwbrowser
Obsoletes:	mozilla-firebird
Obsoletes:	mozilla-firefox
Obsoletes:	mozilla-firefox-lang-en < 2.0.0.8-3
Obsoletes:	mozilla-firefox-libs
Obsoletes:	xulrunner
Obsoletes:	xulrunner-gnome
Conflicts:	iceweasel-lang-resources < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		filterout_cpp		-D_FORTIFY_SOURCE=[0-9]+

# don't satisfy other packages
%define		_noautoprovfiles	%{_libdir}/%{name}

# and as we don't provide them, don't require either
%define		_noautoreq	libmozjs.so libxul.so

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

%package libs
Summary:	Iceweasel shared libraries
Summary(pl.UTF-8):	Biblioteki współdzielone Iceweasela
Group:		X11/Libraries
Requires:	cairo >= 1.10.2-5
Requires:	dbus-glib >= 0.60
Requires:	glib2 >= 1:2.22
%{!?with_gtk3:Requires:	gtk+2 >= 2:2.18.0}
%{?with_gtk3:Requires:	gtk+3 >= 3.4.0}
Requires:	libjpeg-turbo
Requires:	libpng >= 2:1.6.16
Requires:	libpng(APNG) >= 0.10
Requires:	libvpx >= 1.3.0
Requires:	pango >= 1:1.22.0
Requires:	sqlite3 >= %{sqlite_build_version}
Requires:	startup-notification >= 0.8
Provides:	xulrunner-libs = 2:%{version}-%{release}
Obsoletes:	xulrunner-libs

%description libs
XULRunner shared libraries.

%description libs -l pl.UTF-8
Biblioteki współdzielone XULRunnera.

%package devel
Summary:	Headers for developing programs that will use Iceweasel
Summary(pl.UTF-8):	Pliki nagłówkowe do tworzenia programów używających Iceweasel
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	nspr-devel >= 1:%{nspr_ver}
Requires:	nss-devel >= 1:%{nss_ver}
Requires:	python-ply
Provides:	xulrunner-devel = 2:%{version}-%{release}
Obsoletes:	mozilla-devel
Obsoletes:	mozilla-firefox-devel
Obsoletes:	seamonkey-devel
Obsoletes:	xulrunner-devel

%description devel
Iceweasel development package.

%description devel -l pl.UTF-8
Pakiet programistyczny Iceweasela.

%prep
%setup -qc
mv -f mozilla-release mozilla
%setup -q -T -D -a1
cd mozilla
/bin/sh %{SOURCE2}

# avoid using included headers (-I. is before HUNSPELL_CFLAGS)
%{__rm} extensions/spellcheck/hunspell/src/{*.hxx,hunspell.h}
# hunspell needed for factory including mozHunspell.h
echo 'LOCAL_INCLUDES += $(MOZ_HUNSPELL_CFLAGS)' >> extensions/spellcheck/src/Makefile.in

%patch0 -p1
%patch1 -p2
%patch2 -p1
%patch3 -p2
%patch4 -p1
%patch5 -p2
%patch6 -p1
%patch7 -p1
%patch8 -p2
%patch9 -p2
%patch10 -p1
%patch11 -p2
%patch12 -p1
%patch13 -p2
%patch14 -p2

cp -a xulrunner/installer/*.pc.in browser/installer/

%if %{with pgo}
sed -i -e 's@__BROWSER_PATH__@"../../dist/bin/iceweasel-bin"@' build/automation.py.in
%endif

%build
cd mozilla
cp -p %{_datadir}/automake/config.* build/autoconf

cat << 'EOF' > .mozconfig
. $topsrcdir/browser/config/mozconfig

mk_add_options MOZ_OBJDIR=@TOPSRCDIR@/obj-%{_target_cpu}

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
ac_add_options --enable-mochitest
%else
%if %{with pgo}
ac_add_options --enable-tests
%else
ac_add_options --disable-tests
%endif
ac_add_options --disable-mochitest
%endif
ac_add_options --disable-cpp-exceptions
ac_add_options --disable-crashreporter
ac_add_options --disable-elf-dynstr-gc
ac_add_options --disable-gconf
ac_add_options --disable-gnomeui
ac_add_options --disable-gnomevfs
ac_add_options --disable-installer
ac_add_options --disable-javaxpcom
ac_add_options --disable-long-long-warning
ac_add_options --disable-necko-wifi
ac_add_options --disable-pedantic
ac_add_options --disable-updater
ac_add_options --disable-xterm-updates
ac_add_options --enable-canvas
ac_add_options --enable-chrome-format=omni
ac_add_options --enable-default-toolkit=%{?with_gtk3:cairo-gtk3}%{!?with_gtk3:cairo-gtk2}
ac_add_options --enable-extensions=default
ac_add_options --enable-gio
ac_add_options --enable-gstreamer=1.0
ac_add_options --enable-libxul
ac_add_options --enable-mathml
ac_add_options --enable-pango
ac_add_options --enable-readline
ac_add_options --enable-safe-browsing
%{?with_shared_js:ac_add_options --enable-shared-js}
ac_add_options --enable-startup-notification
ac_add_options --enable-svg
ac_add_options --enable-system-cairo
ac_add_options --enable-system-ffi
ac_add_options --enable-system-hunspell
ac_add_options --enable-system-sqlite
ac_add_options --enable-url-classifier
ac_add_options --enable-xinerama
ac_add_options --with-branding=iceweasel/branding
ac_add_options --with-default-mozilla-five-home=%{_libdir}/%{name}
ac_add_options --with-distribution-id=org.pld-linux
ac_add_options --with-pthreads
ac_add_options --with-system-bz2
ac_add_options --with-system-icu
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
D=$(( RANDOM % (200 - 100 + 1 ) + 5 ))
/usr/bin/Xvfb :${D} &
XVFB_PID=$!
[ -n "$XVFB_PID" ] || exit 1
export DISPLAY=:${D}
%{__make} -j1 -f client.mk profiledbuild \
	DESTDIR=obj-%{_target_cpu}/dist \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	MOZ_MAKE_FLAGS="%{_smp_mflags}"
kill $XVFB_PID
%else
%{__make} -j1 -f client.mk build \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	MOZ_MAKE_FLAGS="%{_smp_mflags}"
%endif

%install
rm -rf $RPM_BUILD_ROOT
cd mozilla
install -d \
	$RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_libdir}} \
	$RPM_BUILD_ROOT%{_desktopdir} \
	$RPM_BUILD_ROOT%{_datadir}/%{name}/browser \
	$RPM_BUILD_ROOT%{_libdir}/%{name}/browser/plugins \
	$RPM_BUILD_ROOT%{_libdir}/%{name}-devel/sdk/{lib,bin} \
	$RPM_BUILD_ROOT%{_includedir}/%{name} \
	$RPM_BUILD_ROOT%{_datadir}/idl/%{name} \
	$RPM_BUILD_ROOT%{_pkgconfigdir}

%browser_plugins_add_browser %{name} -p %{_libdir}/%{name}/browser/plugins

cd obj-%{_target_cpu}
%{__make} -C browser/installer stage-package libxul.pc libxul-embedding.pc mozilla-js.pc mozilla-plugin.pc \
	DESTDIR=$RPM_BUILD_ROOT \
	installdir=%{_libdir}/%{name} \
	INSTALL_SDK=1 \
	PKG_SKIP_STRIP=1

%{__make} -C iceweasel/branding install \
	DESTDIR=$RPM_BUILD_ROOT

cp -aL browser/installer/*.pc $RPM_BUILD_ROOT%{_pkgconfigdir}
cp -aL dist/iceweasel/* $RPM_BUILD_ROOT%{_libdir}/%{name}/
cp -aL dist/idl/* $RPM_BUILD_ROOT%{_datadir}/idl/%{name}
cp -aL dist/include/* $RPM_BUILD_ROOT%{_includedir}/%{name}
cp -aL dist/include/xpcom-config.h $RPM_BUILD_ROOT%{_libdir}/%{name}-devel
cp -aL dist/sdk/lib/* $RPM_BUILD_ROOT%{_libdir}/%{name}-devel/sdk/lib
cp -aL dist/sdk/bin/* $RPM_BUILD_ROOT%{_libdir}/%{name}-devel/sdk/bin
find $RPM_BUILD_ROOT%{_libdir}/%{name}-devel/sdk -name "*.pyc" | xargs rm -f

ln -s %{_libdir}/%{name} $RPM_BUILD_ROOT%{_libdir}/%{name}-devel/bin
ln -s %{_includedir}/%{name} $RPM_BUILD_ROOT%{_libdir}/%{name}-devel/include
ln -s %{_datadir}/idl/%{name} $RPM_BUILD_ROOT%{_libdir}/%{name}-devel/idl
ln -s %{_libdir}/%{name}-devel/sdk/lib $RPM_BUILD_ROOT%{_libdir}/%{name}-devel/lib

# replace copies with symlinks
%{?with_shared_js:ln -sf %{_libdir}/%{name}/libmozjs.so $RPM_BUILD_ROOT%{_libdir}/%{name}-devel/sdk/lib/libmozjs.so}
ln -sf %{_libdir}/%{name}/libxul.so $RPM_BUILD_ROOT%{_libdir}/%{name}-devel/sdk/lib/libxul.so
# temp fix for https://bugzilla.mozilla.org/show_bug.cgi?id=63955
chmod a+rx $RPM_BUILD_ROOT%{_libdir}/%{name}-devel/sdk/bin/xpt.py

# move arch independant ones to datadir
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/browser/chrome $RPM_BUILD_ROOT%{_datadir}/%{name}/browser/chrome
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/browser/extensions $RPM_BUILD_ROOT%{_datadir}/%{name}/browser/extensions
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/browser/icons $RPM_BUILD_ROOT%{_datadir}/%{name}/browser/icons
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/defaults $RPM_BUILD_ROOT%{_datadir}/%{name}/browser/defaults
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/browser/defaults/{pref,preferences}

ln -s ../../../share/%{name}/browser/chrome $RPM_BUILD_ROOT%{_libdir}/%{name}/browser/chrome
ln -s ../../../share/%{name}/browser/defaults $RPM_BUILD_ROOT%{_libdir}/%{name}/browser/defaults
ln -s ../../../share/%{name}/browser/extensions $RPM_BUILD_ROOT%{_libdir}/%{name}/browser/extensions
ln -s ../../../share/%{name}/browser/icons $RPM_BUILD_ROOT%{_libdir}/%{name}/browser/icons

%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/%{name}/dictionaries
ln -s %{_datadir}/myspell $RPM_BUILD_ROOT%{_libdir}/%{name}/dictionaries

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
%if "%{pld_release}" == "ac"
cp -a %{SOURCE6} $RPM_BUILD_ROOT%{_datadir}/%{name}/browser/defaults/preferences/vendor.js
%else
cp -a %{SOURCE5} $RPM_BUILD_ROOT%{_datadir}/%{name}/browser/defaults/preferences/vendor.js
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
if [ -d %{_libdir}/%{name}/browser/extensions ] && [ ! -L %{_libdir}/%{name}/browser/extensions ]; then
	install -d %{_datadir}/%{name}/browser
	if [ -e %{_datadir}/%{name}/browser/extensions ]; then
		mv %{_datadir}/%{name}/browser/extensions{,.rpmsave}
	fi
	mv -v %{_libdir}/%{name}/browser/extensions %{_datadir}/%{name}/browser/extensions
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

%{_desktopdir}/iceweasel.desktop
%{_iconsdir}/hicolor/*/apps/iceweasel.png

# browser plugins v2
%{_browserpluginsconfdir}/browsers.d/%{name}.*
%config(noreplace) %verify(not md5 mtime size) %{_browserpluginsconfdir}/blacklist.d/%{name}.*.blacklist

%dir %{_libdir}/%{name}/browser
%dir %{_libdir}/%{name}/browser/components
%dir %{_libdir}/%{name}/browser/plugins

%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/browser
%dir %{_datadir}/%{name}/browser/extensions
%{_datadir}/%{name}/browser/chrome
%{_datadir}/%{name}/browser/defaults
%{_datadir}/%{name}/browser/icons

# symlinks
%{_libdir}/%{name}/browser/extensions
%{_libdir}/%{name}/browser/chrome
%{_libdir}/%{name}/browser/icons
%{_libdir}/%{name}/browser/defaults

%attr(755,root,root) %{_libdir}/%{name}/iceweasel
%attr(755,root,root) %{_libdir}/%{name}/iceweasel-bin
%attr(755,root,root) %{_libdir}/%{name}/run-mozilla.sh
%{_libdir}/%{name}/application.ini
%{_libdir}/%{name}/browser/blocklist.xml
%{_libdir}/%{name}/browser/chrome.manifest
%{_libdir}/%{name}/browser/components/components.manifest
%attr(755,root,root) %{_libdir}/%{name}/browser/components/libbrowsercomps.so
# the signature of the default theme
%{_datadir}/%{name}/browser/extensions/{972ce4c6-7e08-4474-a285-3208198ce6fd}
%{_libdir}/%{name}/browser/omni.ja
%{_libdir}/%{name}/webapprt
%attr(755,root,root) %{_libdir}/%{name}/webapprt-stub

# files created by iceweasel -register
%ghost %{_libdir}/%{name}/browser/components/compreg.dat
%ghost %{_libdir}/%{name}/browser/components/xpti.dat

# private xulrunner instance
%dir %{_libdir}/%{name}/components
%{_libdir}/%{name}/components/components.manifest
%attr(755,root,root) %{_libdir}/%{name}/components/libdbusservice.so
%attr(755,root,root) %{_libdir}/%{name}/components/libmozgnome.so
%attr(755,root,root) %{_libdir}/%{name}/plugin-container
%{_libdir}/%{name}/dictionaries
%{_libdir}/%{name}/chrome.manifest

%dir %{_libdir}/%{name}/gmp-clearkey
%dir %{_libdir}/%{name}/gmp-clearkey/0.1
%{_libdir}/%{name}/gmp-clearkey/0.1/clearkey.info
%attr(755,root,root) %{_libdir}/%{name}/gmp-clearkey/0.1/libclearkey.so

%files libs
%defattr(644,root,root,755)
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/platform.ini
%{?with_shared_js:%attr(755,root,root) %{_libdir}/%{name}/libmozjs.so}
%attr(755,root,root) %{_libdir}/%{name}/libxul.so
%{_libdir}/%{name}/dependentlibs.list
%{_libdir}/%{name}/omni.ja

%files devel
%defattr(644,root,root,755)
%{_includedir}/%{name}
%{_datadir}/idl/%{name}
%dir %{_libdir}/%{name}-devel
%{_libdir}/%{name}-devel/bin
%{_libdir}/%{name}-devel/idl
%{_libdir}/%{name}-devel/lib
%{_libdir}/%{name}-devel/include
%{_libdir}/%{name}-devel/*.h
%dir %{_libdir}/%{name}-devel/sdk
%{_libdir}/%{name}-devel/sdk/lib
%dir %{_libdir}/%{name}-devel/sdk/bin
%attr(755,root,root) %{_libdir}/%{name}-devel/sdk/bin/header.py
%attr(755,root,root) %{_libdir}/%{name}-devel/sdk/bin/run-mozilla.sh
%attr(755,root,root) %{_libdir}/%{name}-devel/sdk/bin/typelib.py
%attr(755,root,root) %{_libdir}/%{name}-devel/sdk/bin/xpcshell
%attr(755,root,root) %{_libdir}/%{name}-devel/sdk/bin/xpidl.py
%{_libdir}/%{name}-devel/sdk/bin/xpidllex.py
%{_libdir}/%{name}-devel/sdk/bin/xpidlyacc.py
%attr(755,root,root) %{_libdir}/%{name}-devel/sdk/bin/xpt.py
%{_libdir}/%{name}-devel/sdk/bin/ply

%{_pkgconfigdir}/libxul.pc
%{_pkgconfigdir}/libxul-embedding.pc
%{_pkgconfigdir}/mozilla-js.pc
%{_pkgconfigdir}/mozilla-plugin.pc
