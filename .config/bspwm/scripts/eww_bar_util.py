import os
import bspc

def are_eww_windows_present(eww_window_names: list[str]) -> bool:
    return all([window_exists(window_name) for window_name in eww_window_names])

def update_focused_desktop_highlight() -> None:
    update_eww_var("activeworkspace", bspc.get_desktop_name(bspc.get_focused_desktop()))

def update_eww_var(var: str, value: str) -> None:
    os.popen(f"eww update {var}={value}")

def get_cropped_node_name(node_id: str, ignored_names: list[str]) -> str:
    name: str = bspc.get_node_name(node_id, bspc.get_desktop_of_node(node_id))
    if name in (ignored_names + [""]):
        return "desktop"
    if len(name) <= 64:
        return name
    return name[0:61] + "..."

def window_exists(window_name: str) -> bool:
    desktop_ids = bspc.get_desktop_ids()
    for desktop_id in desktop_ids:
        if window_name in bspc.get_window_names(desktop_id):
            return True
    return False
