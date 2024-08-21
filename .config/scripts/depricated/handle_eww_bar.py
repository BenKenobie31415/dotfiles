#!/usr/bin/env python3
import bspc
import time
import subprocess
import eww_bar_util
import os
from bspc_lib import *

main_monitor: str
side_monitor: str
eww_main_window_names: list[str] = ["Eww - bar_main", "Eww - darkbar_main"]
eww_side_window_names: list[str] = ["Eww - bar_side", "Eww - darkbar_side"]
eww_window_names: list[str]
eww_window_ids: list[str]
bar_node_id_main: str
bar_node_id_side: str
darkbar_node_id_main: str
darkbar_node_id_side: str

def main():
    global eww_window_ids
    global eww_window_names
    global bar_node_id_main
    global bar_node_id_side
    global darkbar_node_id_main
    global darkbar_node_id_side
    global main_monitor
    global side_monitor

    is_single = is_single_monitor()

    eww_window_names = eww_main_window_names
    if not is_single:
        eww_window_names += eww_side_window_names

    if is_single:
        main_monitor = bspc.get_monitor_id("eDP1")
        side_monitor = None
    else:
        main_monitor = bspc.get_monitor_id("HDMI2")
        side_monitor = bspc.get_monitor_id("eDP1")

    #Wait for Eww-bar to be initialized
    while not eww_bar_util.are_eww_windows_present(eww_window_names):
        time.sleep(0.5)
        print("waiting for eww windows")
    print("found eww windows")
    #caches ids that should be ignored for determining if a desktop is occupied
    eww_window_ids = [bspc.get_first_window_with_name(name) for name in eww_window_names]
    #caches the id of the two bar-windows for each monitor
    bar_node_id_main = bspc.get_first_window_with_name("Eww - bar_main")
    bar_node_id_side = bspc.get_first_window_with_name("Eww - bar_side")
    darkbar_node_id_main = bspc.get_first_window_with_name("Eww - darkbar_main")
    darkbar_node_id_side = bspc.get_first_window_with_name("Eww - darkbar_side")
    init_eww_bar()
    bspc.subscribe("desktop_focus", handle_desktop_focus)
    bspc.subscribe("node_remove", handle_node_remove)
    bspc.subscribe("node_add", handle_node_add)
    bspc.subscribe("node_transfer", handle_node_transfer)
    bspc.subscribe("node_state", handle_node_state)
    bspc.subscribe("node_focus", handle_node_focus)
    os.popen("notify-send Bar-Init finished")


def handle_desktop_focus(args: list[str]) -> None:
    start = time.time()
    eww_bar_util.update_focused_desktop_highlight()
    update_eww_bar()
    #print(f"{'handle desktop focus:':<30} {(1/60)/(time.time()-start)} frames")

def handle_node_remove(args: list[str]) -> None:
    start = time.time()
    update_eww_bar()
    #print(f"{'handle node remove:':<30} {(1/60)/(time.time()-start)} frames")

def handle_node_add(args: list[str]) -> None:
    start = time.time()
    update_eww_bar()
    #print(f"{'handle node add:':<30} {(1/60)/(time.time()-start)} frames")

def handle_node_transfer(args: list[str]) -> None:
    start = time.time()
    #ensures that only events get handled where a node gets moved to another desktop
    src_desktop_id = args[1]
    if bspc.get_focused_desktop() != src_desktop_id:
        return
    update_eww_bar()
    #print(f"{'handle node transfer:':<30} {(1/60)/(time.time()-start)} frames")

def handle_node_state(args: list[str]) -> None:
    start = time.time()
    update_eww_bar()
    #print(f"{'handle node state:':<30} {(1/60)/(time.time()-start)} frames")

def handle_node_focus(args: list[str]) -> None:
    ()
    # update_focused_name()

def set_darkbar_hidden(hidden: bool, main: bool) -> None:
    active_desktop_main = bspc.get_active_desktop(main_monitor)
    active_desktop_side = bspc.get_active_desktop(side_monitor)
    if hidden and main:
        bspc.set_node_flag(darkbar_node_id_main, "hidden", "on", active_desktop_main)
    elif not hidden and main:
        bspc.set_node_flag(darkbar_node_id_main, "hidden", "off", active_desktop_main)
    elif hidden and not main:
        bspc.set_node_flag(darkbar_node_id_side, "hidden", "on", active_desktop_side)
    elif not hidden and not main:
        bspc.set_node_flag(darkbar_node_id_side, "hidden", "off", active_desktop_side)

