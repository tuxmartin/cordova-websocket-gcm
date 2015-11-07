Instalace Cordovy
=================

```npm install -g cordova```


Vytvoreni aplikace pomoci Cordovy
=================================

Je potreba mit nainstalovane Android SDK a nastavene cesty.

```
cordova create gcm com.example.gcm GCM
cd gcm
```

Tim vznikne:

```
$ tree
.
├── config.xml
├── hooks
│   └── README.md
├── platforms
├── plugins
└── www
    ├── css
    │   └── index.css
    ├── img
    │   └── logo.png
    ├── index.html
    └── js
        └── index.js

7 directories, 6 files
```

Pridame Android:

```
cordova platform add android
cordova platforms ls
```

Obsah app je v adresari **www**.

Sestaveni a test
----------------

```
cordova build
cordova emulate android
cordova run android

```

emulate=emulator, run=mobil pres usb.

GCM plugin (Google Cloud Messaging)
-----------------------------------

Pravdepodobne je to tento: https://github.com/phonegap/phonegap-plugin-push

Instalace:

```
cordova plugin add phonegap-plugin-push
cordova plugin ls
```


Cordova app - jak na to
=======================

Po vygenerovani kostry app jsem jenom upravil tuto kostru. Dulezity je pouze obsah adresare **www**.

Pridal jsem *jQuery* a *materialise.js* JS knihovny, ale slo by to i bez nich.

Je potreba upravit *www/js/index.js*. Hlavne tam dat ID z webu GCM.

APK pro android bude v *gcm/platforms/android/build/outputs/apk/android-debug.apk*


Poznamky
=======

Ziskani GCM ID/KEY: https://developers.google.com/cloud-messaging/

Pokud je na mobilu apliakce otevrena, prichozi notifikace se pripise na konec a to je vse. Pokud je aplikace na pozadi (nema otevrene okno), mobil zahlasi notifikaci a prida ji do notifiakcniho menu (nevim jak se to jmenuje - proste jak se stahne horni lista dolu...).



