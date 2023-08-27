#!/usr/bin/env python3
import subprocess
import threading
import socket
import os
from bspc_lib import *
from time import time

socket_path = "/tmp/bspwm_0_0-socket"
try:
    socket_path = os.environ["BSPWM_SOCKET"]
except KeyError:
    pass

def __get_decoded_output(cmd: list[str]) -> list[str]:
    """Get the output of a command as a list of strings, where each string is a line of the output."""
    try:
        # [:-1] to remove the newline at the end
        return subprocess.check_output(cmd, encoding="utf-8")[:-1].split("\n")
    except subprocess.CalledProcessError:
        return []

def bspc(*command: str):
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect(socket_path)
    cmd = b"\x00".join(argument.encode("utf-8") for argument in command)
    client.send(cmd + b"\x00")
    data = client.recv(4096)
    if data:
        data = data.decode("utf-8")
        client.close()
        return data.split("\n")[:-1]
    # [:-1] to remove the newline at the end
    client.close()
    return None

def modifiers_to_string(modifiers) -> str:
    result = ""
    for modifier in modifiers:
        result += modifier.value
    return result

def query(query_object: Queryables,
              monitor_modifiers: list[MonitorMods]=[],
              monitor_descriptor: str=None,
              desktop_modifiers: list[DesktopMods]=[],
              desktop_descriptor: str=None,
              node_modifiers: list[NodeMods]=[],
              node_descriptor: str=None,
              query_names: bool=False) -> list[str]:
    start = time()
    cmd = ["query", query_object.value]

    monitor_sel = ""
    if monitor_descriptor:
        monitor_sel += monitor_descriptor
    if len(monitor_modifiers) > 0:
        monitor_sel += modifiers_to_string(monitor_modifiers)
    if len(monitor_sel) > 0:
        cmd.append("-m")
        cmd.append(monitor_sel)

    desktop_sel = ""
    if desktop_descriptor:
        desktop_sel += desktop_descriptor
    if len(desktop_modifiers) > 0:
        desktop_sel += modifiers_to_string(desktop_modifiers)
    if len(desktop_sel) > 0:
        cmd.append("-d")
        cmd.append(desktop_sel)

    node_sel = ""
    if node_descriptor:
        node_sel += node_descriptor
    if len(node_modifiers) > 0:
        node_sel += modifiers_to_string(node_modifiers)
    if len(node_sel) > 0:
        cmd.append("-n")
        cmd.append(node_sel)

    if query_names and (query_object == Queryables.MONITOR or query_object == Queryables.DESKTOP):
        cmd.append("--names")
    #end = time()
    #cmd_string = ""
    #for arg in cmd:
        #cmd_string += " " + arg
    #print(f"finished [{cmd_string:<40}] in {end-start}s")
    return bspc(*cmd)

#Monitor querys
def get_monitor_ids() -> list[str]:
    return query(Queryables.MONITOR)

def get_focused_monitor() -> str:
    return query(Queryables.MONITOR, monitor_modifiers=[MonitorMods.FOCUSED])[0]

def get_monitor_id(port: str) -> str:
    ids = query(Queryables.MONITOR, monitor_descriptor=port)
    if len(ids) == 0:
        return None
    return ids[0]

#Desktop querys
def get_desktops(monitor_id: str=None, query_names: bool=False) -> list[str]:
    return query(Queryables.DESKTOP, monitor_descriptor=monitor_id, query_names=query_names)

def get_focused_desktop() -> str:
    return query(Queryables.DESKTOP, desktop_modifiers=[DesktopMods.FOCUSED])[0]

def get_active_desktops() -> list[str]:
    return query(Queryables.DESKTOP, desktop_modifiers=[DesktopMods.ACTIVE])

def get_desktop_name(desktop_id: str) -> str:
    ids = query(Queryables.DESKTOP, desktop_descriptor=desktop_id, query_names=True)
    if len(ids) == 0:
        return None
    return ids[0]

def get_first_free_desktop_id() -> str:
    free_desktops = query(Queryables.DESKTOP, desktop_modifiers=[DesktopMods.NOT_OCCUPIED])
    if len(free_desktops) == 0:
        return None
    return free_desktops[0]

def get_active_desktop(monitor_id: str) -> str:
    for desktop in get_active_desktops():
        if get_monitor_of_desktop(desktop) == monitor_id:
            return desktop
    return None

def get_desktop_of_node(node_id: str) -> str:
    for desktop_id in get_desktops():
        if node_id in get_node_ids(desktop_id):
            return desktop_id
    return None

