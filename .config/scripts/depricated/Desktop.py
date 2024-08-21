from dataclasses import dataclass
import bspc

ignored_names = ["Eww - bar", "Eww - darkbar"]
ignored_ids = [bspc.get_first_window_with_name(name, bspc.get_focused_desktop()) for name in ignored_names]

@dataclass
class Desktop:
    id: str
    name: str
    applications: list[str]

    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name
        self.applications = bspc.get_node_ids(self.id, excluded=ignored_ids)

    def handle_node_add(self):
        self.applications = bspc.get_node_ids(self.id, excluded=ignored_ids)
        #print(self.applications, " should not include", ignored_ids)

    def handle_node_remove(self):
        self.applications = bspc.get_node_ids(self.id, excluded=ignored_ids)
        #print(self.applications, " should not include", ignored_ids)

    def is_occupied(self) -> bool:
        #print(bspc.get_desktop_name(self.id), ": ", str([bspc.get_node_name(application) for application in self.applications]), " is occupied: ", len(self.applications) > 0)
        return len(self.applications) > 0
