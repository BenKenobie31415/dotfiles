import bspc

def main():
    bspc.subscribe("monitor_add", handle_monitor_add)
    bspc.subscribe("monitor_remove", handle_monitor_remove)

def handle_monitor_add(args: list[str]):
    print("added monitor")

def handle_monitor_remove(args: list[str]):
    print("removed monitor")

if __name__ == "__main__":
    main()
