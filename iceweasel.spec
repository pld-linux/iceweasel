#
# Conditional build:
%bcond_with	tests		# enable tests (whatever they check)
%bcond_without	gnomeui		# disable gnomeui support
%bcond_without	gnomevfs	# disable GNOME comp. (gconf+libgnome+gnomevfs) and gnomevfs ext.
%bcond_without	gnome		# disable all GNOME components (gnome+gnomeui+gnomevfs)
%bcond_without	kerberos	# disable krb5 support
%if "%{pld_release}" == "ti"
%bcond_with	xulrunner	# build with system xulrunner
%else
%bcond_without	xulrunner	# build with system xulrunner
%endif

%if %{without gnome}
%undefine	with_gnomeui
%undefine	with_gnomevfs
%endif

# convert firefox release number to platform version: 3.6.x -> 1.9.2.x
%define		xulrunner_main	1.9.2
%define		xulrunner_ver	%(v=%{version}; echo %{xulrunner_main}${v#3.6})

%if %{without xulrunner}
# The actual sqlite version (see RHBZ#480989):
%define		sqlite_build_version %(pkg-config --silence-errors --modversion sqlite3 2>/dev/null || echo ERROR)
%endif

Summary:	Iceweasel web browser
Summary(hu.UTF-8):	Iceweasel web böngésző
Summary(pl.UTF-8):	Iceweasel - przeglądarka WWW
Name:		iceweasel
Version:	3.6.14
Release:	1
License:	MPL 1.1 or GPL v2+ or LGPL v2.1+
Group:		X11/Applications/Networking
Source0:	ftp://ftp.mozilla.org/pub/mozilla.org/firefox/releases/%{version}/source/firefox-%{version}.source.tar.bz2
# Source0-md5:	ab0d00cd33e6b2388429dda1c01abd01
Source1:	%{name}-branding.tar.bz2
# Source1-md5:	b49feae9f6434eca8a749776160c15a8
Source2:	%{name}-rm_nonfree.sh
Source3:	%{name}.desktop
Source4:	%{name}.sh
Patch0:		%{name}-branding.patch
Patch1:		%{name}-install.patch
Patch2:		%{name}-gcc3.patch
Patch3:		%{name}-agent.patch
Patch4:		%{name}-ac-agent.patch
Patch5:		%{name}-ti-agent.patch
Patch6:		%{name}-nss_cflags.patch
Patch7:		%{name}-prefs.patch
Patch8:		%{name}-pld-branding.patch
Patch9:		%{name}-no-subshell.patch
Patch10:	%{name}-ppc.patch
Patch11:	%{name}-libpng.patch
URL:		http://www.pld-linux.org/Packages/Iceweasel
%{?with_gnomevfs:BuildRequires:	GConf2-devel >= 1.2.1}
BuildRequires:	alsa-lib-devel
BuildRequires:	automake
BuildRequires:	bzip2-devel
BuildRequires:	cairo-devel >= 1.8.8
BuildRequires:	dbus-glib-devel >= 0.60
%{?with_gnomevfs:BuildRequires:	gnome-vfs2-devel >= 2.0}
BuildRequires:	gtk+2-devel >= 2:2.10
%{?with_kerberos:BuildRequires:	heimdal-devel >= 0.7.1}
BuildRequires:	hunspell-devel
BuildRequires:	libIDL-devel >= 0.8.0
BuildRequires:	libdnet-devel
%{?with_gnomevfs:BuildRequires:	libgnome-devel >= 2.0}
%{?with_gnomeui:BuildRequires:	libgnomeui-devel >= 2.2.0}
BuildRequires:	libiw-devel
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	libnotify-devel >= 0.4
BuildRequires:	libpng(APNG)-devel >= 0.10
BuildRequires:	libpng-devel >= 1.2.17
BuildRequires:	libstdc++-devel
BuildRequires:	nspr-devel >= 1:4.8.6
BuildRequires:	nss-devel >= 1:3.12.8
BuildRequires:	pango-devel >= 1:1.14.0
BuildRequires:	perl-modules >= 5.004
BuildRequires:	pkgconfig
BuildRequires:	python-modules
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpmbuild(macros) >= 1.453
BuildRequires:	sqlite3-devel >= 3.7.2
BuildRequires:	startup-notification-devel >= 0.8
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXft-devel >= 2.1
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXp-devel
BuildRequires:	xorg-lib-libXt-devel
%if %{with xulrunner}
BuildRequires:	xulrunner-devel >= 2:%{xulrunner_ver}
%endif
BuildRequires:	zip
BuildRequires:	zlib-devel >= 1.2.3
Requires(post):	mktemp >= 1.5-18
%if %{with xulrunner}
%requires_eq_to	xulrunner xulrunner-devel
%else
Requires:	browser-plugins >= 2.0
Requires:	cairo >= 1.8.8
Requires:	dbus-glib >= 0.60
Requires:	gtk+2 >= 2:2.18
Requires:	libpng(APNG) >= 0.10
Requires:	myspell-common
Requires:	nspr >= 1:4.8.6
Requires:	nss >= 1:3.12.8
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
# and as we don't provide them, don't require either
%define		_noautoreq	libmozjs.so libxpcom.so libxul.so libjemalloc.so

%if "%{cc_version}" >= "3.4"
%define		specflags	-fno-strict-aliasing -fomit-frame-pointer -fno-tree-vrp -fno-stack-protector
%else
%define		specflags	-fno-strict-aliasing -fomit-frame-pointer
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
mv -f mozilla-%{xulrunner_main} mozilla
%setup -q -T -D -a1
cd mozilla
/bin/sh %{SOURCE2}

%patch0 -p1
%patch1 -p1

%if "%{cc_version}" < "3.4"
%patch2 -p2
%endif

%if "%{pld_release}" == "th"
%patch3 -p1
%endif

%if "%{pld_release}" == "ac"
%patch4 -p1
%endif

%if "%{pld_release}" == "ti"
%patch5 -p1
%endif

%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p2
%patch10 -p1
%patch11 -p0

%build
cd mozilla
cp -f %{_datadir}/automake/config.* build/autoconf

cat << EOF > .mozconfig
. \$topsrcdir/browser/config/mozconfig

mk_add_options MOZ_OBJDIR=@TOPSRCDIR@/obj-%{_target_cpu}

# Options for 'configure' (same as command-line options).
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
%if %{with tests}
ac_add_options --enable-tests
%else
ac_add_options --disable-tests
%endif
%if %{with gnomeui}
ac_add_options --enable-gnomeui
%else
ac_add_options --disable-gnomeui
%endif
%if %{with gnomevfs}
ac_add_options --enable-gnomevfs
%else
ac_add_options --disable-gnomevfs
%endif
ac_add_options --disable-crashreporter
ac_add_options --disable-installer
ac_add_options --disable-javaxpcom
ac_add_options --disable-updater
ac_add_options --disable-xprint
ac_add_options --enable-canvas
ac_add_options --enable-libxul
ac_add_options --enable-pango
ac_add_options --enable-startup-notification
ac_add_options --enable-svg
ac_add_options --enable-system-cairo
ac_add_options --enable-system-hunspell
ac_add_options --enable-system-sqlite
ac_add_options --enable-xinerama
ac_add_options --with-distribution-id=org.pld-linux
ac_add_options --with-branding=iceweasel/branding
%if %{with xulrunner}
ac_add_options --with-libxul-sdk=$(pkg-config --variable=sdkdir libxul)
%endif
ac_add_options --with-pthreads
ac_add_options --with-system-bz2
ac_add_options --with-system-jpeg
ac_add_options --with-system-nspr
ac_add_options --with-system-nss
ac_add_options --with-system-png
ac_add_options --with-system-zlib
ac_add_options --with-default-mozilla-five-home=%{_libdir}/%{name}
EOF

%{__make} -f client.mk build \
	STRIP="/bin/true" \
	CC="%{__cc}" \
	CXX="%{__cxx}"

%install
rm -rf $RPM_BUILD_ROOT
cd mozilla
install -d \
	$RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_libdir}} \
	$RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir}} \
	$RPM_BUILD_ROOT%{_datadir}/%{name}

