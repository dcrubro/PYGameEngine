import pygame
from GameObject.Objects import *
from Scripting.Script import Script
import random

class AutoKillComp(Script):
    def __init__(self, gameObject):
        super().__init__("AutoKillComp", gameObject)

    def start(self):
        self.gameObject.addTag("AutoKill") # Make sure to tag correctly

    def update(self):
        if self.gameObject.getPosition().x > -256:
            return # Skip

        self.gameObject.destroySelf(False) # When reached X coordinate, destroy