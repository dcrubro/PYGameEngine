"""
ImageLoader.py
This class is used for loading images into memory, thus making them faster to access than always reloading from disk every frame.
"""

import pygame
from Logging.Logger import Logger
from Enums.LogType import LogType
import os

class ImageLoader:
    def __init__(self):
        self.__images = dict()

    def getName(self):
        return "ImageLoader"

    def loadImage(self, name, path):
        if self.__images.get(name):
            Logger.log(f"An image with the name '{name}' is already loaded! The already loaded image will be overwritten!", LogType.WARNING, self)
        image = pygame.image.load(path)
        self.__images[name] = image
        Logger.log(f"Image at {path} has been loaded as '{name}'.", LogType.INFO, self)

    def autoLoadImages(self, rootDir):
        # Recursively load all .png and .jpg files from a specified root directory.
        for root, dirs, files in os.walk(rootDir):
            for file in files:
                if file.endswith((".png", ".jpg")):
                    fullPath = os.path.join(root, file) # Get the full path
                    fileName = os.path.splitext(file)[0] # Get the pure name
                    self.loadImage(fileName, fullPath) # Load the image

    def accessImage(self, name):
        return self.__images.get(name)

    def freeImage(self, name):
        if self.__images.get(name):
            del self.__images[name]
            Logger.log(f"Image '{name}' has been freed.", LogType.INFO, self)