%browser_plugins_add_browser %{name} -p %{_libdir}/%{name}/plugins

%{__make} -C obj-%{_target_cpu}/browser/installer stage-package \
	DESTDIR=$RPM_BUILD_ROOT \
	MOZ_PKG_APPDIR=%{_libdir}/%{name} \
	PKG_SKIP_STRIP=1

install -d \
	$RPM_BUILD_ROOT%{_libdir}/%{name}/plugins

# move arch independant ones to datadir
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome $RPM_BUILD_ROOT%{_datadir}/%{name}/chrome
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/defaults $RPM_BUILD_ROOT%{_datadir}/%{name}/defaults
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/extensions $RPM_BUILD_ROOT%{_datadir}/%{name}/extensions
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/icons $RPM_BUILD_ROOT%{_datadir}/%{name}/icons
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/modules $RPM_BUILD_ROOT%{_datadir}/%{name}/modules
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/searchplugins $RPM_BUILD_ROOT%{_datadir}/%{name}/searchplugins
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/browserconfig.properties $RPM_BUILD_ROOT%{_datadir}/%{name}
%if %{without xulrunner}
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/greprefs $RPM_BUILD_ROOT%{_datadir}/%{name}/greprefs
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/res $RPM_BUILD_ROOT%{_datadir}/%{name}/res
%endif

