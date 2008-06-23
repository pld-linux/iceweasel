#!/bin/sh
# based on script by (c) vip at linux.pl, wolf at pld-linux.org

LIBDIR="@LIBDIR@/iceweasel"

MOZARGS=
MOZLOCALE="$(/usr/bin/locale | grep "^LC_MESSAGES=" | \
		sed -e "s|LC_MESSAGES=||g" -e "s|\"||g" )"
for MOZLANG in $(echo $LANGUAGE | tr ":" " ") $MOZLOCALE; do
	eval MOZLANG="$(echo $MOZLANG | sed -e "s|_\([^.]*\).*|-\1|g")"

	if [ -f $LIBDIR/chrome/$MOZLANG.jar ]; then
		MOZARGS="-UILocale $MOZLANG"
		break
	fi
done

if [ -z "$MOZARGS" ]; then
	# try harder
	for MOZLANG in $(echo $LANGUAGE | tr ":" " ") $MOZLOCALE; do
		eval MOZLANG="$(echo $MOZLANG | sed -e "s|_.*||g")"

		LANGFILE=$(echo $LIBDIR/chrome/${MOZLANG}*.jar \
				| sed 's/\s.*//g' )
		if [ -f "$LANGFILE" ]; then
			MOZLANG=$(basename "$LANGFILE" | sed 's/\.jar//')
			MOZARGS="-UILocale $MOZLANG"
			break
		fi
	done
fi

# compreg.dat and/or chrome.rdf will screw things up if it's from an
# older version.  http://bugs.gentoo.org/show_bug.cgi?id=63999
for f in ~/{.,.mozilla/}iceweasel/*/{compreg.dat,chrome.rdf,XUL.mfasl}; do
	if [[ -f ${f} && ${f} -ot /usr/bin/iceweasel ]]; then
		echo "Removing ${f} leftover from older iceweasel"
		rm -f "${f}"
	fi
done

if [ -n "$MOZARGS" ]; then
	ICEWEASEL="$LIBDIR/iceweasel $MOZARGS"
else
	ICEWEASEL="$LIBDIR/iceweasel"
fi

if [ "$1" == "-remote" ]; then
	exec $ICEWEASEL "$@"
else
	PING=`$ICEWEASEL -remote 'ping()' 2>&1 >/dev/null`
	if [ -n "$PING" ]; then
		if [ -f "`pwd`/$1" ]; then
			exec $ICEWEASEL "file://`pwd`/$1"
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
			if [ -f "`pwd`/$1" ]; then
				URL="file://`pwd`/$1"
			else
				URL="$1"
			fi
			grep browser.tabs.opentabfor.middleclick ~/.mozilla/iceweasel/*/prefs.js | grep false > /dev/null
			if [ $? -ne 0 ]; then
				exec $ICEWEASEL -new-tab "$URL"
			else
				exec $ICEWEASEL -new-window "$URL"
			fi
		fi
	fi
fi
