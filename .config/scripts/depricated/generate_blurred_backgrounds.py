#!/usr/bin/env python3
import os
from change_background_new import get_background_folder

backgrounds_cache: str = "/home/benkenobi/.config/bspwm/scripts/cache/background_list"
bg_blurred_folder_path: str = "/home/benkenobi/.config/bspwm/scripts/cache/images/"

def main() -> None:
    old_bgs = read_background_cache()
    new_bgs = read_directory(get_background_folder())
    blrd_bgs = read_directory(bg_blurred_folder_path)
    write_background_cache()
    added = [new_bg for new_bg in new_bgs if new_bg not in old_bgs or new_bg not in blrd_bgs]
    removed = [old_bg for old_bg in old_bgs if old_bg not in new_bgs]
    removed += [blrd_bg for blrd_bg in blrd_bgs if blrd_bg not in new_bgs and blrd_bg not in removed]
    if len(removed) == 0 and len(added) == 0:
        print("Blurred versions up to date")
        return
    remove_blurred_bgs(removed)
    generate_blurred_bg(added)

def read_background_cache() -> list[str]:
    with open(backgrounds_cache, "r") as file:
        return [element.replace("\n", "") for element in file.readlines()]

def write_background_cache() -> None:
    current_bgs = read_directory(get_background_folder())
    with open(backgrounds_cache, "w") as file:
        file.writelines([bg + "\n" for bg in current_bgs])

def read_directory(folder: str) -> list[str]:
    return os.popen(f"ls {folder}").read().split()

def remove_blurred_bgs(bgs: list[str]) -> None:
    for bg in bgs:
        print(f"Removing {bg_blurred_folder_path}{bg}")
        os.popen(f"rm {bg_blurred_folder_path}{bg}")

def generate_blurred_bg(bgs: list[str]) -> None:
    for bg in bgs:
        print(f"Generating {bg_blurred_folder_path}{bg}")
        os.system(f"convert {get_background_folder()}{bg} -resize 3000x1080 -filter Gaussian -blur 0x12 {bg_blurred_folder_path}{bg}")

if __name__ == "__main__":
    main()

