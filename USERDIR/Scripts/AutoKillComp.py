import pygame
from GameObject.Objects import *
from Scripting.Script import Script
import random

class AutoKillComp(Script):
    def __init__(self, gameObject):
        super().__init__("AutoKillComp", gameObject)

    def start(self):
        if self.gameObject.hasTag("AutoKill"):
            # If this object already has the correct tag, we can safely assume that the player has restarted the game. As such, we should destroy it
            self.gameObject.destroySelf(restartAllComponents=False)
        self.gameObject.addTag("AutoKill") # Make sure to tag correctly

    def update(self):
        if self.gameObject.getPosition().x > -256:
            return # Skip

        self.gameObject.destroySelf(restartAllComponents=False) # When reached X coordinate, destroy