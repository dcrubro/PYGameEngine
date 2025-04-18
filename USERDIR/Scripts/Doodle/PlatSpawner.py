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
        self.platCnt = 5
        #self.spawned = 0

    def spawnSection(self):
        if not(self.gMHandl.getGameObjectByName("PlayerObj").getComponents()["PlayerMovement"].isAlive):
            return # Skip, player is dead


        for i in range(self.platCnt):
            randomId = random.randint(-32767, 32767)
            randomPosX = random.randint(0, 1280) # Pretty unlikely for 2 to spawn next to each other
            objTop: Rectangle = Rectangle(f"Platform{randomId}", pygame.Vector2(randomPosX, self.topLevelY - 100), 0,
                                                                pygame.Vector2(75, 10), "red")
            objTop.addTag("Platform")
            objTop.addComponent(AutoKillCompDoodle(objTop, self.gMHandl))
            objTop.addComponent(RigidBody("RigidBody", objTop, 0, 1, isSimulated=False))
            objTop.addComponent(BoxCollider("BoxCollider", objTop, 1, 1, None))
            self.gMHandl.registerGameObject(objTop, start=True)
            #self.spawned += 1
            #print(self.spawned)

        self.topLevelY -= 100

    def start(self):
        self.spawnFrameLimit = 200 # Reset the spawn speed on start (death case)

    def update(self):
        diff = abs(self.gMHandl.getGameObjectByName("PlayerObj").getPosition().y - self.topLevelY)
        print(diff)
        if diff < 450:
            print("Spawned")
            # Spawn platform level, player is getting close
            self.spawnSection()

        self.frames1 = 0
        #self.spawnSection()