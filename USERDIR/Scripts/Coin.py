from Scripting.Script import Script
from Input.Input import Input
from Logging.Logger import Logger
from Enums.LogType import LogType
import pygame

class Coin(Script):
    def __init__(self, gameObject):
        super().__init__(f"Coin{gameObject.getName()}", gameObject)
        self.superSecretScriptIdentifierFlag = True
        self.baseTexDir = "USERDIR/Textures/coin/"
        self.frames = 0
        self.imgIndex = 1

    def object1CollisionCallback(self, collidedWith, side):
        # if (side[0] != "NONE"): print(side[0])
        self.object1CanMove = side
        self.colTop1 = side[1] == "BOTTOM"

    def start(self):
        pass

    def update(self):
        #Logger.log("I'm being called", LogType.INFO, self.gameObject)
        # A simple animation cycle for the coin.
        self.frames += 1
        if (self.frames == 14): # Wait 15 frames
            self.frames = 0
            self.gameObject.setTexture(f"coin{self.imgIndex}")
            self.imgIndex += 1
            if (self.imgIndex > 6):
                self.imgIndex = 1