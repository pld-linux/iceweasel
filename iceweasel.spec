#
# TODO:
# - %files
# - make it install in /usr/lib/iceweasel and so on (not mozilla-firefox)
# - change patches to iceweasel (in sources)
# - make it use mozilla-launcher
# - check all other firefox todos:
#
# - with new gcc version (it is possible that)
#   - -fvisibility=hiddenn and ac_cv_visibility_pragma=no can be removed
# - with new firefox version (it is possible that)
#   - -fno-strict-aliasing can be removed (needs to be tested carefuly,
#      not to be fixed soon, imho)
# - handle locales differently (runtime, since it's possible to do)
# - see ftp://ftp.debian.org/debian/pool/main/m/mozilla-firefox/*diff*
#   for hints how to make locales and other stuff like extensions working
# - rpm upgrade is broken. First you need uninstall Firefox 1.0.x.
#
# Conditional build:
%bcond_with	tests	# enable tests (whatever they check)
%bcond_without	gnome	# disable all GNOME components (gnomevfs, gnome, gnomeui)
#
%define		_sourceversion		1.5.0
%define		_rel			g1
Summary:	Iceweasel web browser
Summary(pl):	Iceweasel - przegl±darka WWW
Name:		iceweasel
Version:	1.5.0.7
Release:	0.1
License:	MPL/LGPL
Group:		X11/Applications/Networking
Source0:	http://gnuzilla.gnu.org/download/%{name}-%{_sourceversion}-%{_rel}.tar.bz2
# Source0-md5:	c7dd4d099bd9acdea0d16c601f359017
Source1:	mozilla-firefox.desktop
Source2:	mozilla-firefox.sh
Patch0:		%{name}-nss.patch
Patch1:		mozilla-firefox-lib_path.patch
Patch2:		mozilla-firefox-nss-system-nspr.patch
Patch3:		mozilla-firefox-nopangoxft.patch
#Patch4: mozilla-firefox-name.patch
Patch5:		mozilla-firefox-fonts.patch
Patch6:		%{name}-build.patch
Patch7:		%{name}-stack.patch
# UPDATE or DROP?
#PatchX: %{name}-searchplugins.patch
URL:		http://www.gnu.org/software/gnuzilla/
%{?with_gnome:BuildRequires:	GConf2-devel >= 1.2.1}
BuildRequires:	automake
BuildRequires:	cairo-devel >= 1.0.0
%{?with_gnome:BuildRequires:	gnome-vfs2-devel >= 2.0}
BuildRequires:	gtk+2-devel >= 1:2.0.0
BuildRequires:	heimdal-devel >= 0.7.1
BuildRequires:	libIDL-devel >= 0.8.0
%{?with_gnome:BuildRequires:	libgnome-devel >= 2.0}
%{?with_gnome:BuildRequires:	libgnomeui-devel >= 2.2.0}
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	libpng-devel >= 1.2.7
BuildRequires:	libstdc++-devel
BuildRequires:	nspr-devel >= 1:4.6.1-2
BuildRequires:	nss-devel >= 1:3.11.3
BuildRequires:	pango-devel >= 1:1.6.0
BuildRequires:	perl-modules >= 5.004
BuildRequires:	pkgconfig
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXft-devel >= 2.1
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXp-devel
BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	zip
BuildRequires:	zlib-devel >= 1.2.3
Requires(post):	mktemp >= 1.5-18
Requires:	%{name}-lang-resources = %{version}
Requires:	nspr >= 1:4.6.1-2
Requires:	nss >= 1:3.11.3
Provides:	wwwbrowser
Obsoletes:	mozilla-firebird
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_firefoxdir	%{_libdir}/iceweasel
# mozilla and firefox provide their own versions
%define		_noautoreqdep		libgkgfx.so libgtkembedmoz.so libgtkxtbin.so libjsj.so libmozjs.so libxpcom.so libxpcom_compat.so

%define		specflags	-fno-strict-aliasing -funswitch-loops -funroll-loops

