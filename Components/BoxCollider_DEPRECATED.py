import pygame
import GameObject.Objects
from GameObject import Objects
from Components.Component import Component

# Deprecated - Do not use!
class BoxCollider(Component):
    # NOTE: This component is designed to work best with a RigidBody component
    # installed onto the GameObject as well. Please add a RigidBody component
    # alongside this component for proper function.

    def __init__(self, name, collisionCallback, noCollisionCallback):
        super().__init__(name)
        self.parent = None
        self.sceneColliders = dict()
        self.size = None
        self.position = None
        self.rotation = None
        self.collisionCallback = collisionCallback
        self.noCollisionCallback = noCollisionCallback
        self.previousPosition = None  # Store previous position (help with colliders)

    def start(self, gameObject, gameObjects):
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
        # Update Logic
        self.previousPosition = self.position  # Save old position before updating
        self.size = gameObject.getSize()
        self.position = gameObject.getPosition()
        self.rotation = gameObject.getRotation()

        for key, collider in self.sceneColliders.items():
            if collider == self:
                continue

            otherColliderPosition = collider.getPosition()
            otherColliderSize = collider.getSize()

            if ((self.position.x >= otherColliderPosition.x and self.position.x <= (otherColliderPosition.x + otherColliderSize.x)) and
                (self.position.y >= otherColliderPosition.y and self.position.y <= (otherColliderPosition.y + otherColliderSize.y))):

                # Determine collision side and the precise position of the collision
                collisionSide, collisionPoint = self.getCollisionDetails(collider)

                # Call the collision callback with the detected side and precise point
                self.collisionCallback(collider, collisionSide, collisionPoint)
            else:
                self.noCollisionCallback(collider) # Collision exit callback

    def getCollisionDetails(self, other):
        """
        Determines the side and exact point of collision relative to the top-left
        of the current collider.
        Returns: (collisionSide, (collisionX, collisionY))
        """
        otherPos = other.getPosition()
        otherSize = other.getSize()

        # Calculate overlapping distances
        leftOverlap = abs(self.position.x + self.size.x - otherPos.x)  # Right side hits left
        rightOverlap = abs(self.position.x - (otherPos.x + otherSize.x))  # Left side hits right
        topOverlap = abs(self.position.y + self.size.y - otherPos.y)  # Bottom hits top
        bottomOverlap = abs(self.position.y - (otherPos.y + otherSize.y))  # Top hits bottom

        # Determine the smallest overlap, which indicates the collision side
        minOverlap = min(leftOverlap, rightOverlap, topOverlap, bottomOverlap)

        collisionX = 0  # Default to top-left
        collisionY = 0

        if minOverlap == leftOverlap:
            collisionSide = "LEFT"
            collisionX = self.size.x  # Right-most part of this object
            collisionY = max(0, min(self.size.y, (self.position.y + self.size.y / 2) - otherPos.y))  # Centered Y
        elif minOverlap == rightOverlap:
            collisionSide = "RIGHT"
            collisionX = 0  # Left-most part of this object
            collisionY = max(0, min(self.size.y, (self.position.y + self.size.y / 2) - otherPos.y))  # Centered Y
        elif minOverlap == topOverlap:
            collisionSide = "TOP"
            collisionX = max(0, min(self.size.x, (self.position.x + self.size.x / 2) - otherPos.x))  # Centered X
            collisionY = self.size.y  # Bottom-most part
        elif minOverlap == bottomOverlap:
            collisionSide = "BOTTOM"
            collisionX = max(0, min(self.size.x, (self.position.x + self.size.x / 2) - otherPos.x))  # Centered X
            collisionY = 0  # Top-most part
        else:
            collisionSide = "UNKNOWN"
            collisionX, collisionY = -1, -1  # Unknown collision point

        return collisionSide, (collisionX, collisionY)

