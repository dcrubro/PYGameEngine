from Enums.LogType import LogType
from GameObject.Objects import GameObject

class Logger:
    @staticmethod
    def log(logMsg: str, logType: LogType, objectRef: GameObject):
        print(f"{logType.value}{logType.name}\033[0m from {objectRef.getName()}: {logMsg}")