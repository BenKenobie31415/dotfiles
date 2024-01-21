#!/usr/bin/env python3
import bspc
import time
import subprocess
import eww_bar_util
import os
from bspc_lib import *

main_monitor: str
eww_main_window_names: list[str] = ["Eww - bar_main", "Eww - darkbar_main"]
eww_window_names: list[str]
eww_window_ids: list[str]
bar_node_id_main: str
darkbar_node_id_main: str

def main():
    global eww_window_ids
    global eww_window_names
    global bar_node_id_main
    global darkbar_node_id_main
    global main_monitor

    eww_window_names = eww_main_window_names
    main_monitor = bspc.query(Queryables.MONITOR, monitor_modifiers=[MonitorMods.FOCUSED])[0]

    #Wait for Eww-bar to be initialized
    while not eww_bar_util.are_eww_windows_present(eww_window_names):
        time.sleep(0.5)
        print(bspc.get_window_names(bspc.get_active_desktop(main_monitor)))
    print("found eww windows")
    #caches ids that should be ignored for determining if a desktop is occupied
    eww_window_ids = [bspc.get_first_window_with_name(name) for name in eww_window_names]
    #caches the id of the two bar-windows for each monitor
    bar_node_id_main = bspc.get_first_window_with_name("Eww - bar_main")
    darkbar_node_id_main = bspc.get_first_window_with_name("Eww - darkbar_main")
    init_eww_bar()
    bspc.subscribe("desktop_focus", handle_desktop_focus)
    bspc.subscribe("node_remove", handle_node_remove)
    bspc.subscribe("node_add", handle_node_add)
    bspc.subscribe("node_transfer", handle_node_transfer)
    bspc.subscribe("node_state", handle_node_state)
    bspc.subscribe("node_focus", handle_node_focus)
    os.popen("notify-send Bar-Init finished")


def handle_desktop_focus(args: list[str]) -> None:
    eww_bar_util.update_focused_desktop_highlight()
    update_eww_bar()

def handle_node_remove(args: list[str]) -> None:
    update_eww_bar()

def handle_node_add(args: list[str]) -> None:
    update_eww_bar()

def handle_node_transfer(args: list[str]) -> None:
    #ensures that only events get handled where a node gets moved to another desktop
    src_desktop_id = args[1]
    if bspc.get_focused_desktop() != src_desktop_id:
        return
    update_eww_bar()

def handle_node_state(args: list[str]) -> None:
    update_eww_bar()

def handle_node_focus(args: list[str]) -> None:
    update_focused_name()

def set_darkbar_hidden(hidden: bool, main: bool) -> None:
    active_desktop_main = bspc.get_active_desktop(main_monitor)
    if hidden and main:
        bspc.set_node_flag(darkbar_node_id_main, "hidden", "on", active_desktop_main)
    elif not hidden and main:
        bspc.set_node_flag(darkbar_node_id_main, "hidden", "off", active_desktop_main)

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
    update_focused_name()

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
    bspc.set_node_flag(bar_node_id_main, "locked", "on", active_desktop_main)
    bspc.set_node_flag(darkbar_node_id_main, "locked", "on", active_desktop_main)

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
    for node_id in fullscreen_nodes:
        desktop_id = bspc.get_desktop_of_node(node_id)
        bspc.set_node_flag(bar_node_id_main, "hidden", "on", desktop_id)

def get_desktop_names() -> list[str]:
    return bspc.query(Queryables.DESKTOP, query_names=True)

def is_desktop_occupied(desktop_id: str) -> bool:
    return bspc.is_desktop_occupied(desktop_id, excluded_ids=eww_window_ids)

def is_main_monitor(monitor_id: str) -> bool:
    return main_monitor == monitor_id

if __name__ == "__main__":
    main()
