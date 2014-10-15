pref("general.useragent.vendor", "PLD");
pref("general.useragent.vendorSub", "3.0");
pref("general.useragent.vendorComment", "Th");

pref("general.useragent.compatMode.firefox", true);
pref("distribution.searchplugins.defaultLocale", "en-US");
// Forbid application updates
lockPref("app.update.enabled", false);
// POODLE protection, CVE-2014-3566
pref("security.tls.version.min", 1);
