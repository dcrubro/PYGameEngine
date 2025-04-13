from Scripting.Script import Script
from Input.Input import Input
from Logging.Logger import Logger
from Enums.LogType import LogType
import pygame

class PlayerMovement(Script):
    def __init__(self, gameObject, inputHandler):
        super().__init__("PlayerMovement", gameObject)
        self.superSecretScriptIdentifierFlag = True
        self.inputHandler = inputHandler
        self.moveSpeed = 8
        self.jumpPower = 10
        self.object1CanMove = ["NONE", "NONE"]
        self.colTop1 = False
        self.oG = 9.81*2.5
        self.coinsCollected = 0

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
        frozenRight = False
        frozenLeft = False
        if (self.inputHandler.isKeyPressed(pygame.K_d)):
            if (self.object1CanMove[0] != "RIGHT" and not (frozenRight)):
                forceDir: pygame.Vector2 = self.gameObject.getComponent("RigidBody").getForceDirection()
                forceDir.x = self.moveSpeed
                self.gameObject.getComponent("RigidBody").setForce(forceDir, isMassiveY=False)
                frozenLeft = False
            else:
                self.gameObject.getComponent("RigidBody").setForce(pygame.Vector2(0, 0), isMassiveY=False)
                frozenRight = True
        if (self.inputHandler.isKeyPressed(pygame.K_a)):
            if (self.object1CanMove[0] != "LEFT" and not (frozenLeft)):
                forceDir: pygame.Vector2 = self.gameObject.getComponent("RigidBody").getForceDirection()
                forceDir.x = -self.moveSpeed
                self.gameObject.getComponent("RigidBody").setForce(forceDir, isMassiveY=False)
                frozenRight = False
            else:
                self.gameObject.getComponent("RigidBody").setForce(pygame.Vector2(0, 0), isMassiveY=False)
                frozenLeft = True
        if (self.inputHandler.isKeyPressed(pygame.K_w) and self.gameObject.getComponent("RigidBody").getIsGrounded()):
            forceDir: pygame.Vector2 = self.gameObject.getComponent("RigidBody").getForceDirection()
            forceDir.y = -self.jumpPower
            self.gameObject.getComponent("RigidBody").setForce(forceDir, isMassiveY=False)

        # Top collision check
        if (self.colTop1):
            self.gameObject.getComponent("RigidBody").setG(0)
            forceDir: pygame.Vector2 = self.gameObject.getComponent("RigidBody").getForceDirection()
            if (forceDir.y > 0): forceDir.y = 0
            self.gameObject.getComponent("RigidBody").setForce(forceDir, isMassiveY=False)
            self.gameObject.getComponent("RigidBody").setIsGrounded(True)
        else:
            self.gameObject.getComponent("RigidBody").setG(self.oG)