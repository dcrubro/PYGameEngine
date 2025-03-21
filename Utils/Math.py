# Math.py - simple wrapper for the python math library, adding more methods and physical constants

import math

class Math:
    @staticmethod
    def infinity() -> float:
        return math.inf

    @staticmethod
    def neginfinity() -> float:
        return -math.inf

    @staticmethod
    def shortpi() -> float:
        return 3.141592654

    @staticmethod
    def pi() -> float:
        return 3.1415926535897932384626433832795028841971693993751

    @staticmethod
    def G() -> float:
        return 6.67e-11

    @staticmethod
    def c() -> int:
        return 299792458

    @staticmethod
    def clamp(val: float, minV: float, maxV: float):
        return max(min(val, maxV), minV)