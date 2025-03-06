import pygame
import GameObject.Objects
from GameObject import Objects
from Components.Component import Component

class BoxCollider(Component):
    def __init__(self, name, collisionCallback):
        super().__init__(name)
        self.parentGameObject = None
        self.sceneColliders = dict()
        self.size = None
        self.position = None
        self.rotation = None
        self.collisionCallback = collisionCallback
        self.previousPosition = None  # Store previous position (help with colliders)

    def start(self, gameObject: Objects.Rectangle, gameObjects: dict):
        # Start logic
        self.parentGameObject = gameObject

        self.size = gameObject.getSize()
        self.position = gameObject.getPosition()
        self.rotation = gameObject.getRotation()
        self.previousPosition = self.position  # Initialize previous position

        # Get all colliders in scene
        for k, v in gameObjects.items():
            for k2, v2 in v.getComponents().items():
                if isinstance(v2, BoxCollider):
                    self.sceneColliders[k] = v2

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

    def update(self, gameObject: Objects.Rectangle, gameObjects: dict):
        self.position = gameObject.getPosition()
        self.size = gameObject.getSize()

        for key, collider in self.sceneColliders.items():
            if collider == self:
                continue

            otherColliderPosition = collider.getPosition()
            otherColliderSize = collider.getSize()

            sideX = "NONE"
            sideY = "NONE"

            #if (gameObject.getName() == "Rect1"):
            #    print((self.position.x, self.position.y))

            if (abs(self.position.x - (otherColliderPosition.x + otherColliderSize.x)) < 1):
                sideX = "LEFT"
            elif (abs((self.position.x + self.size.x) - otherColliderPosition.x) < 1):
                sideX = "RIGHT"

            if (abs(self.position.y - (otherColliderPosition.y + otherColliderSize.y)) < 1):
                sideY = "TOP"
            elif (abs((self.position.y + self.size.y) - otherColliderPosition.y) < 1):
                sideY = "BOTTOM"

            self.collisionCallback(collider, (sideX, sideY))
