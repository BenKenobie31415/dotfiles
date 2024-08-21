#!/usr/bin/env python3
import bspc
import time

def main():
    bspc.subscribe("desktop_focus", focus_pointed_node)
    bspc.subscribe("node_remove", focus_pointed_node)
    bspc.subscribe("node_add", focus_pointed_node)
    bspc.subscribe("node_transfer", focus_pointed_node)

def focus_pointed_node(args: list[str]) -> None:
    pointed_window = bspc.get_pointed_window()
    if not pointed_window:
        return
    bspc.focus_node(pointed_window)

if __name__ == "__main__":
    main()