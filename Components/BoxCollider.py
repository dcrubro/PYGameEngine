import pygame

import GameObject.Objects
from GameObject import Objects
from Components.Component import Component

class BoxCollider(Component):
    # NOTE: This component is designed to work best with a RigidBody component
    # installed onto the GameObject as well. Please add a RigidBody component
    # alongside this component for proper function.
    def __init__(self, name, collisionCallback):
        super().__init__(name)
        self.__parent = None
        self.__sceneColliders = dict()
        self.__size = None
        self.__position = None
        self.__rotation = None
        self.__collisionCallback = collisionCallback

    def start(self, gameObject, gameObjects):
        # Start logic
        self.__parentGameObject = gameObject

        self.__size = gameObject.getSize()
        self.__position = gameObject.getPosition()
        self.__rotation = gameObject.getRotation()

        # Get all colliders
        for k, v in gameObjects.items():
            for k2, v2 in v.getComponents().items():
                if type(v2) == BoxCollider:
                    self.__sceneColliders[k] = v2

    def getSceneColliders(self):
        return self.__sceneColliders

    def setSceneColliders(self, v: dict):
        self.__sceneColliders = v

    def getSize(self):
        return self.__size

    def setSize(self, v: pygame.Vector2):
        self.__size = v

    def getPosition(self):
        return self.__position

    def setPosition(self, v: pygame.Vector2):
        self.__position = v

    def getRotation(self):
        return self.__rotation

    def setRotation(self, v: pygame.Vector2):
        self.__rotation = v

    def getParentGameObject(self):
        return self.__parentGameObject

    def setParentGameObject(self, v: GameObject.Objects.GameObject):
        self.__parentGameObject = v

    def update(self, gameObject: Objects.Rectangle, gameObjects: dict):
        # Update Logic
        self.__size = gameObject.getSize()
        self.__position = gameObject.getPosition()
        self.__rotation = gameObject.getRotation()

        #print(gameObject, self.__position)

        # Collision Check (checking contact with another BoxCollider)
        for k, v in self.__sceneColliders.items():
            if (v == self):
                continue

            otherColliderPosition = v.getPosition()
            otherColliderSize = v.getSize()

            if ((self.__position.x >= otherColliderPosition.x and self.__position.x <= (otherColliderPosition.x + otherColliderSize.x)) and (self.__position.y >= otherColliderPosition.y and self.__position.y <= (otherColliderPosition.y + otherColliderSize.y))):
                # Collision detected, try calling the self's collision callback
                self.__collisionCallback(v)

    def onCollision(self):
        pass
