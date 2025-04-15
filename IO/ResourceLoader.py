"""
ResourceLoader.py
This class is used for loading resources into memory, thus making them faster to access than always reloading from disk every frame.
"""

import pygame
from Logging.Logger import Logger
from Enums.LogType import LogType
import os

class ResourceLoader:
    def __init__(self):
        self.__resources = dict()
        self.loadResource("pygameengine_missing_texture", "Resources/missing_texture.png")

    def getName(self):
        return "ResourceLoader"

    def loadResource(self, name, path):
        if self.__resources.get(name):
            Logger.log(f"A resource with the name '{name}' is already loaded! The already loaded resource will be overwritten!", LogType.WARNING, self)

        if path.endswith((".png", ".jpg")):
            resource = pygame.image.load(path).convert_alpha()
            self.__resources[name] = resource
            Logger.log(f"Resource at {path} has been loaded as '{name}'.", LogType.INFO, self)
        elif path.endswith(".wav"):
            resource = pygame.mixer.Sound(path)
            self.__resources[name] = resource
            Logger.log(f"Resource at {path} has been loaded as '{name}'.", LogType.INFO, self)
        else:
            Logger.log(f"Could not figure out how to load the resource as '{name}' (PYGE_TYPE_UNKNOWN_ERROR, PYGE_NON_FATAL_ERROR).", LogType.ERROR, self)

    def autoLoadResources(self, rootDir, ingoreList=tuple()):
        # Recursively load all .png and .jpg files from a specified root directory.
        for root, dirs, files in os.walk(rootDir):
            for file in files:
                if file.endswith((".png", ".jpg", ".wav")) and not(os.path.splitext(file)[0] in ingoreList):
                    fullPath = os.path.join(root, file) # Get the full path
                    fileName = os.path.splitext(file)[0] # Get the pure name
                    self.loadResource(fileName, fullPath) # Load the image

    def accessResource(self, name, returnIfMissing = True):
        if name in self.__resources:
            return self.__resources[name]
        elif returnIfMissing:
            Logger.log("Tried to access an unknown resource!", LogType.WARNING, self)
            return self.__resources["pygameengine_missing_texture"]
        Logger.log("Tried to access an unknown resource!", LogType.WARNING, self)

    def freeResource(self, name):
        if self.__resources.get(name):
            del self.__resources[name]
            Logger.log(f"Resource '{name}' has been freed.", LogType.INFO, self)

    def freeAll(self):
        self.__resources.clear()
        Logger.log(f"Freed all resources.", LogType.INFO, self)