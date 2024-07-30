[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/W7W21OEBU)
# EAC Image Swapper
A python script for randomly picking a screenshot or image to use as the EAC splashscreen.

This isn't considered a mod, it doesn't modify the VRChat client in any way.  The EasyAntiCheat/SplashScreen.png it replaces is fully accessible without any external programs, this simply automates it.

## Download the latest ImageSwapper.zip from https://github.com/synlogic/EAC-Image-Swapper/releases

# How To Use
1) Download the latest [release](https://github.com/synlogic/EAC-Image-Swapper/releases).
2) Open steam, go to library and right click on VRChat.  Go to Manage->Browse Local Files
3) Unzip ImageSwapper.zip and place files into the local files folder
4) Open config.ini in a text editor and place the path of your photos directory.
-  The photo that gets picked can be a folder within the root folder, for example if you set it to C:\Pictures it might pull a picture from C:\Pictures\ThisIsASubFolder.  You can exclude subfolders using the "exclude" option in the same way.
   EX: photos = C:\Users\user\Pictures\VRChat
- You can append more directories by using + between them.  Example: C:\Users\user\Pictures\VRChat+C:\Users\user\Pictures\Skebs
6) (Optional) Go ahead and run ImageSwapper.exe once manually by double clicking.  The process technically runs after EAC is launched so the image will change on the *next* run.  Running the ImageSwapper.exe manually just insures that the first run is a new image.
7) In steam again right click VRChat and go to properties.  In the launch options box insert "run.bat %COMMAND%" **BEFORE** any launch options
8) Run VRChat and enjoy seeing your screenshots, skebs, or whatever else on your EAC splash screen!

# Video Tutorial
[eac tutorial.webm](https://user-images.githubusercontent.com/26206994/182078101-76e2988a-d060-4f3d-abc6-cabfeee51efc.webm)

This was made and tested with VRChat in mind. However, this should work on many other games using EAC as well.
