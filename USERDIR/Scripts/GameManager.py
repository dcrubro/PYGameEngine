from Scripting.Script import Script
from Input.Input import Input
from Logging.Logger import Logger
from Enums.LogType import LogType
import pygame
from GameObjectHandler import GameObjectHandler

# GameManager is a special type of script, which should be used for general tracking/event handling in your games.
# Only one of these should exist per game.
class GameManager(Script):
    _coins = 0
    _scrollSpeed = 2
    def __init__(self, gameObject):
        super().__init__(f"GameManager{gameObject.getName()}", gameObject)
        self.superSecretScriptIdentifierFlag = True
        #self.centerPoint = pygame.Vector2(640, 700)
        self.previousPlayerPosition = None

    def start(self, gameObjHandl: GameObjectHandler):
        self.gameObject.addTag("GameManager")
        player = gameObjHandl.getObjectByTag("Player")  # Get real player object
        if player:
            self.previousPlayerPosition = player.getPosition()  # Use real position
        else:
            Logger.log("Player not found during GameManager start.", LogType.ERROR, self)
            self.previousPlayerPosition = pygame.Vector2(0, 0)  # Fallback

    def update(self, screenResolution: pygame.Vector2, gameObjHandl: GameObjectHandler):
        #player = gameObjHandl.getObjectByTag("Player")
        #if not player:
        #    Logger.log("Player not found during update.", LogType.ERROR, self)
        #    return

        #playerPosition: pygame.Vector2 = player.getPosition()

        #if self.previousPlayerPosition is None:
        #    self.previousPlayerPosition = playerPosition
        #    return  # Skip first frame

        #delta = playerPosition - self.previousPlayerPosition
        delta = pygame.Vector2(self._scrollSpeed, 0)

        #Logger.log(f"Delta Vector: {delta.x}, {delta.y}", LogType.INFO, self)

        for k, v in gameObjHandl.getGameObjects().items():
            if v.hasTag("Player"):
                continue
            v.moveBy(-delta)

    def lateUpdate(self, gameObjHandl: GameObjectHandler):
        """This runs AFTER the player has finished moving."""
        player = gameObjHandl.getObjectByTag("Player")
        if not player:
            return
        self.previousPlayerPosition = player.getPosition()  # Update AFTER everything moved

    @classmethod
    def addCoin(cls):
        cls._coins += 1
        Logger.log(f"Coins: {cls._coins}", LogType.INFO, cls)
        if cls._coins % 10 == 0:
            cls.increaseSpeed()
        return cls._coins

    @classmethod
    def increaseSpeed(cls):
        cls._scrollSpeed += 0.2