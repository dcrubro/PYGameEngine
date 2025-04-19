import pygame

from Components.BoxCollider import BoxCollider
from Components.RigidBody import RigidBody
from GameObject.Objects import *
from Scripting.Script import Script
from IO.ResourceLoader import ResourceLoader
from GameObjectHandler import GameObjectHandler
import math

from Sound.Sound import Sound
from USERDIR.Scripts.AutoKillComp import AutoKillComp
import random

from USERDIR.Scripts.Coin import Coin
from USERDIR.Scripts.Doodle.AutoKillCompDoodle import AutoKillCompDoodle
from USERDIR.Scripts.Doodle.GameManagerDoodle import GameManagerDoodle
from USERDIR.Scripts.GameManager import GameManager
from Utils.Math import Math

class PlatSpawner(Script):
    def __init__(self, gameObject, gMHandl, resLoaderPtr, sndHandl):
        super().__init__("PipeSpawner", gameObject)
        self.frames1 = 0
        self.gMHandl: GameObjectHandler = gMHandl
        self.resLoaderPtr: ResourceLoader = resLoaderPtr
        self.sndHandl = sndHandl
        self.topLevelY = 100
        self.platCnt = 7
        self.maxPlats = 90

    def spawnSection(self):
        if GameManagerDoodle._maxY % 2000 == 0 and self.platCnt > 5:
            self.platCnt -= 1 # Increase the difficulty every 2000 height gained

        if not(self.gMHandl.getGameObjectByName("PlayerObj").getComponents()["PlayerMovement"].isAlive):
            return # Skip, player is dead

        for i in range(self.platCnt):
            if GameManagerDoodle._spawned >= self.maxPlats:
                continue

            randomId = random.randint(-32767, 32767)
            randomPosX = random.randint(0, 1280) # Pretty unlikely for 2 to spawn next to each other
            objTop: Rectangle = Rectangle(f"Platform{randomId}", pygame.Vector2(randomPosX, random.randint(self.topLevelY - 500, self.topLevelY - 100)), 0, pygame.Vector2(75, 10), "#300000")
            objTop.addTag("Platform")
            objTop.addComponent(AutoKillCompDoodle(objTop, self.gMHandl))
            objTop.addComponent(RigidBody("RigidBody", objTop, 0, 1, isSimulated=False))
            objTop.addComponent(BoxCollider("BoxCollider", objTop, 1, 1, None))
            self.gMHandl.registerGameObject(objTop, start=True)
            GameManagerDoodle._spawned += 1

        self.topLevelY -= 100

    def start(self):
        # Reset the counters
        self.platCnt = 10
        self.topLevelY = 100

    def update(self):
        # ChatGPT helped with this logic.
        platformProgress = -self.topLevelY  # upward distance of highest spawned platform
        maxClimb = GameManagerDoodle._maxY

        if platformProgress < maxClimb + 650 and self.frames1 % 80 == 0:
            #print(f"Total platforms: {len(self.gMHandl.getObjectsByTag('Platform'))}")
            #print(f"Spawning section: platformProgress={platformProgress}, maxClimb={maxClimb}")
            self.spawnSection()
            self.frames1 = 0

        self.frames1 += 1 # Limit spawn speed to every 80 frames to help avoid lag