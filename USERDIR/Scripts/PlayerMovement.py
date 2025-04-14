from Scripting.Script import Script
from Input.Input import Input
from Logging.Logger import Logger
from Enums.LogType import LogType
from Sound.Sound import Sound
import pygame

class PlayerMovement(Script):
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

    def object1CollisionCallback(self, collidedWith, side):
        # if (side[0] != "NONE"): print(side[0])
        if (not(collidedWith.getParentGameObject().hasTag("Coin"))):
            self.object1CanMove = side
            self.colTop1 = side[1] == "BOTTOM"

    def start(self):
        self.gameObject.addTag("Player") # Make sure to tag correctly
        Logger.log("Set gravitational acceleration.", LogType.INFO, self.gameObject)
        self.gameObject.getComponent("RigidBody").setG(self.oG)

    def update(self):
        #Logger.log("I'm being called", LogType.INFO, self.gameObject)

        # Top collision check
        if (self.colTop1):
            self.gameObject.getComponent("RigidBody").setG(0)
            forceDir: pygame.Vector2 = self.gameObject.getComponent("RigidBody").getForceDirection()
            if (forceDir.y > 0): forceDir.y = 0
            self.gameObject.getComponent("RigidBody").setForce(forceDir, isMassiveY=False)
            self.gameObject.getComponent("RigidBody").setIsGrounded(True)
        else:
            self.gameObject.getComponent("RigidBody").setG(self.oG)

        if self.frames1 < 10:
            self.frames1 += 1
            return # Skip

        frozenRight = False
        frozenLeft = False
        if (self.inputHandler.isKeyPressed(pygame.K_w) and self.frames1 % 10 == 0):
            # Play sound
            self.soundHandler.playSound("jump", 0.15)
            forceDir: pygame.Vector2 = self.gameObject.getComponent("RigidBody").getForceDirection()
            forceDir.y = -self.jumpPower
            self.gameObject.getComponent("RigidBody").setForce(forceDir, isMassiveY=False)
            self.frames1 = 0

        #self.frames1 += 1