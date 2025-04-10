import pygame
import GameObject.Objects
from GameObject import Objects
from Components.Component import Component

"""
BoxCollider needs a RigidBody on the same object to work correctly.
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

        #print(gameObjects.items())
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
        self.position = gameObject.getPosition()
        self.size = gameObject.getSize()
        self.velocity = gameObject.getComponent("RigidBody").getForceDirection()
        self.mass = gameObject.getComponent("RigidBody").getMass()

        if len(gameObjects) != self.cycleObjects:
            self.start(self.getParentGameObject(), gameObjects)

        for key, collider in self.sceneColliders.items():
            if collider == self:
                continue

            otherColliderPosition = collider.getPosition()
            otherColliderSize = collider.getSize()

            sideX = "NONE"
            sideY = "NONE"

            if ((self.position.y < (otherColliderPosition.y + (otherColliderSize.y))) and (self.position.y > (otherColliderPosition.y - (otherColliderSize.y)))):
                if (abs(self.position.x - (otherColliderPosition.x - otherColliderSize.x)) < self.__xTolerance - self.velocity.x * self.mass):
                    sideX = "LEFT"
                if (abs(self.position.x - (otherColliderPosition.x + otherColliderSize.x)) < self.__xTolerance + self.velocity.x * self.mass):
                    sideX = "RIGHT"

            if ((self.position.x < (otherColliderPosition.x + (otherColliderSize.x))) and (self.position.x > (otherColliderPosition.x - (otherColliderSize.x)))):
                if (abs(self.position.y - (otherColliderPosition.y - otherColliderSize.y)) < self.__yTolerance - self.velocity.y * self.mass):
                    sideY = "TOP"
                if (abs(self.position.y - (otherColliderPosition.y + otherColliderSize.y)) < self.__yTolerance + self.velocity.y * self.mass):
                    sideY = "BOTTOM"

            self.collisionCallback(collider, (sideX, sideY))
