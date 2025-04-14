import pygame
from GameObject.Objects import *
from Scripting.Script import Script
from IO.ResourceLoader import ResourceLoader
from GameObjectHandler import GameObjectHandler
import math
from USERDIR.Scripts.AutoKillComp import AutoKillComp
import random

class PipeSpawner(Script):
    def __init__(self, gameObject, gMHandl, resLoaderPtr):
        super().__init__("PipeSpawner", gameObject)
        self.frames1 = 0
        self.yCoof = 5.76 # 720 / 125 px
        self.gMHandl: GameObjectHandler = gMHandl
        self.resLoaderPtr: ResourceLoader = resLoaderPtr

    def spawnSection(self):
        randomId = random.randint(-32767, 32767)
        randOut = random.randint(1, 4)

        # Due to the limitations of python, and the amount of calculations that are made with physics, rendering, etc., you shouldn't carelessly add objects like this.
        # This is simply a proof of concept
        objp = Sprite(f"Pipe{randomId}", self.resLoaderPtr, pygame.Vector2(1350, 0), 0, pygame.Vector2(125, 125 * (randOut + 1)), "Pipe")
        kllp = AutoKillComp(objp)
        objp.addComponent(kllp)
        self.gMHandl.registerGameObject(objp)

        obj = Sprite(f"PipeEnd{randomId}", self.resLoaderPtr, pygame.Vector2(1350, (randOut + 0) * 125), 0, pygame.Vector2(125, 125), "PipeEnd")
        kll = AutoKillComp(obj)
        obj.addComponent(kll)
        self.gMHandl.registerGameObject(obj)

        """
        objd = Sprite(f"PipeEndD{randomId}", self.resLoaderPtr, pygame.Vector2(1350, (randOut + 0) * 125), 180, pygame.Vector2(125, 125), "PipeEnd")
        klld = AutoKillComp(objd)
        objd.addComponent(klld)
        self.gMHandl.registerGameObject(objd)
        """

        """
        objr = Sprite(f"PipeD{randomId}", self.resLoaderPtr, pygame.Vector2(1350, 125 * (randOut + 2)), 0,pygame.Vector2(125, 125 * 10), "Pipe")
        kllr = AutoKillComp(objr)
        objr.addComponent(kllr)
        self.gMHandl.registerGameObject(objr)
        """

    def start(self):
        pass

    def update(self):
        if self.frames1 < 200:
            self.frames1 += 1
            return # Skip

        self.frames1 = 0
        self.spawnSection()