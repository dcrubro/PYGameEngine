import pygame
from GameObject.Objects import *
from Scripting.Script import Script
import random

class AutoKillCompDoodle(Script):
    def __init__(self, gameObject, gMHandl):
        super().__init__("AutoKillComp", gameObject)
        self.gMHandl = gMHandl

    def start(self):
        if self.gameObject.hasTag("AutoKill"):
            # If this object already has the correct tag, we can safely assume that the player has restarted the game. As such, we should destroy it
            self.gameObject.destroySelf(restartAllComponents=False)
        self.gameObject.addTag("AutoKill") # Make sure to tag correctly

    def update(self):
        if abs(self.gMHandl.getGameObjectByName("PlayerObj").getPosition().y - self.gameObject.getPosition().y) >= 512:
            self.gameObject.destroySelf(restartAllComponents=False) # When reached Y coordinate, destroy