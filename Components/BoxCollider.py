import pygame
import GameObject.Objects
from GameObject import Objects
from Components.Component import Component
from Logging.Logger import Logger
from Enums.LogType import LogType

"""
BoxCollider needs a RigidBody on the same object to work correctly.
Also, calling it a "collider" is a little bit misleading. It's actually just a trigger box, and you have to handle
the actions that take place after a "collision" is detected.
"""
class BoxCollider(Component):
    def __init__(self, name, gameObject, xTolerance, yTolerance, collisionCallback):
        super().__init__(f"{name}{gameObject.getName()}")
        self.parentGameObject = gameObject
        self.sceneColliders = dict()
        self.size = None
        self.position = None
        self.rotation = None
        self.collisionCallback = collisionCallback
        self.previousPosition = None  # Store previous position (help with colliders)
        self.__xTolerance = xTolerance
        self.__yTolerance = yTolerance
        self.velocity = None

        # Temporary stuff
        self.cycleObjects = 0

    def start(self, gameObject: Objects.Rectangle, gameObjects: dict):
        # Start logic
        self.sceneColliders = dict() # Reset the colliders

        self.size = gameObject.getSize()
        self.velocity = gameObject.getComponent("RigidBody").getForceDirection()
        self.position = gameObject.getPosition()
        self.rotation = gameObject.getRotation()
        self.previousPosition = self.position  # Initialize previous position

        # Get all colliders in scene
        for k, v in gameObjects.items():
            for k2, v2 in v.getComponents().items():
                if isinstance(v2, BoxCollider):
                    self.sceneColliders[k] = v2

        self.cycleObjects = len(gameObjects)

    def getSceneColliders(self):
        return self.sceneColliders

    def setSceneColliders(self, colliders: dict):
        self.sceneColliders = colliders

    def getSize(self):
        return self.size

    def setSize(self, size: pygame.Vector2):
        self.size = size

    def getPosition(self):
        return self.position

    def setPosition(self, position: pygame.Vector2):
        self.position = position

    def getRotation(self):
        return self.rotation

    def setRotation(self, rotation: pygame.Vector2):
        self.rotation = rotation

    def getParentGameObject(self):
        return self.parentGameObject

    def setParentGameObject(self, parent: GameObject.Objects.GameObject):
        self.parentGameObject = parent

    def getPreviousPosition(self):
        return self.previousPosition

    def getXTolerance(self):
        return self.__xTolerance

    def getYTolerance(self):
        return self.__yTolerance

    def update(self, gameObject: Objects.Rectangle, gameObjects: dict):
        # This code was generated, courtesy of ChatGPT :) (Modified by me)
        self.position = gameObject.getPosition()
        self.size = gameObject.getSize()
        self.velocity = gameObject.getComponent("RigidBody").getForceDirection()
        self.mass = gameObject.getComponent("RigidBody").getMass()

        if len(gameObjects) != self.cycleObjects:
            self.start(self.getParentGameObject(), gameObjects)

        # Calculate this object's bounding box
        selfLeft = self.position.x - self.size.x / 2
        selfRight = self.position.x + self.size.x / 2
        selfTop = self.position.y - self.size.y / 2
        selfBottom = self.position.y + self.size.y / 2

        for key, collider in self.sceneColliders.items():
            if not(collider): continue # None check

            if collider == self:
                continue

            otherPosition = collider.getPosition()
            otherSize = collider.getSize()

            if not(otherPosition) or not(otherSize):
                Logger.log("Something went seriously wrong, continuing to next collider! (PYGE_BOXCOLLIDER_ERROR, PYGE_NON_FATAL_ERROR)", LogType.ERROR, self)
                Logger.log(f"Error with BoxCollider {collider}", LogType.DESCRIPTION, self)
                continue

            otherLeft = otherPosition.x - otherSize.x / 2
            otherRight = otherPosition.x + otherSize.x / 2
            otherTop = otherPosition.y - otherSize.y / 2
            otherBottom = otherPosition.y + otherSize.y / 2

            # Apply small tolerances
            expandedXTolerance = self.__xTolerance
            expandedYTolerance = self.__yTolerance

            if (selfRight > otherLeft - expandedXTolerance and
                    selfLeft < otherRight + expandedXTolerance and
                    selfBottom > otherTop - expandedYTolerance and
                    selfTop < otherBottom + expandedYTolerance):

                # Calculate the side of collision (simple version)
                dx = (otherPosition.x - self.position.x)
                dy = (otherPosition.y - self.position.y)

                sideX = "NONE"
                sideY = "NONE"

                if abs(dx) > abs(dy):
                    if dx > 0:
                        sideX = "LEFT"
                    else:
                        sideX = "RIGHT"
                else:
                    if dy > 0:
                        sideY = "TOP"
                    else:
                        sideY = "BOTTOM"

                if self.collisionCallback:
                    self.collisionCallback(collider, (sideX, sideY))
