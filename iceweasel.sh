#!/bin/sh
# based on script by (c) vip at linux.pl, wolf at pld-linux.org

LIBDIR="@LIBDIR@/iceweasel"

# copy profile from Firefox if its available and if no Iceweasel
# profile exists
if [ ! -d $HOME/.iceweasel ]; then
	if [ -d $HOME/.mozilla/firefox ]; then
		echo "Copying profile from Firefox"
		cp -rf $HOME/.mozilla/firefox $HOME/.iceweasel
	fi
fi

# compreg.dat and/or chrome.rdf will screw things up if it's from an
# older version.  http://bugs.gentoo.org/show_bug.cgi?id=63999
for f in ~/.iceweasel/*/{compreg.dat,chrome.rdf,XUL.mfasl}; do
	if [[ -f ${f} && ${f} -ot /usr/bin/iceweasel ]]; then
		echo "Removing ${f} leftover from older iceweasel"
		rm -f "${f}"
	fi
done

ICEWEASEL="$LIBDIR/iceweasel"
PWD=${PWD:-$(pwd)}

if [ "$1" == "-remote" ]; then
	exec $ICEWEASEL "$@"
else
	PING=$($ICEWEASEL -remote 'ping()' 2>&1 >/dev/null)
	if [ -n "$PING" ]; then
		if [ -f "$PWD/$1" ]; then
			exec $ICEWEASEL "file://$PWD/$1"
		else
			exec $ICEWEASEL "$@"
		fi
	else
		if [ -z "$1" ]; then
			exec $ICEWEASEL -remote 'xfeDoCommand(openBrowser)'
		elif [ "$1" == "-mail" ]; then
			exec $ICEWEASEL -remote 'xfeDoCommand(openInbox)'
		elif [ "$1" == "-compose" ]; then
			exec $ICEWEASEL -remote 'xfeDoCommand(composeMessage)'
		else
			if [ -f "$PWD/$1" ]; then
				URL="file://$PWD/$1"
			else
				URL="$1"
			fi
			if grep -q browser.tabs.opentabfor.middleclick.*false ~/.iceweasel/*/prefs.js; then
				exec $ICEWEASEL -new-tab "$URL"
			else
				exec $ICEWEASEL -new-window "$URL"
			fi
		fi
	fi
fi
