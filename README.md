# Steam Library Image Replacer

A Python script for randomly picking a screenshot or image to use as the Steam Library Hero (Steam Banner) for VRChat or any other game. Based on https://github.com/synlogic/EAC-Image-Swapper, this script is specifically modified for Steam Library grid images. 

This tool allows you to replace the default Steam library image (438100_hero.jpg) for your games with a custom image of your choice. The project automatically replaces images from a folder you specify. The 438100_hero.jpg file is fully accessible, and this tool only automates the process. This does **not** modify any game client files or Steam itself.

## Download the Latest Release

Download the latest Steam Library Image Replacer zip from the [SteamLibrary-Image-Swapper GitHub Releases Page](https://github.com/BenjiThatFoxGuy/VRC_SteamLibrary-Image-Swapper/releases).

---

## How To Use

1. Download the latest [release](https://github.com/BenjiThatFoxGuy/VRC_SteamLibrary-Image-Swapper/releases).
2. Open Steam, go to your library, right-click on the game, and select `Manage` -> `Browse Local Files`.
3. Unzip the `SteamImageSwapper.zip` and place the `ImageSwapper` folder into the game's root folder.
4. Run `SteamImageSwapper.exe` to generate the `config_steam.ini` and `run.bat` files if they don't already exist.
5. Open `config_steam.ini` in a text editor and configure the photo directory. Specify the path(s) where your images are stored.
    - You can directly reference a folder or a specific image. 
    - The path format for the `photos` field can be like this: `photos = C:\Users\user\Pictures\VRChat` or `photos = C:\Users\user\Pictures\VRChat+C:\Users\user\Memes` .
    - You can also exclude specific subfolders using the `exclusions` field.
    - Example: `exclusions = C:\Users\user\Pictures\VRChat\UnwantedImages`
6. **Important**: You need to modify `config_steam.ini` to point to where Steam stores your grid images. Usually, this is located in:
    ```
    C:\Program Files (x86)\Steam\userdata\<your_steam_id>\config\grid
    ```
    Update the path to the `grid` directory where Steam saves its custom grid images (including `438100_hero.jpg`).
7. (Optional but recommended): Run `SteamImageSwapper.exe` manually once by double-clicking it. This step ensures the image is updated right away, as the image will only change on the next game run if you wait for Steam to launch.
8. In Steam, right-click the game or click the cog icon, go to `Properties`, and in the `Launch Options` box, insert:
    ```
    ImageSwapper\run.bat %COMMAND%
    ```
    **BEFORE** any other launch options. Be sure to use a **backslash** (`\`) and not a forward slash (`/`), or the system may not be able to find the file.
    Example:
    ```
    ImageSwapper\run.bat %COMMAND% --this-is-an-option=True
    ```
9. Run the game and enjoy seeing your custom images in the Steam Library Banner!

---

## Using with EAC Image Swapper

If you are also using the **EAC Image Swapper** alongside the Steam Library Image Replacer, follow these additional steps to ensure both tools work together seamlessly:

1. In the `run.bat` file that was generated, you will see the following line:
    ```batch
    cmd /c start ImageSwapper.exe
    ```
2. **To use both tools together**, simply add the following line after the first one:
    ```batch
    cmd /c start SteamImageSwapper.exe
    ```
   This ensures that **both** the EAC Image Swapper and the Steam Library Image Replacer run when launching the game.

3. Now, when you run the game, **both** the EAC Image Swapper and Steam Library Image Replacer will work in tandem to update the hero image for your game.

---

# Video Tutorial

<video src="https://github.com/user-attachments/assets/9ee4a18a-dc67-4c0f-a299-4c28ee895990"></video>

## This is the tutorial made by the author of the original project mind you.
---

# For Use with Other Applications

If you're using the Steam Library Image Replacer with games other than VRChat, you will need to make a couple of adjustments:

1. **Change the `steamgridfile` option**: 
   By default, the `steamgridfile` is set to `438100_hero.jpg`, which corresponds to VRChat's Steam ID. To use a custom game, you will need to replace `438100` with the correct **Steam App ID** for that game.

2. To find the correct Steam App ID for your game, visit [SteamDB](https://steamdb.info/) and search for the game you're interested in. You'll find the App ID listed there. For example:
   - VRChat's Steam App ID is `438100`, hence the default filename is `438100_hero.jpg`.
   - For Apex Legends, the App ID is `1172470`, so you would replace the filename with `1172470_hero.jpg`.

3. **Update the `steamgridfile` setting** in your `config_steam.ini` file:
   - If you're using Apex Legends, your `steamgridfile` should look like:
     ```
     steamgridfile = 1172470_hero.jpg
     ```
   - If you're using a different game, replace the `1172470` with the correct Steam App ID for that game.

4. Once the `steamgridfile` is updated with the correct App ID, the script will use the custom image file corresponding to the specified App ID when generating the banner for your game.

---

# Common Issues

If you run into any of the issues below, please try the following fixes:

1. **Error on game launch: "Windows cannot find 'ImageSwapper/run.bat'"**
    - Ensure that the `ImageSwapper` folder is placed **within** the game's root directory.
    - Double-check that you are using a **backslash** (`\`) and not a **forward slash** (`/`) in the launch options.

2. **Error on game launch: "Windows cannot find --launch-option-example"**
    - Ensure all launch options are **AFTER** `ImageSwapper\run.bat %COMMAND%`, not before. Ensure there is a space between them.