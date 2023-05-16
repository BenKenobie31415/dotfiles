from i3ipc import Connection, Event
import subprocess
import os
import math
import zmq

i3 = Connection()
context = zmq.Context()

socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

def set_eww_window_name(name):
     send(f"eww update focusedname='{name}'")

def send(message: str):
    socket.send_string(message)
    socket.recv()




def get_focused_title():
    focused = i3.get_tree().find_focused()
    if (focused.type == "workspace"):
        return "desktop"
    return focused.window_title

def updateBar(self, e):
    #set_eww_window_name(get_focused_title())
    if (get_focused_title() == "desktop"):
        send('xdotool search --class "eww-bar-blur" set_window --class "eww-bar"')

    else:
        send('xdotool search --class "eww-bar" set_window --class "eww-bar-blur"')

def updateBarOnHotkey(self, e):
    maxBrightness = float(subprocess.check_output(["brightnessctl", "m"]))
    currentBrightness = float(subprocess.check_output(["brightnessctl", "g"]))
    percentage = math.ceil(100*(currentBrightness/maxBrightness))
    send(f"eww update brightness={percentage}")

updateBarOnHotkey(None, None)

i3.on(Event.WORKSPACE_FOCUS, updateBar)
i3.on(Event.WINDOW_FOCUS, updateBar)
i3.on(Event.WINDOW_CLOSE, updateBar)
i3.on(Event.BINDING, updateBar)
i3.on(Event.BINDING, updateBarOnHotkey)

i3.main()