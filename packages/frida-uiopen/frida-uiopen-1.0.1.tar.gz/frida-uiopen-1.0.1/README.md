# Frida UIOpen
A frida command-line tool that supports iOS devices that attempt to open resources at a specified URL.
## Examples
```shell
# Open a web page in the browser of your iOS device
frida-uiopen -U "https://www.baidu.com"

# Jump to the Bluetooth Preferences page on your iOS device
frida-uiopen -U "prefs:root=Bluetooth"

# On your iOS device, go to the App Store Details page
frida-uiopen -U "itms-apps://itunes.apple.com/app/id1142110895"
```