ln -s ../../share/%{name}/chrome $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome
ln -s ../../share/%{name}/defaults $RPM_BUILD_ROOT%{_libdir}/%{name}/defaults
ln -s ../../share/%{name}/extensions $RPM_BUILD_ROOT%{_libdir}/%{name}/extensions
ln -s ../../share/%{name}/modules $RPM_BUILD_ROOT%{_libdir}/%{name}/modules
ln -s ../../share/%{name}/icons $RPM_BUILD_ROOT%{_libdir}/%{name}/icons
ln -s ../../share/%{name}/searchplugins $RPM_BUILD_ROOT%{_libdir}/%{name}/searchplugins
ln -s ../../share/%{name}/browserconfig.properties $RPM_BUILD_ROOT%{_libdir}/%{name}
%if %{without xulrunner}
ln -s ../../share/%{name}/greprefs $RPM_BUILD_ROOT%{_libdir}/%{name}/greprefs
ln -s ../../share/%{name}/res $RPM_BUILD_ROOT%{_libdir}/%{name}/res
%endif

%if %{without xulrunner}
rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/dictionaries
ln -s %{_datadir}/myspell $RPM_BUILD_ROOT%{_libdir}/%{name}/dictionaries
%endif

sed 's,@LIBDIR@,%{_libdir},' %{SOURCE4} > $RPM_BUILD_ROOT%{_bindir}/iceweasel
chmod a+rx $RPM_BUILD_ROOT%{_bindir}/iceweasel
ln -s iceweasel $RPM_BUILD_ROOT%{_bindir}/firefox
ln -s iceweasel $RPM_BUILD_ROOT%{_bindir}/mozilla-firefox

cp -a iceweasel/branding/default64.png $RPM_BUILD_ROOT%{_pixmapsdir}/iceweasel.png
cp -a %{SOURCE3} $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

# files created by regxpcom and iceweasel -register
touch $RPM_BUILD_ROOT%{_libdir}/%{name}/components/compreg.dat
touch $RPM_BUILD_ROOT%{_libdir}/%{name}/components/xpti.dat

%if %{with xulrunner}
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/run-mozilla.sh
%endif
rm $RPM_BUILD_ROOT%{_libdir}/%{name}/LICENSE
rm $RPM_BUILD_ROOT%{_libdir}/%{name}/README.txt
rm $RPM_BUILD_ROOT%{_libdir}/%{name}/components/components.list

