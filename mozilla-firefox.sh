#!/bin/sh
# based on script by (c) vip at linux.pl, wolf at pld-linux.org

if [ `arch` == "x86_64" ]; then
	LIBDIR="/usr/lib64/mozilla-firefox"
else
	LIBDIR="/usr/lib/mozilla-firefox"
fi

MOZILLA_FIVE_HOME=$LIBDIR
if [ "$1" == "-remote" ]; then
	$LIBDIR/firefox "$@"
else
	PING=`$LIBDIR/firefox -remote 'ping()' 2>&1 >/dev/null`
	if [ -n "$PING" ]; then
		if [ -f "`pwd`/$1" ]; then
			$LIBDIR/firefox "file://`pwd`/$1"
		else
			$LIBDIR/firefox "$@"
		fi
	else
		if [ -z "$1" ]; then
			$LIBDIR/firefox -remote 'xfeDoCommand (openBrowser)'
		elif [ "$1" == "-mail" ]; then
			$LIBDIR/firefox -remote 'xfeDoCommand (openInbox)'
		elif [ "$1" == "-compose" ]; then
			$LIBDIR/firefox -remote 'xfeDoCommand (composeMessage)'
		else
			if [ -f "`pwd`/$1" ]; then
				URL="file://`pwd`/$1"
			else
				URL="$1"
			fi
			grep browser.tabs.opentabfor.middleclick ~/.mozilla/firefox/*/prefs.js | grep true > /dev/null
			if [ 0 -eq 0 ]; then
				$LIBDIR/firefox -remote "OpenUrl($URL,new-tab)"
			else
				$LIBDIR/firefox -remote "OpenUrl($URL,new-window)"
			fi
		fi
	fi
fi
