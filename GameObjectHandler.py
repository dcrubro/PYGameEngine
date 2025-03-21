import pygame

from GameObject.Objects import GameObject
from Scripting.Script import Script

class GameObjectHandler:
    def __init__(self, gameObjects = dict()):
        self.__gameObjects = gameObjects

    def getGameObjects(self):
        return self.__gameObjects

    def setGameObjects(self, v: dict):
        self.__gameObjects = v

    def registerGameObject(self, object: GameObject):
        self.__gameObjects[object.getName()] = object
        # Call load on all scripts
        for comp in object.getComponents().values():
            try:
                if comp.superSecretScriptIdentifierFlag:
                    try:
                        comp.load()
                    except AttributeError:
                        continue # No load() defined
            except AttributeError:
                continue # Not a script

    def start(self):
        # Start logic
        for k, v in self.__gameObjects.items():
            v.start(self.__gameObjects)

    def update(self):
        #Update logic
        for k, v in self.__gameObjects.items():
            v.update(self.__gameObjects)

    def updateThenDraw(self, pygameInstance: pygame, screenInstance):
        # Update logic
        for k, v in self.__gameObjects.items():
            v.update(self.__gameObjects)
            v.draw(pygameInstance, screenInstance, v.getRotation())

    def drawThenUpdate(self, pygameInstance: pygame, screenInstance):
        # Update logic
        for k, v in self.__gameObjects.items():
            v.draw(pygameInstance, screenInstance, v.getRotation())
            v.update(self.__gameObjects)