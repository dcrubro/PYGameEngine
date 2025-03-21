from Enums.LogType import LogType
from Logging.Logger import Logger
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

    moveSpeed = 8
    global object1CanMove
    object1CanMove = ""
    colTop1 = False

    def object1CollisionCallback(self, collidedWith, side):
        # if (side[0] != "NONE"): print(side[0])
        global object1CanMove
        object1CanMove = side
        global colTop1
        colTop1 = side[1] == "BOTTOM"

    def update(self):
        Logger.log("I'm being called", LogType.INFO, self.__gameObject)
        # Called every frame
        frozenRight = False
        frozenLeft = False
        if (self.inputHandler.isKeyPressed(pygame.K_d)):
            if (object1CanMove[0] != "RIGHT" and not (frozenRight)):
                forceDir: pygame.Vector2 = self.__gameObject.getComponent("RigidBody").getForceDirection()
                forceDir.x = 8
                self.__gameObject.getComponent("RigidBody").setForce(forceDir, isMassiveY=False)
                frozenLeft = False
            else:
                self.__gameObject.getComponent("RigidBody").setForce(pygame.Vector2(0, 0), isMassiveY=False)
                frozenRight = True
        if (self.inputHandler.isKeyPressed(pygame.K_a)):
            if (object1CanMove[0] != "LEFT" and not (frozenLeft)):
                forceDir: pygame.Vector2 = self.__gameObject.getComponent("RigidBody").getForceDirection()
                forceDir.x = -8
                self.__gameObject.getComponent("RigidBody").setForce(forceDir, isMassiveY=False)
                frozenRight = False
            else:
                self.__gameObject.getComponent("RigidBody").setForce(pygame.Vector2(0, 0), isMassiveY=False)
                frozenLeft = True
        if (self.inputHandler.isKeyPressed(pygame.K_w)):
            forceDir: pygame.Vector2 = self.__gameObject.getComponent("RigidBody").getForceDirection()
            forceDir.y = -8
            self.__gameObject.getComponent("RigidBody").setForce(forceDir, isMassiveY=False)

        # Top collision check
        if (colTop1):
            self.__gameObject.getComponent("RigidBody").setG(0)
            forceDir: pygame.Vector2 = self.__gameObject.getComponent("RigidBody").getForceDirection()
            if (forceDir.y > 0): forceDir.y = 0
            self.__gameObject.getComponent("RigidBody").setForce(forceDir, isMassiveY=False)
            self.__gameObject.getComponent("RigidBody").setIsGrounded(True)
        else:
            self.__gameObject.getComponent("RigidBody").setG(9.81)