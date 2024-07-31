[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/W7W21OEBU)
# EAC Image Swapper
A python script for randomly picking a screenshot or image to use as the EAC Splash Screen.

This was made and tested with VRChat in mind. However, this should work on many other games using EAC as well. See "For Use with Other Application" sections for more information.

This is not mod, it does not modify the VRChat (or any other game) client in any way.  The SplashScreen.png it replaces is fully accessible without any external programs, this simply automates the process :)

## Download the latest ImageSwapper.zip from https://github.com/synlogic/EAC-Image-Swapper/releases

# How To Use
1) Download the latest [release](https://github.com/synlogic/EAC-Image-Swapper/releases).
2) Open steam, go to library and right click on the game.  Go to Manage->Browse Local Files
3) Unzip ImageSwapper.zip and place the ImageSwapper folder into the games root folder.
4) Run ImageSwapper.exe to generate the config.ini and run.bat files if they do not already exist.
5) Open config.ini in a text editor and place the path(s) of your photo directory.  You can also directly reference a single image instead of a directory.
-  The photo that gets picked can be a folder within the root folder, for example if you set it to C:\Pictures it might pull a picture from C:\Pictures\ThisIsASubFolder.  You can exclude subfolders using the "exclude" option in the same way as the photos option.
- Example:  photos = C:\Users\user\Pictures\VRChat OR photos = C:\Users\user\Pictures\VRChat+C:\Users\user\Memes+....etc for adding additional folders.
- Example:  exclusions = C:\Users\user\Pictures\VRChat\PicturesIDoNotWantToSee
- You can append more directories by using + between them.  Example: C:\Users\user\Pictures\VRChat+C:\Users\user\Pictures\Skebs
6) (Optional but recommended) Once configured, Go ahead and run ImageSwapper.exe once manually by double clicking.  This application technically runs after EAC is launched so the image will change on the *next* run. By running the ImageSwapper.exe manually this just insures that the first run is a new image.
7) In steam right click the game or click the cog icon and go to Properties.  In the launch options box insert "ImageSwapper\run.bat %COMMAND%" **BEFORE** any launch options
- It is important that you use a **backslash** (\) otherwise it may throw and error that the file cannot be found.
- Ensure all launch options are **AFTER** the %COMMAND% with a space in between.  Example: ImageSwapper\run.bat %COMMAND% --this-is-an-option=True
8) Run the game and enjoy seeing your screenshots, skebs, or whatever else on your EAC splash screen!

# Video Tutorial
[eac tutorial.webm](https://user-images.githubusercontent.com/26206994/182078101-76e2988a-d060-4f3d-abc6-cabfeee51efc.webm)

# For Use with Other Applications
Follow the same steps above for setup. However, there is one more configuration change to make:
- easyanticheat option allows for direct reference to a specific folder where the SplashImage.png is located. 
- Example: easyanticheat = C:\Games\Apex Legends\EasyAntiCheat\OddlySpecificFolderProbably

# Common issues
If you run into one the issues below please try the following fixes.

1) You get an error on game launch "Windows cannot find 'ImageSwapper/run.bat'"
- Ensure the ImageSwapper folder is placed within the game's root directory.
- Make sure you are using a **backslash** (\) and not a **forward slash** (/)
2) You get an error on game launch "Windows cannot find --launch-option-example"
- Ensure all launch options are **AFTER** ImageSwapper\run.bat %COMMAND% and not before.