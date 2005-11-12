#!/bin/sh
# based on script by (c) vip at linux.pl, wolf at pld-linux.org

if [ `arch` == "x86_64" ]; then
	LIBDIR="/usr/lib64/mozilla-firefox"
else
	LIBDIR="/usr/lib/mozilla-firefox"
fi

MOZILLA_FIVE_HOME=$LIBDIR

MOZLOCALE="$(/usr/bin/locale | grep "^LC_MESSAGES=" | \
		sed -e "s|LC_MESSAGES=||g" -e "s|\"||g" )"
for MOZLANG in $(echo $LANGUAGE | tr ":" " ") $MOZLOCALE; do
	eval MOZLANG="$(echo $MOZLANG | sed -e "s|_\([^.]*\).*|-\1|g")"

	if [ -f $MOZILLA_FIVE_HOME/chrome/$MOZLANG.jar ]; then
		MOZARGS="-UILocale $MOZLANG"
		break
	fi
done

if [ -z "$MOZARGS" ]; then
	# try harder
	for MOZLANG in $(echo $LANGUAGE | tr ":" " ") $MOZLOCALE; do
		eval MOZLANG="$(echo $MOZLANG | sed -e "s|_.*||g")"

		LANGFILE=$(echo ${MOZILLA_FIVE_HOME}/chrome/${MOZLANG}*.jar \
				| sed 's/\s.*//g' )
		if [ -f "$LANGFILE" ]; then
			MOZLANG=$(basename "$LANGFILE" | sed 's/\.jar//')
			MOZARGS="-UILocale $MOZLANG"
			break
		fi
	done
fi

if [ -n "$MOZARGS" ]; then
	FIREFOX="$LIBDIR/firefox $MOZARGS"
else
	FIREFOX="$LIBDIR/firefox"
fi

if [ "$1" == "-remote" ]; then
	$FIREFOX "$@"
else
	PING=`$FIREFOX -remote 'ping()' 2>&1 >/dev/null`
	if [ -n "$PING" ]; then
		if [ -f "`pwd`/$1" ]; then
			$FIREFOX "file://`pwd`/$1"
		else
			$FIREFOX "$@"
		fi
	else
		if [ -z "$1" ]; then
			$FIREFOX -remote 'xfeDoCommand (openBrowser)'
		elif [ "$1" == "-mail" ]; then
			$FIREFOX -remote 'xfeDoCommand (openInbox)'
		elif [ "$1" == "-compose" ]; then
			$FIREFOX -remote 'xfeDoCommand (composeMessage)'
		else
			if [ -f "`pwd`/$1" ]; then
				URL="file://`pwd`/$1"
			else
				URL="$1"
			fi
			grep browser.tabs.opentabfor.middleclick ~/.mozilla/firefox/*/prefs.js | grep true > /dev/null
			if [ 0 -eq 0 ]; then
				$FIREFOX -remote "OpenUrl($URL,new-tab)"
			else
				$FIREFOX -remote "OpenUrl($URL,new-window)"
			fi
		fi
	fi
fi
