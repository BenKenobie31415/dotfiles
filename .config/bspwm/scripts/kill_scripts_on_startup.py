#!/usr/bin/env python3
import subprocess
import os

ps = subprocess.Popen(["ps", "-ef"], stdout=subprocess.PIPE)
output_lines = subprocess.check_output(["grep", "python"], stdin=ps.stdout).decode("utf-8").split("\n")

script_path = "/home/benkenobi/.config/bspwm/scripts/"
scripts_to_kill = ["HandleEwwBar.py", "HandleFocus.py"]
paths_to_kill = [script_path + script for script in scripts_to_kill]

filtered_lines = [line for line in output_lines if any([path in line for path in paths_to_kill])]
pids = [line.split()[1] for line in filtered_lines]

for pid in pids:
    os.popen(f"kill {pid} PID")
