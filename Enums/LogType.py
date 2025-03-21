from enum import Enum

class LogType(Enum):
    INFO = "INFO"
    WARNING = "\033[33m"
    ERROR = "\033[31m"