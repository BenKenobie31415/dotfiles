from enum import Enum

class Queryables(Enum):
    MONITOR="-M"
    DESKTOP="-D"
    NODE="-N"

class MonitorMods(Enum):
    FOCUSED=".focused"
    NOT_FOCUSED=".!focused"
    OCCUPIED=".occupied"
    NOT_OCCUPIED=".!occupied"

class DesktopMods(Enum):
    FOCUSED=".focused"
    NOT_FOCUSED=".!focused"
    ACTIVE=".active"
    NOT_ACTIVE=".!active"
    OCCUPIED=".occupied"
    NOT_OCCUPIED=".!occupied"
    URGENT=".urgent"
    NOT_URGENT=".!urgent"
    LOCAL=".local"
    NOT_LOCAL=".!local"

class NodeMods(Enum):
    FOCUSED=".focused"
    NOT_FOCUSED=".!focused"
    ACTIVE=".active"
    NOT_ACTIVE=".!active"
    LOCAL=".local"
    NOT_LOCAL=".!local"
    LEAF=".leaf"
    NOT_LEAF=".!leaf"
    WINDOW=".window"
    NOT_WINDOW=".!window"

    TILED=".tiled"
    NOT_TILED=".!tiled"
    PSEUDO_TILED=".pseudo_tiled"
    NOT_PSEUDO_TILED=".!pseudo_tiled"
    FLOATING=".floating"
    NOT_FLOATING=".!floating"
    FULLSCREEN=".fullscreen"
    NOT_FULLSCREEN=".!fullscreen"

    HIDDEN=".hidden"
    NOT_HIDDEN=".!hidden"
    STICKY=".sticky"
    NOT_STICKY=".!sticky"
    PRIVATE=".private"
    NOT_PRIVATE=".!private"
    LOCKED=".locked"
    NOT_LOCKED=".!locked"
    MARKED=".marked"
    NOT_MARKED=".!marked"
    URGENT=".urgent"
    NOT_URGENT=".!urgent"

    BELOW=".below"
    NOT_BELOW=".!below"
    NORMAL=".normal"
    NOT_NORMAL=".!normal"
    ABOVE=".above"
    NOT_ABOVE=".!above"

    HORIZONTAL=".horizontal"
    NOT_HORIZONTAL=".!horizontal"
    VERTICAL=".vertical"
    NOT_VERTICAL=".!vertical"

class NodeState(Enum):
    TILED="tiled"
    PSEUDO_TILED="pseudo_tiled"
    FLOATING="floating"
    FULLSCREEN="fullscreen"
