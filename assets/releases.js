/* The one place to change versions and download links.
   Files live in the Cloudflare R2 bucket in the layout scripts/collect_release.ps1 produces:
     /installer/Genesis-Setup-<ver>.exe
     /android/Genesis-Android-<ver>.apk
     /extension/Genesis-Browser-Bridge-<ver>.zip
   Versioning: all three share the Genesis release number (a "release train").
   A companion-only fix adds a fourth number (1.4.0.1, 1.4.0.2 ...) and still pairs
   with Genesis 1.4.0; when Genesis moves, everything moves with it. */
(function () {
  "use strict";
  var bucket = "https://pub-d9b3fb0b9c9f4e1a9eb645d1b333650a.r2.dev";
  var train = "1.4.0";

  window.GENESIS_RELEASES = {
    train: train,
    windows: {
      label: "Genesis AI for Windows",
      version: train,
      url: bucket + "/installer/Genesis-Setup-" + train + ".exe",
      platform: "Windows 10/11 · 64-bit"
    },
    android: {
      label: "Android companion",
      version: train,
      url: bucket + "/android/Genesis-Android-" + train + ".apk",
      platform: "Android 10+ · pairs with Genesis AI " + train
    },
    extension: {
      label: "Browser Bridge",
      version: train,
      url: bucket + "/extension/Genesis-Browser-Bridge-" + train + ".zip",
      platform: "Chrome · Edge · Brave · Opera · Vivaldi"
    }
  };
}());
