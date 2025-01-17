from random import choice
from os import path, listdir, getcwd, pardir
from sys import exit, stdout
from glob import glob
from requests import get as rget
from configparser import ConfigParser
from traceback import print_exc, format_exc
from PIL import Image
from packaging import version

def print(value, force=False):
    config = ConfigParser()
    config.read('config_steam.ini')
    if config.get('OPTIONS', 'output_to_cmd').lower() == 'true' or force:
        stdout.write(f'{value}\\n')

def CheckForUpdates():
    current_version = "0.0.1"
    print(f"VRChat Steam Library Banner Swapper version: {current_version}", True)
    print("Checking for updates | You can disable this in config_steam.ini", True)
    
    try:
        response = rget("https://github.com/BenjiThatFoxGuy/VRC_SteamLibrary-Image-Swapper/releases/latest")
        latest = response.url.split('/')[-1].replace('v', '')
        if version.parse(current_version) < version.parse(latest):
            print("\\nUpdate Available! Download from \\nhttps://github.com/BenjiThatFoxGuy/VRC_SteamLibrary-Image-Swapper/releases/latest (Copy Paste into Browser)\\n", True)
            input("Press enter key to continue..")
    except Exception:
        print_exc()
        print('Checking for updates failed...', True)
        return

def Resize(path):
    image = Image.open(path)
    
    # Calculate the scaling factor to fill the entire 1920x620 size
    ratio = max(1920 / image.width, 620 / image.height)

    # New dimensions that will cover the 1920x620 area
    x = int(image.width * ratio)
    y = int(image.height * ratio)

    # Resize the image to the new dimensions
    image = image.resize((x, y))

    # Crop the image to 1920x620 by cutting off excess parts from the center
    left = (x - 1920) // 2
    top = (y - 620) // 2
    right = left + 1920
    bottom = top + 620

    cropped_image = image.crop((left, top, right, bottom))

    return cropped_image


def GenerateConfig():
    sections = ('PATH', 'OPTIONS')
    options = [
        ['PATH', 'photos', ''],
        ['PATH', 'exclusions', ''],
        ['PATH', 'steamgridpath', 'C:\\Program Files (x86)\\Steam\\userdata\\123456789\\config\\grid'],
        ['PATH', 'steamgridfile', '438100_hero.jpg'],
        ['OPTIONS', 'pause_on_complete', 'false'],
        ['OPTIONS', 'check_for_updates', 'true'],
        ['OPTIONS', 'output_to_cmd', 'false']
    ]
    config = ConfigParser()

    config_file_exists = run_bat_exists = True
    ## I have renamed a bunch of stuff to let it coexist with the EAC Image Swapper
    # Verify if the config file exists
    if not path.exists('config_steam.ini'):
        config_file_exists = False
        print("config_steam.ini not found, creating a new one...", True)
        for section in sections:
            if not config.has_section(section):
                print(f"Adding section: {section}")
                config.add_section(section)
        for option in options:
            if not config.has_option(option[0], option[1]):
                print(f"Adding option: {option[0]} -> {option[1]} = {option[2]}")
                config.set(option[0], option[1], option[2])
        with open('config_steam.ini', 'w') as configfile:
            config.write(configfile)
        print('config_steam.ini created. Open it to input your photo path\\n', True)

    # Print config sections for debugging
    print("Current sections in config_steam.ini:", config.sections())

    # Ensure all necessary sections and options are present
    if path.exists('config_steam.ini'):
        config.read('config_steam.ini')
        
        # Debugging: print the sections and options
        # print("Sections loaded from config_steam.ini", config.sections())
        
        for section in sections:
            if not config.has_section(section):
                print(f"Section {section} is missing. Adding it...")
                config.add_section(section)
        
        for option in options:
            if not config.has_option(option[0], option[1]):
                print(f"Option {option[1]} under section {option[0]} is missing. Adding it with default value...")
                config.set(option[0], option[1], option[2])

        with open('config_steam.ini', 'w') as configfile:
            config.write(configfile)

    # Verify 'OPTIONS' section exists before accessing
    if not config.has_section('OPTIONS'):
        print("ERROR: 'OPTIONS' section is missing in config_steam.ini!")
        input("Press enter key to exit...")
        exit()

    return config


def getLastUsedPhoto():
    photo_path = None
    if path.exists('last_used_library.txt'):
        with open('last_used_library.txt') as f:
            photo_path = f.read().strip()
    return photo_path

def saveLastUsedPhoto(photo_path):
    print("Saving last used photo")
    with open('last_used_library.txt', 'w') as f:
        f.write(photo_path)
    
def GetPhotosInDirectory(dir):
    print(f'Finding files in {dir}')
    last_used = getLastUsedPhoto()
    photos = []
    if not path.isdir(dir) and ((dir.lower().endswith('.png') or dir.lower().endswith('.jpg')) and not dir.lower().endswith('_vr.jpg')):
        photos.append(dir)
        try:
            photos.remove(last_used)
        except ValueError:
            pass
        print(photos)
        return photos
    for file in listdir(dir):
        if (file.lower().endswith('.png') or file.lower().endswith('.jpg')) and not file.lower().endswith('_vr.jpg'):
            if file == last_used:
                continue
            path_ = dir + '\\\\' + file
            print(f'     - {file}')
            photos.append(path_)
    return photos

def run():
    config = GenerateConfig()
    if config.get('OPTIONS', 'check_for_updates').lower() == "true": CheckForUpdates()
    exclusions = config.get('PATH', 'exclusions').split('+')
    paths = config.get('PATH', 'photos').split('+')
    photos = []
    for path_ in paths:
        glob_pattern = path.join(path_, '*')
        photos = photos + GetPhotosInDirectory(path_)
        files = sorted(glob(glob_pattern), key=path.getctime)
        for file in files:
            if path.isdir(file) and not file in exclusions:
                photos = photos + GetPhotosInDirectory(file)
    try:
        if len(photos) <= 1:
            print("Only one photo is available to pick from. Exiting early to save time.", True)
            if config.get('OPTIONS', 'pause_on_complete').lower() == 'true':
                input("Pause on Complete enabled in config_steam.ini, Press enter key to exit")
            
        new_photo = choice(photos)
    except IndexError:
        print('No photos to be found! Empty photos directory maybe?', True)
        input("Press enter key to exit.")
        exit()
    except:
        print(format_exc(), True)

    saveLastUsedPhoto(path.basename(new_photo))
    scaled = Resize(new_photo)
    
    # Set the path for Steam grid
    steamgridpath = config.get('PATH', 'steamgridpath')
    steamgridfile = config.get('PATH', 'steamgridfile')
    steam_grid_path = rf'{ steamgridpath }\{ steamgridfile }'
    
    # Save the new scaled photo to the Steam grid folder
    scaled.save(steam_grid_path)
    
    if config.get('OPTIONS', 'pause_on_complete').lower() == 'true':
        print("Image successfully scaled and replaced in Steam grid.", True)
        input("Pause on Complete enabled in config_steam.ini, Press enter key to exit")

if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print(format_exc(), True)
        input("Something went wrong, Press enter key to exit..")
        exit()
