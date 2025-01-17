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
    current_version = "0.0.2"
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

def Resize(path, target_width=1920, target_height=620):
    image = Image.open(path)
    
    # Calculate the scaling factor to fill the target dimensions
    ratio = max(target_width / image.width, target_height / image.height)

    # New dimensions that will cover the target area
    x = int(image.width * ratio)
    y = int(image.height * ratio)

    # Resize the image to the new dimensions
    image = image.resize((x, y))

    # Crop the image to the target dimensions by cutting off excess parts from the center
    left = (x - target_width) // 2
    top = (y - target_height) // 2
    right = left + target_width
    bottom = top + target_height

    cropped_image = image.crop((left, top, right, bottom))

    return cropped_image


def GenerateConfig():
    sections = ('PATH', 'OPTIONS')
    options = [
        ['PATH', 'photos', ''],
        ['PATH', 'exclusions', ''],
        ['PATH', 'steamgridpath', 'C:\\Program Files (x86)\\Steam\\userdata\\123456789\\config\\grid'],
        ['PATH', 'steamgridfile', '438100_hero.jpg'],
        ['PATH', 'grid_image_1', '438100p.png'],
        ['PATH', 'grid_image_2', '438100.png'],
        ['OPTIONS', 'pause_on_complete', 'false'],
        ['OPTIONS', 'check_for_updates', 'true'],
        ['OPTIONS', 'output_to_cmd', 'false'],
        ['OPTIONS', 'replace_grid_images', 'false']
    ]
    config = ConfigParser()

    config_file_exists = run_bat_exists = True
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

    if path.exists('config_steam.ini'):
        config.read('config_steam.ini')
        
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

    # Set the path for Steam grid (Hero image)
    steamgridpath = config.get('PATH', 'steamgridpath')
    steamgridfile = config.get('PATH', 'steamgridfile')
    steam_grid_path = rf'{steamgridpath}\\{steamgridfile}'

    # Save the new scaled hero photo to the Steam grid folder
    scaled.save(steam_grid_path)
    print(f"Hero image replaced: {steam_grid_path}")

    # Check if grid images should be replaced
    if config.get('OPTIONS', 'replace_grid_images').lower() == 'true':
        grid_image_1 = config.get('PATH', 'grid_image_1')
        grid_image_2 = config.get('PATH', 'grid_image_2')
        
        grid_image_1_path = path.join(steamgridpath, grid_image_1)
        grid_image_2_path = path.join(steamgridpath, grid_image_2)
        
        # Resize and save the grid images
        scaled_grid_1 = Resize(new_photo, target_width=1215, target_height=2160)
        scaled_grid_2 = Resize(new_photo, target_width=3840, target_height=2160)
        
        scaled_grid_1.save(grid_image_1_path)
        scaled_grid_2.save(grid_image_2_path)
        print("Grid images replaced.")

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
