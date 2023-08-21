#!/usr/bin/env python3
import subprocess
import os
import time

backgrounds_cache: str = "/home/benkenobi/.config/bspwm/scripts/cache/background_list"
bg_folder_path: str = "/home/benkenobi/Pictures/BackgroundImages/arch/"
bg_blurred_folder_path: str = "/home/benkenobi/Pictures/BackgroundImages/arch_blurred/"

def main() -> None:
    old_bgs = read_background_cache()
    new_bgs = read_directory(bg_folder_path)
    blrd_bgs = read_directory(bg_blurred_folder_path)
    write_background_cache()
    added = [new_bg for new_bg in new_bgs if new_bg not in old_bgs or new_bg not in blrd_bgs]
    removed = [old_bg for old_bg in old_bgs if old_bg not in new_bgs]
    remove_blurred_bgs(removed)
    generate_blurred_bg(added)

def read_background_cache() -> list[str]:
    with open(backgrounds_cache, "r") as file:
        return [element.replace("\n", "") for element in file.readlines()]

def write_background_cache() -> None:
    current_bgs = read_directory(bg_folder_path)
    with open(backgrounds_cache, "w") as file:
        file.writelines([bg + "\n" for bg in current_bgs])

def read_directory(folder: str) -> list[str]:
    return subprocess.check_output(["ls", folder], encoding="utf-8").split()

def remove_blurred_bgs(bgs: list[str]) -> None:
    for bg in bgs:
        os.popen(f"rm {bg_blurred_folder_path}{bg}")

def generate_blurred_bg(bgs: list[str]) -> None:
    for bg in bgs:
        os.system(f"convert {bg_folder_path}{bg} -resize 3000x1080 -filter Gaussian -blur 0x12 {bg_blurred_folder_path}{bg}")
        os.system(f"convert {bg_blurred_folder_path}{bg} -draw \"roundrectangle 150,880 350,990 10,10\" -fill \#11111b {bg_blurred_folder_path+bg}")

if __name__ == "__main__":
    main()

