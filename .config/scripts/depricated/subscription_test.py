import bspc

bspc.subscribe("node_add", callback=lambda _: print("added node"))
bspc.subscribe("node_remove", callback=lambda _: print("removed node"))
