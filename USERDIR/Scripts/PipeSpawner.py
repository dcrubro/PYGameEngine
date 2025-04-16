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
from USERDIR.Scripts.GameManager import GameManager
from Utils.Math import Math


class PipeSpawner(Script):
    def __init__(self, gameObject, gMHandl, resLoaderPtr, sndHandl):
        super().__init__("PipeSpawner", gameObject)
        self.frames1 = 0
        self.yCoof = 5.76 # 720 / 125 px
        self.gMHandl: GameObjectHandler = gMHandl
        self.resLoaderPtr: ResourceLoader = resLoaderPtr
        self.sndHandl = sndHandl
        self.spawnFrameLimit = 200

    def spawnSection(self):
        if not(self.gMHandl.getGameObjectByName("PlayerObj").getComponents()["PlayerMovement"].isAlive):
            return # Skip, player is dead

        if GameManager.getCoins() % 5 == 0 and GameManager.getCoins() > 0:
            self.spawnFrameLimit /= 1.1

        randomId = random.randint(-32767, 32767)
        pipeWidth = 125
        gapSize = 100
        pipeBodHeight = 600

        gapY = random.randint(150, 500)

        topPipeY = gapY - pipeBodHeight
        objTop = Sprite(f"PipeTop{randomId}", self.resLoaderPtr, pygame.Vector2(1350, topPipeY), 0,
                         pygame.Vector2(pipeWidth, pipeBodHeight), "Pipe")
        objTop.addTag("Pipe")
        objTop.addComponent(AutoKillComp(objTop))
        objTop.addComponent(RigidBody("RigidBody", objTop, 0, 1, isSimulated=False))
        objTop.addComponent(BoxCollider("BoxCollider", objTop, 1, 1, None))
        self.gMHandl.registerGameObject(objTop, start=True)

        bottomPipeY = Math.clamp(gapY + gapSize + 60, 420, 32767)
        coinY = (bottomPipeY - 60) - 60 - 180
        coinObj = Sprite(f"Coin{randomId}", self.resLoaderPtr, pygame.Vector2(1350, coinY), 0, pygame.Vector2(75, 75), "coin1")
        coinObj.addTag("Coin")
        coinScr = Coin(coinObj, self.sndHandl)
        coinObj.addComponent(RigidBody("RigidBody", coinObj, 0, 1, isSimulated=False))
        coinObj.addComponent(BoxCollider("BoxCollider", coinObj, 1, 1, coinScr.collisionCallback))
        coinObj.addComponent(coinScr)
        coinObj.addComponent(AutoKillComp(coinObj))
        self.gMHandl.registerGameObject(coinObj, start=True)

        print(bottomPipeY)
        #bottomPipeY = 404
        objBot = Sprite(f"PipeBot{randomId}", self.resLoaderPtr, pygame.Vector2(1350, bottomPipeY + 50), 0,
                         pygame.Vector2(pipeWidth, pipeBodHeight * 0.9), "Pipe")
        objTop.addTag("Pipe")
        objBot.addComponent(AutoKillComp(objBot))
        objBot.addComponent(RigidBody("RigidBody", objBot, 0, 1, isSimulated=False))
        objBot.addComponent(BoxCollider("BoxCollider", objBot, -5, 1, None))
        self.gMHandl.registerGameObject(objBot, start=True)
    def start(self):
        pass

    def update(self):
        if self.frames1 < self.spawnFrameLimit:
            self.frames1 += 1
            return # Skip

        self.frames1 = 0
        self.spawnSection()