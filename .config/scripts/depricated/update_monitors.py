#!/usr/bin/env python3
import bspc
import subprocess
import os

internal_monitor_port: str = "eDP1"
external_monitor_port: str = "DP2-1"
desktop_numbers: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]

def main() -> None:
    xrandr_output = subprocess.check_output(["xrandr", "-q"]).decode("utf-8")
    if f"{external_monitor_port} connected" in xrandr_output:
        setup_dual_monitors()
    else:
        setup_single_monitor()

def setup_single_monitor() -> None:
    #move desktops to internal monitor
    for desktop_name in [str(number) for number in desktop_numbers]:
        bspc.move_desktop(desktop_name, internal_monitor_port)
    #set outputs
    os.popen(f"xrandr --output {internal_monitor_port} --primary --mode 1920x1080 --pos 0x0 --rotate normal --output {external_monitor_port} --off")
    bspc.remove_monitor(external_monitor_port)
    #order desktops
    bspc.bspc("monitor", internal_monitor_port, "-d", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0")

def setup_dual_monitors() -> None:
    bspc.bspc("monitor", external_monitor_port, "-a", "Desktop")
    internal_desktops: list[str] = [str(number) for number in (list(range(6, 10)) + [0])]
    external_desktops: list[str] = [str(number) for number in (list(range(1, 6)))]
    os.system(f"xrandr --output {internal_monitor_port} --mode 1920x1080 --pos 0x540 --rotate normal --output {external_monitor_port} --primary --mode 1920x1080 --pos 1920x0 --rotate normal")
    #os.system(f"xrandr --output {internal_monitor_port} --mode 1920x1080 --pos 0x1080 --rotate normal --output {external_monitor_port} --primary --mode 1920x1080 --pos 0x0 --rotate normal")
    for desktop_name in internal_desktops:
        bspc.move_desktop(desktop_name, internal_monitor_port)
    for desktop_name in external_desktops:
        bspc.move_desktop(desktop_name, external_monitor_port)
    bspc.bspc("desktop", "Desktop", "--remove")
    #reorder desktops
    bspc.bspc("monitor", external_monitor_port, "-d", "1", "2", "3", "4", "5")
    bspc.bspc("monitor", internal_monitor_port, "-d", "6", "7", "8", "9", "0")

if __name__ == "__main__":
    main()
