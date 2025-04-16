from Scripting.Script import Script
from Input.Input import Input
from Logging.Logger import Logger
from Enums.LogType import LogType
import pygame

from Sound.Sound import Sound
from USERDIR.Scripts.GameManager import GameManager

class Coin(Script):
    def __init__(self, gameObject, sndHandl: Sound):
        super().__init__(f"Coin{gameObject.getName()}", gameObject)
        self.superSecretScriptIdentifierFlag = True
        self.frames = 0
        self.imgIndex = 1
        self.sndHandl: Sound = sndHandl

    def collisionCallback(self, collidedWith, side):
        # if (side[0] != "NONE"): print(side[0])
        #Logger.log(f"Bruh", LogType.INFO, self)
        Logger.log(f"{collidedWith.getParentGameObject().getName()}", LogType.INFO, self)
        if (collidedWith.getParentGameObject().getName() == "PlayerObj"):
            Logger.log(f"{self.gameObject.getName()} (OBJ) Collided with {collidedWith.getParentGameObject().getName()}!", LogType.INFO, self)
            GameManager.addCoin()
            self.sndHandl.playSound("coinpickup", 0.15)
            # Destroy the object
            self.gameObject.destroySelf(True)

    def start(self):
        self.gameObject.addTag("Coin")

    def update(self):
        # A simple animation cycle for the coin.
        self.frames += 1
        if (self.frames == 14): # Wait 15 frames
            self.frames = 0
            self.gameObject.setTexture(f"coin{self.imgIndex}")
            self.imgIndex += 1
            if (self.imgIndex > 6):
                self.imgIndex = 1