import pygame

from Components.Component import Component
from Enums.ForceType import ForceType
from Enums.LogType import LogType
from GameObject.Objects import GameObject
from Logging.Logger import Logger

class RigidBody(Component):
    def __init__(self, name, gameObject: GameObject, groundY, mass, isSimulated = True, g = 9.81, bounciness = 0, friction = 0.1, fpsConstant = 60):
        super().__init__(f"{name}{gameObject.getName()}")
        self.__isSimulated = isSimulated # If True, physics will be calculated, otherwise, the object will be static
        self.__gravitationalVelocity: float = 0
        self.__rotationalForce: pygame.Vector2 = pygame.Vector2(0, 0)
        self.__forceDirection: pygame.Vector2 = pygame.Vector2(0, 0)

        self.__mass = mass
        self.__g = g
        self.__fpsConstant = fpsConstant
        self.__groundY = groundY
        self.__gameObject = gameObject
        self.__bounciness = bounciness
        self.__friction = friction

        self.__frozenAxis = (False, False)

        self.__isGrounded = False

    def getGravitationalVelocity(self):
        return self.__gravitationalVelocity

    def setGravitationalVelocity(self, v: float):
        self.__gravitationalVelocity = v

    def getIsSimulated(self):
        return self.__isSimulated

    def setIsSimulated(self, v: bool):
        self.__isSimulated = v

    def getForceDirection(self):
        return self.__forceDirection

    def setForceDirection(self, v: pygame.Vector2):
        self.__forceDirection = v

    def getRotationalForce(self):
        return self.__rotationalForce

    def setRotationalForce(self, v: pygame.Vector2):
        self.__rotationalForce = v

    def getG(self):
        return self.__g

    def setG(self, v: float):
        self.__g = v

    def getFPSConstant(self):
        return self.__fpsConstant

    def setFPSConstant(self, v: int):
        self.__fpsConstant = v

    def getGroundY(self):
        return self.__groundY

    def setGroundY(self, v: float):
        self.__groundY = v

    def getIsGrounded(self):
        return self.__isGrounded

    def setIsGrounded(self, v: bool):
        self.__isGrounded = v

    def getMass(self):
        return self.__mass

    def setMass(self, v: float):
        self.__mass = v

    def getBounciness(self):
        return self.__bounciness

    def setBounciness(self, v: float):
        self.__bounciness = v

    def getFriction(self):
        return self.__friction

    def setFriction(self, v: float):
        self.__friction = v

    def getFrozenAxis(self):
        return self.__frozenAxis

    def setFrozenAxis(self, v: tuple):
        self.__frozenAxis = v

    # GENERAL FUNCTIONS
    def addForce(self, forceDirection: pygame.Vector2, forceType: ForceType, isMassiveX = True, isMassiveY = True):
        if (self.__mass == 0):
            # Lightspeed
            forceDirection = pygame.Vector2(299792458, 299792458)
            self.__forceDirection = forceDirection
            return

        # Add force and account for mass (Newton's 2nd Law of Motion)
        forceDirection = pygame.Vector2(forceDirection.x / self.__mass if isMassiveX else forceDirection.x, forceDirection.y / self.__mass if isMassiveY else forceDirection.y)

        if (forceType == ForceType.INSTANT):
            self.__forceDirection += forceDirection
        if (forceType == ForceType.ACCELERATING):
            pass
        if (forceType == ForceType.NONE):
            self.__forceDirection = pygame.Vector2(0, 0)
            return

    def setForce(self, forceDirection: pygame.Vector2, isMassiveX = True, isMassiveY = True):
        # Set force and account for mass (Newton's 2nd Law of Motion)
        if (self.__mass == 0):
            # Lightspeed
            forceDirection = pygame.Vector2(299792458, 299792458)
            self.__forceDirection = forceDirection
            return

        if (self.__mass < 0):
            Logger.log("Set mass is negative. The physics will not work correctly!", LogType.WARNING, self.__gameObject)

        forceDirection = pygame.Vector2(forceDirection.x / self.__mass if isMassiveX else forceDirection.x, forceDirection.y / self.__mass if isMassiveY else forceDirection.y)
        self.__forceDirection = forceDirection

    def update(self, gameObject: GameObject, gameObjects):
        #Update Logic
        if (self.__isSimulated):
            addedGVelocity: float = self.__g / self.__fpsConstant
            if ((self.__gameObject.getPosition().y + self.__gameObject.getUnderCenterY() >= self.__groundY)):
                # Ground check
                self.__isGrounded = True

                if (self.__forceDirection.y > 0):
                    self.__forceDirection.y *= -self.__bounciness
                # Apply friction
                self.__forceDirection.x *= (1 - self.__friction)
                #if (self.__forceDirection.y <= 0.005): self.__forceDirection.y = 0
            else:
                self.__isGrounded = False
                # set vg
                self.__forceDirection.y += addedGVelocity

            # Account for frozen axis'
            self.__forceDirection.x = 0 if self.__frozenAxis[0] else self.__forceDirection.x
            self.__forceDirection.y = 0 if self.__frozenAxis[1] else self.__forceDirection.y

            # Apply forces
            self.__gameObject.moveBy(self.__forceDirection)