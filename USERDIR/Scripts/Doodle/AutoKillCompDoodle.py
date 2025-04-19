import pygame
from GameObject.Objects import *
from Scripting.Script import Script
import random

from USERDIR.Scripts.Doodle.GameManagerDoodle import GameManagerDoodle


class AutoKillCompDoodle(Script):
    def __init__(self, gameObject, gMHandl):
        super().__init__("AutoKillComp", gameObject)
        self.gMHandl = gMHandl

    def start(self):
        if self.gameObject.hasTag("AutoKill"):
            # If this object already has the correct tag, we can safely assume that the player has restarted the game. As such, we should destroy it
            self.gameObject.destroySelf(restartAllComponents=True)
            GameManagerDoodle._spawned -= 1
        self.gameObject.addTag("AutoKill") # Make sure to tag correctly

    def update(self):
        #playerObj = self.gMHandl.getObjectByTag("Player")
        #playerY = playerObj.getPosition().y
        selfY = self.gameObject.getPosition().y
        
        #isUnderPlayer = selfY > playerY

        #timeBehind = Time.getTime() - self.gameObject.lastRenderTime
        #print(f"{self.gameObject.getName()}: Is under player:", isUnderPlayer, f"Time behind: {timeBehind}")

        # Check if the object hasn't rendered in over 1 second (assuming 60 FPS)
        #if timeBehind >= 60 and isUnderPlayer:
        if selfY >= 720: #0px below the screen
            print("Deleted")
            self.gameObject.destroySelf(restartAllComponents=True)
            GameManagerDoodle._spawned -= 1