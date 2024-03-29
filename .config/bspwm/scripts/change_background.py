#!/usr/bin/env python3
import os
import random
import subprocess

background_images_path: str = "/home/benkenobi/Pictures/BackgroundImages/arch/"
cache_path = "/home/benkenobi/.config/bspwm/scripts/cache/last_background"

def main():
    more_than_one_bg = len(os.popen(f"ls {background_images_path}").read().split()) >= 1
    random_background = get_random_background()
    while random_background == get_last_background() and more_than_one_bg:
        random_background = get_random_background()
    set_background(random_background)

def set_background(file_name: str) -> None:
    #notify(background_images_path + file_name, "benkenobi")
    os.system(f"feh --bg-scale {background_images_path + file_name}")
    write_last_background(file_name)

def get_last_background() -> str:
    with open(cache_path, "r") as cache:
        result = cache.readlines()[0].replace("\n", "")
    return result

def write_last_background(file_name: str) -> None:
    with open(cache_path, "w") as cache:
        cache.write(file_name)

def get_random_background() -> str:
    images = os.popen(f"ls {background_images_path}").read().split()
    return images[random.randint(0, len(images)-1)]

def notify(message: str, user: str):
    id = int(subprocess.check_output(f"id -u {user}".split(" ")))
    os.system(f"sudo -u {user} DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/{id}/bus notify-send '{message}'")

if __name__ == "__main__":
    main()