def get_occupied_desktop_ids(ignored_node_ids: list[str]=[]) -> list[str]:
    return [desktop_id for desktop_id in query(Queryables.DESKTOP, desktop_modifiers=[DesktopMods.OCCUPIED]) if all([node_id not in ignored_node_ids for node_id in get_node_ids(desktop_id)])]

#Node querys
#TODO make desktop modifiers more modular not just desktop-id
def get_node_ids(desktop_id: str=None, excluded: list[str]=[]) -> list[str]:
    ids = query(Queryables.NODE, desktop_descriptor=desktop_id)
    return [id for id in ids if not id in excluded]

def get_window_ids(desktop_id: str=None, excluded: list[str]=[]):
    ids = query(Queryables.NODE, node_modifiers=[NodeMods.WINDOW], desktop_descriptor=desktop_id)
    return [id for id in ids if not id in excluded]

def get_focused_node() -> str:
    nodes = query(Queryables.NODE, node_modifiers=[NodeMods.FOCUSED])
    if len(nodes) == 0:
        return None
    return nodes[0]

def get_pointed_window() -> str:
    windows = query(Queryables.NODE, node_descriptor="pointed", node_modifiers=[NodeMods.WINDOW])
    if len(windows) == 0:
        return None
    return windows[0]

def get_root_node() -> str:
    node = bspc("query", "-N", "-d", "-n", "@focused:/")
    if node == []:
        return None
    return node[0]

def get_node_name(node_id: str, desktop_id: str) -> str:
    if node_id not in get_node_ids(desktop_id):
        return "node does not exist"
    cmd = ["xtitle"]
    cmd.extend([node_id])
    title = __get_decoded_output(cmd)[0]
    return title

def get_window_names(desktop_id: str) -> list[str]:
    ids = get_window_ids(desktop_id)
    if len(ids) == 0:
        return []
    cmd = ["xtitle"]
    cmd.extend(ids)
    return __get_decoded_output(cmd)

def get_first_window_with_name(window_name: str, desktop_id: str = None) -> str:
    if desktop_id:
        desktop_ids = [desktop_id]
    else:
        desktop_ids = get_desktops()
    for desktop_id in desktop_ids:
        window_ids = get_window_ids(desktop_id)
        for window_id in window_ids:
            if (get_node_name(window_id, desktop_id) == window_name):
                return window_id
    return None

def get_monitor_of_desktop(desktop_id: str) -> str:
    monitor_ids = get_monitor_ids()
    for monitor_id in monitor_ids:
        if desktop_id in get_desktops(monitor_id):
            return monitor_id
    return None

#State checker
def is_desktop_empty_except(excluded_names: list[str], desktop_id: str) -> bool:
    windows = get_node_ids(desktop_id)
    for window in windows:
        if get_node_name(window, desktop_id) not in excluded_names:
            return False
    return True

def is_desktop_occupied(desktop_id: str, excluded_ids: list[str]=[]) -> bool:
    return len(get_window_ids(desktop_id, excluded=excluded_ids)) > 0


#State-Setter
def focus_desktop(desktop_id: str) -> None:
    bspc("desktop", "-f", desktop_id)

def focus_node(node_id: str) -> None:
    bspc("node", "-f", node_id)

def focus_next_free_desktop() -> None:
    focus_desktop(get_first_free_desktop_id())

def rename_desktop(name: str, desktop_id: str) -> None:
    bspc("desktop", desktop_id, "-n", name)

def remove_desktop(desktop: str) -> None:
    bspc("desktop", desktop, "--remove")

def move_desktop(desktop: str, monitor: str) -> None:
    bspc("desktop", desktop, "--to-monitor", monitor)

def remove_monitor(monitor_port: str) -> None:
    bspc("monitor", monitor_port, "-r")

def set_node_flag(node_id: str, flag: str, value: str, desktop_id: str) -> None:
    if not node_id or not desktop_id:
        return
    if node_id not in get_node_ids(desktop_id):
        return
    bspc("node", node_id, "-g", flag + "=" + value)

def __add_subscriber(event:str, callback, *callback_args):
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect(socket_path)
    client.send(b"subscribe\x00" + event.encode() + b"\x00")
    while True:
        # [:-1] to remove the newline at the end
        data = client.recv(4096).decode("utf-8")[:-1]
        if data:
            # [1:] to remove the event name
            args = data.split(" ")[1:]
            callback(args, *callback_args)

def subscribe(event:str, callback, *callback_args):
    """Subscribe to an event and call the callback when the event is triggered.
        Callback should take the event arguments (list[str]) as the first argument, and any other arguments as the rest."""
    t = threading.Thread(target=__add_subscriber, args=(event, callback, *callback_args))
    t.start()
