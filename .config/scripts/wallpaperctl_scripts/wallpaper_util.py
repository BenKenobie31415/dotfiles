import os
import random
import re

last_wallpaper_cache = os.path.expanduser("~/.cache/scripts/wallpaperctl/last_wallpaper")
wallpaper_source_cache = os.path.expanduser("~/.cache/scripts/wallpaperctl/current_wallpaper_source")
blurred_images_folder = os.path.expanduser("~/.cache/scripts/wallpaperctl/blurred_images/")
scripts_folder = os.path.expanduser("~/.config/scripts/wallpaperctl_scripts/")

if not os.path.exists(last_wallpaper_cache):
    os.system(f"touch {last_wallpaper_cache}")
    print(f"touch {last_wallpaper_cache}")
if not os.path.exists(wallpaper_source_cache):
    os.system(f"touch {wallpaper_source_cache}")
    print(f"touch {wallpaper_source_cache}")
if not os.path.exists(blurred_images_folder):
    os.system(f"mkdir -p {blurred_images_folder}")
    print(f"mkdir -p {blurred_images_folder}")

def get_wallpaper_source() -> str:
    return read_first_line(wallpaper_source_cache)

def get_last_wallpaper() -> str:
    return read_first_line(last_wallpaper_cache)

def get_blurred_wallpaper(path_to_original: str) -> str:
    if blurred_image_exists(path_to_original):
        return path_to_original
    if os.path.exists(f"{blurred_images_folder}{os.path.basename(path_to_original)}"):
        return f'{blurred_images_folder}{os.path.basename(path_to_original)}'
    print(f'generating blurred version of {path_to_original}')
    blurred_image_path = f"{blurred_images_folder}{os.path.basename(path_to_original)}"
    os.system(f"magick {path_to_original} -resize 3000x1080 -filter Gaussian -blur 0x12 {blurred_image_path}")
    return blurred_image_path

def blurred_image_exists(name_of_original: str) -> bool:
    return name_of_original in os.popen(f"ls {blurred_images_folder}").read().split("\n")

def get_next_wallpaper() -> str:
    if not is_valid_wallpaper_source(get_wallpaper_source()):
        print("Invalid wallpaper source, image file or folder containing images required")
        return
    if is_wallpaper(get_wallpaper_source()):
        return get_wallpaper_source()
    images = get_image_files(get_wallpaper_source())
    return f'{get_wallpaper_source()}{images[random.randint(0, len(images) - 1)]}'

def write_last_wallpaper(file_name: str) -> None:
    with open(last_wallpaper_cache, "w") as cache:
        cache.write(file_name)

def is_valid_wallpaper_source(path: str) -> bool:
    return is_wallpaper(path) or is_wallpaper_folder(path)

def set_wallpaper(wallpaper_path: str) -> None:
    print(f"setting wallpaper to {wallpaper_path}")
    os.popen(f"feh --bg-scale {wallpaper_path}")
    os.system(f"betterlockscreen -u {get_blurred_wallpaper(wallpaper_path)} --fx")
    write_last_wallpaper(wallpaper_path)

def is_wallpaper(path: str) -> bool:
    if not os.path.exists(path):
        return False
    if os.path.isdir(path):
        return False
    return re.match(r".*\.(jpg|jpeg|png)", path)

def is_wallpaper_folder(path: str) -> bool:
    if not os.path.exists(path):
        return False
    if not os.path.isdir(path):
        return False
    return any([re.match(r".*\.(jpg|jpeg|png)", file) for file in os.listdir(path)])

def read_first_line(file_path: str) -> str:
    with open(file_path) as file:
        lines = file.readlines()
        if len(lines) == 0:
            return ""
        result = lines[0].replace("\n", "")
    return result

def get_image_files(folder_path: str) -> list[str]:
    return [f for f in os.listdir(folder_path) if is_wallpaper(f'{folder_path}{f}')]
