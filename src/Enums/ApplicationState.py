from enum import Enum


class ApplicationState(Enum):
    RUNNING = 0
    RESTART = 1
    BREAK = 2
    STOP = 3
    MUSIC_BREAK = 4
