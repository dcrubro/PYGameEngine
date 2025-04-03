from Enums.LogType import LogType

class Logger:
    @staticmethod
    def log(logMsg: str, logType: LogType, objectRef):
        print(f"{logType.value}{logType.name}\033[0m from {objectRef}: {logMsg}")