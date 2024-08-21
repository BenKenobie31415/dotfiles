#!/usr/bin/env python3
import bspc
from bspc_lib import *

def main():
    fullscreen_windows: list[str] = bspc.query(Queryables.NODE, node_modifiers=[NodeMods.FULLSCREEN])
    focused_node = bspc.get_focused_node()
    if len(fullscreen_windows) < 1:
        window_ids = bspc.get_window_ids()
        if focused_node not in window_ids:
            return
        bspc.set_node_state(focused_node, NodeState.FULLSCREEN)
        return
    bspc.set_node_state(fullscreen_windows[0], NodeState.TILED)

if __name__ == '__main__':
    main()
