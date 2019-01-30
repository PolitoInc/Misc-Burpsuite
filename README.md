# Misc-Burpsuite

Various BurpSuite extensions.

politoinc_audiocues.py	
  - audio cues alerts you when burp identifies input parameters.  Could probably be extended to alert on other more interesting events.  Audiocues only works in linux and mac

politoinc_requestanalytics.py
 - Request Analytics tracks the count of files in the site map.  

extension.jar
 - Java audio cues extension. Compatible with Windows, MAC and Linux.

burp/
 - Contains java source code for the extension

assets/
 - Contains sound files used for the extension

build.sh
 - Used to build the extension as long as java JDK is in PATH
