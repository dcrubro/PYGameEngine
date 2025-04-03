import pygame

from GameObject.Objects import GameObject
from Scripting.Script import Script

class GameObjectHandler:
    def __init__(self, srceenDimensions: pygame.Vector2, gameObjects = dict()):
        self.__gameObjects = gameObjects
        self.__srceenDimensions = srceenDimensions

    def getGameObjects(self):
        return self.__gameObjects

    def setGameObjects(self, v: dict):
        self.__gameObjects = v

    def registerGameObject(self, object: GameObject):
        self.__gameObjects[object.getName()] = object
        # Call load on all scripts
        for comp in object.getComponents().values():
            if isinstance(comp, Script):
                if hasattr(comp, "load"):
                    comp.load()

    def start(self):
        # Start logic
        for k, v in self.__gameObjects.items():
            v.start(self.__gameObjects)

    def update(self):
        #Update logic
        for k, v in self.__gameObjects.items():
            v.update(self.__gameObjects)

    def updateThenDraw(self, pygameInstance: pygame, screenInstance, centerPos: pygame.Vector2, toleranceMultiplier = 1):
        # Update logic
        for k, v in self.__gameObjects.items():
            v.update(self.__gameObjects)
            if (v.getPosition().x >= (centerPos.x - (self.__srceenDimensions.x // 2) * toleranceMultiplier) and v.getPosition().x <= (centerPos.x + (self.__srceenDimensions.x // 2) * toleranceMultiplier)):
                v.draw(pygameInstance, screenInstance, v.getRotation())

    def drawThenUpdate(self, pygameInstance: pygame, screenInstance, centerPos: pygame.Vector2):
        # Update logic
        for k, v in self.__gameObjects.items():
            v.draw(pygameInstance, screenInstance, v.getRotation())
            v.update(self.__gameObjects)