%description
IceWeasel is the GNU version of the Firefox browser. Its main advantage
is an ethical one: it is entirely free software. While the source code
from the Mozilla project is free software, the binaries that they release
include additional non-free software. Also, they distribute non-free
software as plug-ins. (IceWeasel does keep the triple licensing used by
Firefox to facilitate the reuse of code.)

IceWeasel also includes some privacy protection features:
Some sites refer to zero-size images on other hosts to keep track of
cookies. When IceWeasel detects this mechanism it blocks cookies from
the site hosting the zero-length image file. (It is possible to
re-enable such a site by removing it from the blocked hosts list.)

Other sites rewrite the host name in links redirecting the user to
another site, mainly to "spy" on clicks. When this behavior is detected,
IceWeasel shows a message alerting the user.

To see these new features in action, some test pages are available
(http://gnuzilla.gnu.org/test/).
Fredrik Hubbe's web site can be used test plugins
(http://fredrik.hubbe.net/plugger.html?free=1).

%description -l pl
Mozilla Firefox jest open sourcow± przegl±dark± sieci WWW, stworzon± z
my¶l± o zgodno¶ci ze standardami, wydajno¶ci± i przeno¶no¶ci±.

%package devel
Summary:	Headers for developing programs that will use Iceweasel
Summary(pl):	Iceweasel - pliki nag³ówkowe
Group:		X11/Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	nspr-devel >= 1:4.6.1-2
Obsoletes:	mozilla-devel

%description devel
Iceweasel development package.

%description devel -l pl
Pliki nag³ówkowe przegl±darki Iceweasel.

%package lang-en
Summary:	English resources for Iceweasel
Summary(pl):	Anglojêzyczne zasoby dla przegl±darki Iceweasel
Group:		X11/Applications/Networking
Requires(post,postun):	%{name} = %{version}-%{release}
Requires(post,postun):	textutils
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-lang-resources = %{version}-%{release}

%description lang-en
English resources for Iceweasel.

%description lang-en -l pl
Anglojêzyczne zasoby dla przegl±darki Iceweasel.

%prep
%setup -q -n %{name}-%{_sourceversion}-%{_rel}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
#%patch4 -p1
%patch5 -p1
%patch6 -p0
%patch7 -p1

sed -i 's/\(-lgss\)\(\W\)/\1disable\2/' configure

%build
rm -f .mozconfig
export CFLAGS="%{rpmcflags} `%{_bindir}/pkg-config mozilla-nspr --cflags-only-I`"
export CXXFLAGS="%{rpmcflags} `%{_bindir}/pkg-config mozilla-nspr --cflags-only-I`"

cp -f %{_datadir}/automake/config.* build/autoconf
cp -f %{_datadir}/automake/config.* nsprpub/build/autoconf
cp -f %{_datadir}/automake/config.* directory/c-sdk/config/autoconf

LIBIDL_CONFIG="%{_bindir}/libIDL-config-2"; export LIBIDL_CONFIG

cat << 'EOF' > .mozconfig
# That is evili, as we don't build default mozilla
#. $topsrcdir/browser/config/mozconfig

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
ac_add_options --enable-optimize="%{rpmcflags}"
%if %{?debug:1}0
ac_add_options --enable-debug
ac_add_options --enable-debug-modules
%else
ac_add_options --disable-debug
ac_add_options --disable-debug-modules
%endif
%if %{with gnome}
ac_add_options --enable-gnomevfs
ac_add_options --enable-gnomeui
%else
ac_add_options --disable-gnomevfs
ac_add_options --disable-gnomeui
%endif
%if %{with tests}
ac_add_options --enable-tests
%else
ac_add_options --disable-tests
%endif
ac_add_options --disable-composer
ac_add_options --disable-dtd-debug
ac_add_options --disable-freetype2
ac_add_options --disable-installer
ac_add_options --disable-jsd
ac_add_options --disable-ldap
ac_add_options --disable-mailnews
ac_add_options --disable-profilesharing
ac_add_options --disable-strip
ac_add_options --disable-xprint
ac_add_options --enable-application=browser
ac_add_options --enable-canvas
ac_add_options --enable-cookies
ac_add_options --enable-crypto
ac_add_options --enable-default-toolkit=gtk2
ac_add_options --enable-extensions=all
ac_add_options --enable-image-encoder=all
ac_add_options --enable-image-decoder=all
ac_add_options --enable-mathml
ac_add_options --enable-pango
# This breaks mozilla start - don't know why
#ac_add_options --enable-places
ac_add_options --enable-postscript
ac_add_options --enable-reorder
ac_add_options --enable-safe-browsing
ac_add_options --enable-single-profile
ac_add_options --enable-storage
ac_add_options --enable-svg
ac_add_options --enable-system-cairo
ac_add_options --enable-url-classifier
ac_add_options --enable-view-source
ac_add_options --enable-xft
ac_add_options --enable-xinerama
ac_add_options --enable-xpctools
ac_add_options --with-distribution-id=org.pld-linux
ac_add_options --with-pthreads
ac_add_options --with-system-jpeg
ac_add_options --with-system-nspr
ac_add_options --with-system-nss
ac_add_options --with-system-png
ac_add_options --with-system-zlib
ac_cv_visibility_pragma=no
EOF

%configure2_13

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
install -d \
	$RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_libdir}{,extensions}} \
	$RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir}} \
	$RPM_BUILD_ROOT{%{_includedir}/%{name}/idl,%{_pkgconfigdir}}
