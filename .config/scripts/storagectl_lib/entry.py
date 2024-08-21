class Entry:
    def __init__(self, name: str, size: str, type: str, mountpoint: str):
        self.name = name
        self.size = size
        self.type = type
        self.mountpoint = mountpoint

    def __str__(self):
        return f'{self.name} {self.type} {self.size} {self.mountpoint}'

    def is_usb(self) -> bool:
        return 'sd' in self.name

    def is_partition(self) -> bool:
        return self.type == 'part'

    def is_mounted(self) -> bool:
        return self.mountpoint != ''