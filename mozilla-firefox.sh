#!/bin/sh
# based on script by (c) vip at linux.pl, wolf at pld-linux.org

MOZILLA_FIVE_HOME=/usr/lib/mozilla-firefox
if [ "$1" == "-remote" ]; then
	/usr/lib/mozilla-firefox/firefox "$@"
else
	PING=`/usr/lib/mozilla-firefox/firefox -remote 'ping()' 2>&1 >/dev/null`
	if [ -n "$PING" ]; then
		if [ -f "`pwd`/$1" ]; then
			/usr/lib/mozilla-firefox/firefox "file://`pwd`/$1"
		else
			/usr/lib/mozilla-firefox/firefox "$@"
		fi
	else
		if [ -z "$1" ]; then
			/usr/lib/mozilla-firefox/firefox -remote 'xfeDoCommand (openBrowser)'
		elif [ "$1" == "-mail" ]; then
			/usr/lib/mozilla-firefox/firefox -remote 'xfeDoCommand (openInbox)'
		elif [ "$1" == "-compose" ]; then
			/usr/lib/mozilla-firefox/firefox -remote 'xfeDoCommand (composeMessage)'
		else
			if [ -f "`pwd`/$1" ]; then
				URL="file://`pwd`/$1"
			else
				URL="$1"
			fi
			grep browser.tabs.opentabfor.middleclick ~/.mozilla/firefox/*/prefs.js | grep true > /dev/null
			if [ 0 -eq 0 ]; then
				/usr/lib/mozilla-firefox/firefox -remote "OpenUrl($URL,new-tab)"
			else
				/usr/lib/mozilla-firefox/firefox -remote "OpenUrl($URL,new-window)"
			fi
		fi
	fi
fi