def init_eww_bar() -> None:
    init_eww_desktops()
    lock_eww_bar()
    eww_bar_util.update_focused_desktop_highlight()
    update_eww_bar()

def update_eww_bar() -> None:
    for desktop_id in bspc.get_active_desktops():
        set_darkbar_hidden(not is_desktop_occupied(desktop_id), is_main_monitor(bspc.get_monitor_of_desktop(desktop_id)))
    update_desktop_visibility()
    update_bar_visibility()
    # update_focused_name()

def init_eww_desktops() -> None:
    desktop_names = get_desktop_names()
    print(desktop_names)
    desktop_names.sort(key = lambda x: x)
    if (desktop_names[0] == 0):
        desktop_names.remove(0)
        desktop_names.append(0)
    eww_bar_util.update_eww_var("workspaceNumber", "\"" + str(desktop_names) + "\"")

def lock_eww_bar() -> None:
    active_desktop_main = bspc.get_active_desktop(main_monitor)
    active_desktop_side = bspc.get_active_desktop(side_monitor)
    bspc.set_node_flag(bar_node_id_main, "locked", "on", active_desktop_main)
    bspc.set_node_flag(bar_node_id_side, "locked", "on", active_desktop_side)
    bspc.set_node_flag(darkbar_node_id_main, "locked", "on", active_desktop_main)
    bspc.set_node_flag(darkbar_node_id_side, "locked", "on", active_desktop_side)

def update_desktop_visibility() -> None:
    visible_desktops = bspc.get_occupied_desktop_ids()
    desktop_ids = bspc.get_desktops()
    desktop_ids.sort(key=lambda x: bspc.get_desktop_name(x))
    desktop_visibility = [desktop_id in visible_desktops for desktop_id in desktop_ids]

    eww_bar_util.update_eww_var("workspaceVisibility", "\"" + str(desktop_visibility).lower() + "\"")

def update_focused_name() -> None:
    name = eww_bar_util.get_cropped_node_name(bspc.get_focused_node(), eww_window_names)
    eww_bar_util.update_eww_var("focusedname", "\"" + name + "\"")

def update_bar_visibility() -> None:
    fullscreen_nodes = bspc.query(Queryables.NODE, node_modifiers=[NodeMods.FULLSCREEN, NodeMods.ACTIVE])
    bspc.set_node_flag(bar_node_id_main, "hidden", "off", bspc.get_active_desktop(main_monitor))
    bspc.set_node_flag(bar_node_id_side, "hidden", "off", bspc.get_active_desktop(side_monitor))
    for node_id in fullscreen_nodes:
        desktop_id = bspc.get_desktop_of_node(node_id)
        is_main = is_main_monitor(bspc.get_monitor_of_desktop(desktop_id))
        if is_main:
            bspc.set_node_flag(bar_node_id_main, "hidden", "on", desktop_id)
        else:
            bspc.set_node_flag(bar_node_id_side, "hidden", "on", desktop_id)

def get_desktop_names() -> list[str]:
    return bspc.query(Queryables.DESKTOP, query_names=True)

def is_desktop_occupied(desktop_id: str) -> bool:
    return bspc.is_desktop_occupied(desktop_id, excluded_ids=eww_window_ids)

def is_main_monitor(monitor_id: str) -> bool:
    return main_monitor == monitor_id

def is_single_monitor() -> bool:
    cmd1 = ["xrandr", "-q"]
    cmd2 = ["grep", "HDMI2 connected"]
    return len(__get_decoded_output_piped(cmd1, cmd2)) == 0

def __get_decoded_output_piped(cmd1: list[str], cmd2: list[str]):
    p1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE)
    p2 = subprocess.Popen(cmd2, stdin=p1.stdout, stdout=subprocess.PIPE)
    output, _ = p2.communicate()
    p1.terminate()
    return output.decode("utf-8")

def __get_decoded_output(cmd: list[str]) -> list[str]:
    """Get the output of a command as a list of strings, where each string is a line of the output."""
    try:
        # [:-1] to remove the newline at the end
        return subprocess.check_output(cmd, encoding="utf-8")[:-1].split("\n")
    except subprocess.CalledProcessError:
        return []

if __name__ == "__main__":
    main()