# extensions dir is needed (it can be empty)

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
	MOZ_PKG_APPNAME="iceweasel"\
	MOZILLA_BIN="\$(DIST)/bin/iceweasel" \
	EXCLUDE_NSPR_LIBS=1

sed 's,@LIBDIR@,%{_libdir},' %{SOURCE2} > $RPM_BUILD_ROOT%{_bindir}/iceweasel

#install -m0644 bookmarks.html $RPM_BUILD_ROOT%{_firefoxdir}/defaults/profile/
#install -m0644 bookmarks.html $RPM_BUILD_ROOT%{_firefoxdir}/defaults/profile/US/

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}

rm -rf US classic comm embed-sample en-{US,mac,unix,win} modern pipnss pippki
rm -f en-win.jar en-mac.jar embed-sample.jar modern.jar

# header/developement files
cp -rfL dist/include/*	$RPM_BUILD_ROOT%{_includedir}/%{name}
cp -rfL dist/idl/*	$RPM_BUILD_ROOT%{_includedir}/%{name}/idl

install dist/bin/regxpcom $RPM_BUILD_ROOT%{_bindir}
install dist/bin/xpidl $RPM_BUILD_ROOT%{_bindir}
install dist/bin/xpt_dump $RPM_BUILD_ROOT%{_bindir}
install dist/bin/xpt_link $RPM_BUILD_ROOT%{_bindir}

#ln -sf %{_includedir}/mozilla-firefox/necko/nsIURI.h \
#	$RPM_BUILD_ROOT%{_includedir}/mozilla-firefox/nsIURI.h

# CA certificates
ln -s %{_libdir}/libnssckbi.so $RPM_BUILD_ROOT%{_firefoxdir}/libnssckbi.so

# pkgconfig files
for f in build/unix/*.pc ; do
        sed -e 's/firefox-%{version}/mozilla-firefox/' $f \
	    > $RPM_BUILD_ROOT%{_pkgconfigdir}/$(basename $f)
done

# already provided by standalone packages
rm -f $RPM_BUILD_ROOT%{_pkgconfigdir}/firefox-{nss,nspr}.pc

sed -i -e 's#firefox-nspr =.*#mozilla-nspr#g' -e 's#irefox-nss =.*#mozilla-nss#g' \
	$RPM_BUILD_ROOT%{_pkgconfigdir}/*.pc

# includedir/dom CFLAGS
sed -i -e '/Cflags:/{/{includedir}\/dom/!s,$, -I${includedir}/dom,}' \
	$RPM_BUILD_ROOT%{_pkgconfigdir}/firefox-plugin.pc

cat << 'EOF' > $RPM_BUILD_ROOT%{_sbindir}/firefox-chrome+xpcom-generate
#!/bin/sh
umask 022
rm -f %{_firefoxdir}/chrome/{chrome.rdf,overlayinfo/*/*/*.rdf}
rm -f %{_firefoxdir}/components/{compreg,xpti}.dat
MOZILLA_FIVE_HOME=%{_firefoxdir}
export MOZILLA_FIVE_HOME

# PATH
PATH=%{_firefoxdir}:$PATH
export PATH

# added %{_prefix}/lib : don't load your local library
LD_LIBRARY_PATH=%{_firefoxdir}${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
export LD_LIBRARY_PATH

unset TMPDIR TMP || :
export HOME=$(mktemp -d)
MOZILLA_FIVE_HOME=%{_firefoxdir} %{_firefoxdir}/regxpcom
MOZILLA_FIVE_HOME=%{_firefoxdir} %{_firefoxdir}/firefox -register
rm -rf $HOME
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/firefox-chrome+xpcom-generate

%postun
if [ "$1" = "0" ]; then
	rm -rf %{_firefoxdir}/chrome/overlayinfo
	rm -f  %{_firefoxdir}/chrome/*.rdf
	rm -rf %{_firefoxdir}/components
	rm -rf %{_firefoxdir}/extensions
fi

#%triggerpostun -- %{name} < 1.5
#%banner %{name} -e <<EOF
#NOTICE:
#If you have problem with upgrade from old mozilla-firefox 1.0.x,
#you should remove it first and reinstall %{name}-%{version}
#EOF

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%dir %{_firefoxdir}
%{_firefoxdir}/res
%dir %{_firefoxdir}/components
%attr(755,root,root) %{_firefoxdir}/components/*.so
%{_firefoxdir}/components/*.js
%{_firefoxdir}/components/*.xpt
%dir %{_firefoxdir}/plugins
%attr(755,root,root) %{_firefoxdir}/plugins/*.so
%{_firefoxdir}/searchplugins
%{_firefoxdir}/icons
%{_firefoxdir}/defaults
%{_firefoxdir}/greprefs
%dir %{_firefoxdir}/extensions
%dir %{_firefoxdir}/init.d
%attr(755,root,root) %{_firefoxdir}/*.so
%attr(755,root,root) %{_firefoxdir}/*.sh
%attr(755,root,root) %{_firefoxdir}/m*
%attr(755,root,root) %{_firefoxdir}/f*
%attr(755,root,root) %{_firefoxdir}/reg*
%attr(755,root,root) %{_firefoxdir}/x*
%{_pixmapsdir}/*
%{_desktopdir}/*

%dir %{_firefoxdir}/chrome
%{_firefoxdir}/chrome/*.jar
%{_firefoxdir}/chrome/*.manifest
# -chat subpackage?
#%{_firefoxdir}/chrome/chatzilla.jar
#%{_firefoxdir}/chrome/content-packs.jar
%dir %{_firefoxdir}/chrome/icons
%{_firefoxdir}/chrome/icons/default

# -dom-inspector subpackage?
%dir %{_firefoxdir}/extensions/inspector@mozilla.org
%{_firefoxdir}/extensions/inspector@mozilla.org/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/regxpcom
%attr(755,root,root) %{_bindir}/xpidl
%attr(755,root,root) %{_bindir}/xpt_dump
%attr(755,root,root) %{_bindir}/xpt_link
%{_includedir}/%{name}
%{_pkgconfigdir}/*

%files lang-en
%defattr(644,root,root,755)
%{_firefoxdir}/chrome/en-US.jar
%{_firefoxdir}/chrome/en-US.manifest
