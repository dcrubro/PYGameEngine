class Time:
    # Simple class to track the "time" (frames) of the game in GameObjects.
    _time = 0
    def __init__(self):
        pass

    @classmethod
    def getTime(self): return Time._time

    @classmethod
    def increment(self): Time._time += 1