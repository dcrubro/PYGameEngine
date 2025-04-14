import pygame
from GameObject.Objects import *
from Scripting.Script import Script
import random

class AutoKillComp(Script):
    def __init__(self, gameObject):
        super().__init__("AutoKillComp", gameObject)
        self.ttl = 900 # Frame count before auto-destroy
        self.frames = 0

    def start(self):
        self.gameObject.addTag("AutoKill") # Make sure to tag correctly

    def update(self):
        if self.frames < self.ttl:
            self.frames += 1
            return # Skip

        self.gameObject.destroySelf(False) # When reached TTL count, destroy self