#! /bin/sh

rm -fv ./modules/oji/tests/script/killer.exe
rm -fv ./other-licenses/7zstub/firefox/7zSD.sfx
rm -fv ./toolkit/mozapps/update/src/updater/macbuild/Contents/Resources/English.lproj/MainMenu.nib/keyedobjects.nib
rm -fv ./toolkit/mozapps/update/src/updater/macbuild/Contents/PkgInfo
rm -fv ./extensions/universalchardet/doc/UniversalCharsetDetection.doc
rm -fv ./config/bin2rc.exe
rm -fv ./config/makedep.exe
rm -fv ./config/mangle.exe
rm -fv ./embedding/browser/activex/src/pluginhostctrl/cab/redist/ATL.DLL
rm -fv ./embedding/browser/activex/tests/vbrowse/browser.frx
rm -fv ./embedding/browser/activex/tests/vbrowse/frmToolBar.frx
rm -fv ./embedding/qa/testembed/testembed.aps
rm -fv ./embedding/tests/MSDotNETCSEmbed/MSDotNETCSEmbed.suo
rm -fv ./embedding/wrappers/DotNETEmbed/DotNETEmbed.snk
rm -fv ./intl/unicharutil/tools/data/case.dat
rm -fv ./intl/unicharutil/tools/data/cmbcl.dat
rm -fv ./intl/unicharutil/tools/data/ctype.dat
rm -fv ./intl/unicharutil/tools/data/decomp.dat
rm -fv ./intl/unicharutil/tools/data/num.dat
rm -fv ./js/src/js.mdp
rm -fv ./js/src/liveconnect/jsj_nodl.c
rm -fv ./memory/jemalloc/ed.exe
rm -fv ./plugin/oji/JEP/MRJPlugin.plugin/Contents/MacOS/MRJPlugin
rm -fv ./plugin/oji/JEP/MRJPlugin.plugin/Contents/MacOS/MRJPlugin.jar
rm -fv ./plugin/oji/JEP/MRJPlugin.plugin/Contents/Resources/MRJPlugin.rsrc
rm -fv ./plugin/oji/JEP/JavaEmbeddingPlugin.bundle/Contents/MacOS/JavaEmbeddingPlugin
rm -fv ./plugin/oji/JEP/JavaEmbeddingPlugin.bundle/Contents/Resources/Java/JavaEmbeddingPlugin.jar
rm -fv ./plugin/oji/MRJ/plugin/Resources/Dialogs.rsrc
rm -fv ./plugin/oji/MRJ/plugin/Resources/Strings.rsrc
rm -fv ./plugin/oji/MRJ/plugin/Resources/Version.rsrc
rm -fv ./plugin/oji/MRJ/plugin/MRJPlugin.jar
rm -fv ./plugin/oji/MRJ/plugin/netscape.plugin.jar
rm -fv ./plugin/oji/MRJ/plugin/Source/JMURLConnection
rm -fv ./plugin/oji/MRJ/testing/ConsoleApplet/ConsoleApplet.mcp
rm -fv ./plugin/oji/MRJ/testing/JSApplet/JSApplet.mcp
rm -fv ./plugin/oji/MRJ/testing/SwingApplet/TestApplet.mcp
rm -fv ./plugin/oji/MRJ/testing/TrivialApplet/MyApplet.mcp
rm -fv ./plugin/oji/MRJCarbon/MRJSDK/JavaFrameworks/JavaEmbeddingLib
rm -fv ./plugin/oji/MRJCarbon/plugin/MRJPlugin.jar
rm -fv ./plugin/oji/MRJCarbon/plugin/Resources/Dialogs.rsrc
rm -fv ./plugin/oji/MRJCarbon/plugin/Resources/Strings.rsrc
rm -fv ./plugin/oji/MRJCarbon/plugin/Resources/Version.rsrc
rm -fv ./xpcom/reflect/xptcall/tests/eVC4/XPTCInvoke_Testing.cpp
rm -fv ./xpcom/tests/StringFactoringTests/StringTest.mcp
rm -fv ./xpinstall/test/pre_checkin.xpi
rm -fv ./layout/doc/SpaceMgr_BlockReflSt_OD.sda
rm -fv ./layout/doc/object_diagram_template.sda
rm -fv ./layout/html/tests/block/bugs/RealSnow.jar
rm -fv ./xpfe/bootstrap/appleevents/nsAppleEvents.rsrc
rm -fv ./toolkit/crashreporter/tools/win32/dump_syms.exe
rm -fv ./toolkit/crashreporter/google-breakpad/src/tools/solaris/dump_syms/testdata/dump_syms_regtest.o
rm -fv ./toolkit/mozapps/installer/windows/nsis/AppAssocReg.dll
rm -fv ./toolkit/mozapps/installer/windows/nsis/ShellLink.dll
rm -fv ./toolkit/mozapps/installer/windows/nsis/UAC.dll
rm -fv ./toolkit/mozapps/installer/windows/nsis/nsProcess.dll
rm -fvr ./other-licenses/7zstub
rm -fvr ./other-licenses/branding
rm -fv ./netwerk/protocol/ftp/doc/rfc959.txt
find . -type d -name CVS | xargs rm -rf
find . -type f -name .cvsignore | xargs rm -f
