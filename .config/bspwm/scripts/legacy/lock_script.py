#!/usr/bin/env python3
from change_background import get_last_background
from generate_blurred_backgrounds import bg_blurred_folder_path
import os
import time
import subprocess

def main():
    script_location = "/home/benkenobi/.config/bspwm/scripts/lock_script"
    current_bg: str = get_last_background()
    blurred_bg: str = bg_blurred_folder_path + current_bg
    subprocess.Popen([script_location, blurred_bg])

if __name__ == "__main__":
    main()
