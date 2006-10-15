#!/bin/sh
# based on script by (c) vip at linux.pl, wolf at pld-linux.org
# using mozilla-launcher by glen at pld-linux.org
# copied from swiftfox.sh by czarny at pld-linux.org
#
# Stub script to run mozilla-launcher.  We used to use a symlink here
# but OOo brokenness makes it necessary to use a stub instead:
# http://bugs.gentoo.org/show_bug.cgi?id=78890

export MOZILLA_LAUNCHER=@APPNAME@
export MOZILLA_LIBDIR=@LIBDIR@/@APPNAME@

mozlocale=$(/usr/bin/locale | awk -F= '/^LC_MESSAGES=/{print $2}' | xargs)
mozlocale="$LANGUAGE ${mozlocale%.*}"
for MOZLANG in $mozlocale; do
	MOZLANG=$(echo $MOZLANG | sed -e 's|_\([^.]*\).*|-\1|')

	if [ -f $MOZILLA_LIBDIR/chrome/$MOZLANG.jar ]; then
		MOZARGS="-UILocale $MOZLANG"
		break
	fi
done

if [ -z "$MOZARGS" ]; then
	# try harder
	for MOZLANG in $mozlocale; do
		MOZLANG=$(echo $MOZLANG | sed -e 's|_.*||')

		LANGFILE=$(echo ${MOZILLA_LIBDIR}/chrome/${MOZLANG}*.jar | sed 's/\s.*//g')
		if [ -f "$LANGFILE" ]; then
			MOZLANG=$(basename "$LANGFILE" | sed 's/\.jar//')
			MOZARGS="-UILocale $MOZLANG"
			break
		fi
	done
fi

exec /usr/lib/mozilla-launcher $MOZARGS "$@"
