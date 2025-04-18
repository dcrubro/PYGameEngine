from Enums.ForceType import ForceType
from Scripting.Script import Script
from Input.Input import Input
from Logging.Logger import Logger
from Enums.LogType import LogType
from Sound.Sound import Sound
import pygame

from USERDIR.Scripts.GameManager import GameManager

class PlayerMovementDoodle(Script):
    def __init__(self, gameObject, inputHandler, soundHandler: Sound):
        super().__init__("PlayerMovement", gameObject)
        self.superSecretScriptIdentifierFlag = True
        self.inputHandler = inputHandler
        self.moveSpeed = 8
        self.jumpPower = 6
        self.object1CanMove = ["NONE", "NONE"]
        self.colTop1 = False
        self.oG = 9.81*2.5
        self.coinsCollected = 0
        self.soundHandler: Sound = soundHandler
        self.frames1 = 0
        self.frames2 = 0
        self.isAlive = True

    def addZeForceee(self):
        self.gameObject.getComponent("RigidBody").setForce(pygame.Vector2(self.gameObject.getComponent("RigidBody").getForceDirection().x, -15), ForceType.INSTANT)

    def object1CollisionCallback(self, collidedWith, side):
        #print(side)
        # if (side[0] != "NONE"): print(side[0])
        if side[1] == "BOTTOM" or self.gameObject.getComponent("RigidBody").getIsGrounded():
            self.addZeForceee()
        #elif (not(collidedWith.getParentGameObject().hasTag("Platform"))) and self.isAlive:
        #    Logger.log("You died!", LogType.INFO, self)
        #    self.soundHandler.playSound("death", 0.15)
        #    self.isAlive = False
        #    GameManager.die()
        #    self.gameObject.setTexture("BirdDead")
            #self.gameObject.getComponent("RigidBody").setFrozenAxis((False, True))

    def start(self):
        self.gameObject.setTexture("DoodleChar")
        self.isAlive = True
        self.gameObject.setPosition(pygame.Vector2(200, 200))
        self.gameObject.addTag("Player") # Make sure to tag correctly
        Logger.log("Set gravitational acceleration.", LogType.INFO, self.gameObject)
        self.gameObject.getComponent("RigidBody").setG(self.oG)
        self.gameObject.getComponent("RigidBody").setFrozenAxis((False, False))

    def update(self):
        # Top collision check
        if self.isAlive:
            #if (self.colTop1):
            #    self.gameObject.getComponent("RigidBody").setG(0)
            #    forceDir: pygame.Vector2 = self.gameObject.getComponent("RigidBody").getForceDirection()
            #    if (forceDir.y > 0): forceDir.y = 0
            #    self.gameObject.getComponent("RigidBody").setForce(forceDir, isMassiveY=False)
            #    self.gameObject.getComponent("RigidBody").setIsGrounded(True)
            #else:
            #    self.gameObject.getComponent("RigidBody").setG(self.oG)

            if self.gameObject.getComponent("RigidBody").getIsGrounded() and False:
                Logger.log("You died!", LogType.INFO, self)
                self.soundHandler.playSound("death", 0.15)
                self.gameObject.setTexture("BirdDead")
                self.isAlive = False
                GameManager.die()

            # Input section
            #if self.frames1 < 10:
            #    self.frames1 += 1
            #    return # Skip

            #if ((self.inputHandler.isKeyPressed(pygame.K_w) or self.inputHandler.isKeyPressed(pygame.K_SPACE)) and self.frames1 % 10 == 0 and self.gameObject.getPosition().y > 0):
            #    # Play sound
            #    self.soundHandler.playSound("jump", 0.15)
            #    forceDir: pygame.Vector2 = self.gameObject.getComponent("RigidBody").getForceDirection()
            #    forceDir.y = -self.jumpPower
            #    self.gameObject.getComponent("RigidBody").setForce(forceDir, isMassiveY=False)
            #    self.frames1 = 0

            if self.inputHandler.isKeyPressed(pygame.K_d):
                self.gameObject.getComponent("RigidBody").setForce(pygame.Vector2(4, self.gameObject.getComponent("RigidBody").getForceDirection().y), ForceType.INSTANT)
            if self.inputHandler.isKeyPressed(pygame.K_a):
                self.gameObject.getComponent("RigidBody").setForce(pygame.Vector2(-4, self.gameObject.getComponent("RigidBody").getForceDirection().y), ForceType.INSTANT)
