from enum import Enum

class LogType(Enum):
    INFO = ""
    WARNING = "\033[33m"
    ERROR = "\033[31m"
    DESCRIPTION = '\033[92m'