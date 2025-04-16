from IO.ResourceLoader import ResourceLoader
from Scripting.Script import Script
from Input.Input import Input
from Logging.Logger import Logger
from Enums.LogType import LogType
import pygame
from GameObjectHandler import GameObjectHandler
import os

# GameManager is a special type of script, which should be used for general tracking/event handling in your games.
# Only one of these should exist per game.
class GameManager(Script):
    _coins = 0
    _scrollSpeed = 2
    _death = False
    def __init__(self, gameObject, resLoaderPtr, screenPtr):
        super().__init__(f"GameManager{gameObject.getName()}", gameObject)
        self.superSecretScriptIdentifierFlag = True
        #self.centerPoint = pygame.Vector2(640, 700)
        self.previousPlayerPosition = None
        self.resLoaderPtr: ResourceLoader = resLoaderPtr
        self.screenPtr = screenPtr

    def start(self, gameObjHandl: GameObjectHandler):
        Logger.log(f"Hit the R key at any time to restart!", LogType.IMPORTANT, self)
        self.gameObject.addTag("GameManager")
        player = gameObjHandl.getObjectByTag("Player")  # Get real player object
        if player:
            self.previousPlayerPosition = player.getPosition()  # Use real position
        else:
            Logger.log("Player not found during GameManager start.", LogType.ERROR, self)
            self.previousPlayerPosition = pygame.Vector2(0, 0)  # Fallback

    def update(self, screenResolution: pygame.Vector2, gameObjHandl: GameObjectHandler):
        delta = pygame.Vector2(self._scrollSpeed, 0)

        for k, v in gameObjHandl.getGameObjects().items():
            if v.hasTag("Player"):
                continue
            v.moveBy(-delta)

        # Some basic font rendering - this currently isn't handled by an Engine Class, but I will make one someday
        #font: pygame.font.Font = self.resLoaderPtr.accessResource("Roboto-Bold")

    def lateUpdate(self, gameObjHandl: GameObjectHandler):
        """This runs AFTER the player has finished moving."""
        player = gameObjHandl.getObjectByTag("Player")
        if not player:
            return
        self.previousPlayerPosition = player.getPosition()  # Update AFTER everything moved
        font = pygame.font.Font(
            os.path.dirname(os.path.realpath(__file__)) + "/../Textures/fonts/Roboto/Roboto-Bold.ttf", 32)
        text = font.render("Coins: " + str(self.getCoins()), True, "black")
        self.screenPtr.blit(text, (0, 0))

    @classmethod
    def addCoin(cls):
        cls._coins += 1
        Logger.log(f"Coins: {cls._coins}", LogType.INFO, cls)
        if cls._coins % 5 == 0:
            cls.increaseSpeed()
        return cls._coins

    @classmethod
    def getCoins(cls):
        return cls._coins

    @classmethod
    def increaseSpeed(cls):
        cls._scrollSpeed += 0.2

    @classmethod
    def die(cls):
        cls._death = True
        cls._scrollSpeed = 0

    @classmethod
    def resetScene(cls):
        pass