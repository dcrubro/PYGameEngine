from Components.BoxCollider import BoxCollider
from Components.RigidBody import RigidBody
from GameObject.Objects import GameObject, Rectangle
from IO.ResourceLoader import ResourceLoader
from IO.SaveLoad import SaveLoad
from Scripting.Script import Script
from Input.Input import Input
from Logging.Logger import Logger
from Enums.LogType import LogType
import pygame
from GameObjectHandler import GameObjectHandler
import os

# GameManager is a special type of script, which should be used for general tracking/event handling in your games.
# Only one of these should exist per game.
class GameManagerDoodle(Script):
    _coins = 0
    _scrollSpeed = 2
    _death = False
    _scrolledY = 0
    _maxY = 0
    _spawned = 0
    _hS = 0
    def __init__(self, gameObject, resLoaderPtr, screenPtr):
        super().__init__(f"GameManager{gameObject.getName()}", gameObject)
        self.superSecretScriptIdentifierFlag = True
        #self.centerPoint = pygame.Vector2(640, 700)
        self.previousPlayerPosition = None
        self.resLoaderPtr: ResourceLoader = resLoaderPtr
        self.screenPtr = screenPtr
        self.prevDelta = pygame.Vector2(0, 0)
        self.scrolledY = 0
        self.gameObjHandl: GameObjectHandler = None

    def start(self, gameObjHandl: GameObjectHandler):
        self.gameObjHandl = gameObjHandl
        GameManagerDoodle._maxY = 0
        GameManagerDoodle._scrolledY = 0
        Logger.log(f"Hit the R key at any time to restart!", LogType.IMPORTANT, self)
        self.gameObject.addTag("GameManager")
        player = gameObjHandl.getObjectByTag("Player")  # Get real player object
        if player:
            self.previousPlayerPosition = player.getPosition()  # Use real position
        else:
            Logger.log("Player not found during GameManager start.", LogType.ERROR, self)
            self.previousPlayerPosition = pygame.Vector2(0, 0)  # Fallback

    def update(self, screenResolution: pygame.Vector2, gameObjHandl: GameObjectHandler):
        # Temp Input Handler
        if Input(pygame).isKeyPressed(pygame.K_r):
            self.restartGame(gameObjHandl)

        if GameManagerDoodle._death:
            return

        playerY = gameObjHandl.getObjectByTag("Player").getPosition().y
        if (-playerY + GameManagerDoodle._scrolledY) > GameManagerDoodle._maxY:
            GameManagerDoodle._maxY = (-playerY + GameManagerDoodle._scrolledY)

        delta = pygame.Vector2(0, 3.5)
        GameManagerDoodle._scrolledY += delta.y

        for k, v in gameObjHandl.getGameObjects().items():
            if v.hasTag("Player") or v.hasTag("BG"):
                continue
            v.moveBy(delta)

        self.prevDelta = delta

        #Logger.log(f"Delta: {delta}", LogType.INFO, self)

        # Some basic font rendering - this currently isn't handled by an Engine Class, but I will make one someday
        #font: pygame.font.Font = self.resLoaderPtr.accessResource("Roboto-Bold")

    def lateUpdate(self, gameObjHandl: GameObjectHandler):
        # As the name implies, this runs after update()
        player: GameObject = gameObjHandl.getObjectByTag("Player")
        if not player:
            return
        self.previousPlayerPosition = player.getPosition()  # Update AFTER everything moved
        font = pygame.font.Font( # Sadly, the way fonts work in pygame is stupid, and requires you to specify the size on load. :(
            os.path.dirname(os.path.realpath(__file__)) + "/../../Textures/fonts/Roboto/Roboto-Bold.ttf", 32)
        text = font.render("Height: " + str(int(GameManagerDoodle._maxY)), True, "black")

        if not(player.getComponents()["PlayerMovement"].isAlive):
            text2 = font.render("YOU DIED", True, "red")
            text3 = font.render("(Press 'R' to restart)", True, "red")
            text4 = font.render(f"Highscore: {int(GameManagerDoodle._hS)}", True, "blue")
            self.screenPtr.blit(text2, (570, 290))
            self.screenPtr.blit(text3, (500, 350))
            self.screenPtr.blit(text4, (510, 410))

        self.screenPtr.blit(text, (0, 0))

    #@classmethod
    #def addCoin(cls):
    #    cls._coins += 1
    #    Logger.log(f"Coins: {cls._coins}", LogType.INFO, cls)
    #    if cls._coins % 5 == 0:
    #        cls.increaseSpeed()
    #    return cls._coins

    #@classmethod
    #def getCoins(cls):
    #    return cls._coins

    #@classmethod
    #def increaseSpeed(cls):
    #    cls._scrollSpeed += 0.2

    @classmethod
    def die(cls):
        # HighScore saving
        highScore = SaveLoad.getValue("doodleHighScore")
        if highScore is None:
            highScore = 0

        highScore = max(cls._maxY, highScore)
        SaveLoad.saveValue("doodleHighScore", highScore)
        cls._hS = highScore

        cls._death = True

    def restartGame(self, gameObjHandl: GameObjectHandler):
        if self.resetGame():
            platformTest: Rectangle = Rectangle("PlatformTest", pygame.Vector2(200, 100), 0,
                                                                pygame.Vector2(75, 10), "#300000")
            platformTest.addComponent(
                RigidBody("RigidBody", platformTest, 720, 1, bounciness=0, friction=0.1,
                          isSimulated=False))
            platformTest.addComponent(BoxCollider("BoxCollider", platformTest, 1, 21, None))
            self.gameObjHandl.registerGameObject(platformTest, start=True)
            gameObjHandl.start()

    @classmethod
    def resetGame(cls):
        if cls._death: # Only allow reset if dead
            Logger.log("Restarting game.", LogType.WARNING, cls)
            cls._maxY = 0
            cls._scrolledY = 0
            cls._spawned = 0
            cls._death = False
            return True
        return False