cat << 'EOF' > $RPM_BUILD_ROOT%{_sbindir}/%{name}-chrome+xpcom-generate
#!/bin/sh
umask 022
rm -f %{_libdir}/%{name}/components/{compreg,xpti}.dat

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
if [ -d %{_libdir}/%{name}/dictionaries ] && [ ! -L %{_libdir}/%{name}/dictionaries ]; then
	mv -v %{_libdir}/%{name}/dictionaries{,.rpmsave}
fi
for d in chrome defaults extensions greprefs icons res searchplugins; do
	if [ -d %{_libdir}/%{name}/$d ] && [ ! -L %{_libdir}/%{name}/$d ]; then
		install -d %{_datadir}/%{name}
		mv %{_libdir}/%{name}/$d %{_datadir}/%{name}/$d
	fi
done
exit 0

%post
%{_sbindir}/%{name}-chrome+xpcom-generate
%update_browser_plugins

%postun
if [ "$1" = 0 ]; then
	%update_browser_plugins
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
%if %{without xulrunner}
%attr(755,root,root) %{_libdir}/%{name}/*.so
%endif
%{_libdir}/%{name}/blocklist.xml

%if %{with crashreporter}
%{_libdir}/%{name}/crashreporter
%{_libdir}/%{name}/crashreporter-override.ini
%{_libdir}/%{name}/crashreporter.ini
%{_libdir}/%{name}/Throbber-small.gif
%endif

# config?
%{_libdir}/%{name}/.autoreg
%{_libdir}/%{name}/application.ini

%dir %{_libdir}/%{name}/components

%{_libdir}/%{name}/components/FeedConverter.js
%{_libdir}/%{name}/components/FeedWriter.js
%{_libdir}/%{name}/components/WebContentConverter.js
%{_libdir}/%{name}/components/browser.xpt
%{_libdir}/%{name}/components/fuelApplication.js
%{_libdir}/%{name}/components/nsBrowserContentHandler.js
%{_libdir}/%{name}/components/nsBrowserGlue.js
%{_libdir}/%{name}/components/nsMicrosummaryService.js
%{_libdir}/%{name}/components/nsPlacesTransactionsService.js
%{_libdir}/%{name}/components/nsPrivateBrowsingService.js
%{_libdir}/%{name}/components/nsSafebrowsingApplication.js
%{_libdir}/%{name}/components/nsSessionStartup.js
%{_libdir}/%{name}/components/nsSessionStore.js
%{_libdir}/%{name}/components/nsSetDefaultBrowser.js
%{_libdir}/%{name}/components/nsSidebar.js
%if %{without xulrunner}
%{_libdir}/%{name}/platform.ini
%{_libdir}/%{name}/components/FeedProcessor.js
%{_libdir}/%{name}/components/GPSDGeolocationProvider.js
%{_libdir}/%{name}/components/NetworkGeolocationProvider.js
%{_libdir}/%{name}/components/jsconsole-clhandler.js
%{_libdir}/%{name}/components/nsAddonRepository.js
%{_libdir}/%{name}/components/nsBadCertHandler.js
%{_libdir}/%{name}/components/nsBlocklistService.js
%{_libdir}/%{name}/components/nsContentDispatchChooser.js
%{_libdir}/%{name}/components/nsContentPrefService.js
%{_libdir}/%{name}/components/nsDefaultCLH.js
%{_libdir}/%{name}/components/nsDownloadManagerUI.js
%{_libdir}/%{name}/components/nsExtensionManager.js
%{_libdir}/%{name}/components/nsFilePicker.js
%{_libdir}/%{name}/components/nsFormAutoComplete.js
%{_libdir}/%{name}/components/nsHandlerService.js
%{_libdir}/%{name}/components/nsHelperAppDlg.js
%{_libdir}/%{name}/components/nsINIProcessor.js
%{_libdir}/%{name}/components/nsLivemarkService.js
%{_libdir}/%{name}/components/nsLoginInfo.js
%{_libdir}/%{name}/components/nsLoginManager.js
%{_libdir}/%{name}/components/nsLoginManagerPrompter.js
%{_libdir}/%{name}/components/nsPlacesAutoComplete.js
%{_libdir}/%{name}/components/nsPlacesDBFlush.js
%{_libdir}/%{name}/components/nsProxyAutoConfig.js
%{_libdir}/%{name}/components/nsSearchService.js
%{_libdir}/%{name}/components/nsSearchSuggestions.js
%{_libdir}/%{name}/components/nsTaggingService.js
%{_libdir}/%{name}/components/nsTryToClose.js
%{_libdir}/%{name}/components/nsURLFormatter.js
%{_libdir}/%{name}/components/nsUpdateTimerManager.js
%{_libdir}/%{name}/components/nsUrlClassifierLib.js
%{_libdir}/%{name}/components/nsUrlClassifierListManager.js
%{_libdir}/%{name}/components/nsWebHandlerApp.js
%{_libdir}/%{name}/components/pluginGlue.js
%{_libdir}/%{name}/components/storage-Legacy.js
%{_libdir}/%{name}/components/storage-mozStorage.js
%{_libdir}/%{name}/components/txEXSLTRegExFunctions.js
%endif

%attr(755,root,root) %{_libdir}/%{name}/components/libbrowsercomps.so
%attr(755,root,root) %{_libdir}/%{name}/components/libbrowserdirprovider.so
%if %{without xulrunner}
%attr(755,root,root) %{_libdir}/%{name}/components/libdbusservice.so
%attr(755,root,root) %{_libdir}/%{name}/components/libimgicon.so
%endif

%if %{with gnomevfs}
%if %{without xulrunner}
%attr(755,root,root) %{_libdir}/%{name}/components/libmozgnome.so
%endif
#%%attr(755,root,root) %{_libdir}/%{name}/components/libnkgnomevfs.so
%endif

%attr(755,root,root) %{_libdir}/%{name}/iceweasel
%dir %{_libdir}/%{name}/plugins
%if %{without xulrunner}
%attr(755,root,root) %{_libdir}/%{name}/run-mozilla.sh
%attr(755,root,root) %{_libdir}/%{name}/iceweasel-bin
%attr(755,root,root) %{_libdir}/%{name}/plugins/*.so
%attr(755,root,root) %{_libdir}/%{name}/mozilla-xremote-client
%attr(755,root,root) %{_libdir}/%{name}/plugin-container
%endif

%{_pixmapsdir}/iceweasel.png
%{_desktopdir}/iceweasel.desktop

# symlinks
%{_libdir}/%{name}/chrome
%{_libdir}/%{name}/defaults
%{_libdir}/%{name}/extensions
%{_libdir}/%{name}/icons
%{_libdir}/%{name}/modules
%{_libdir}/%{name}/searchplugins
%{_libdir}/%{name}/browserconfig.properties
%if %{without xulrunner}
%{_libdir}/%{name}/dictionaries
%{_libdir}/%{name}/greprefs
%{_libdir}/%{name}/res
%endif

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/chrome
%{_datadir}/%{name}/defaults
%{_datadir}/%{name}/icons
%{_datadir}/%{name}/modules
%{_datadir}/%{name}/searchplugins
%{_datadir}/%{name}/browserconfig.properties
%if %{without xulrunner}
%{_datadir}/%{name}/greprefs
%{_datadir}/%{name}/res
%endif

%dir %{_datadir}/%{name}/extensions
# -dom-inspector subpackage?
#%{_datadir}/%{name}/extensions/inspector@mozilla.org
# the signature of the default theme
%{_datadir}/%{name}/extensions/{972ce4c6-7e08-4474-a285-3208198ce6fd}

# files created by regxpcom and iceweasel -register
%ghost %{_libdir}/%{name}/components/compreg.dat
%ghost %{_libdir}/%{name}/components/xpti.dat
