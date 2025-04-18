import pygame
import Components.Component
from Enums.LogType import LogType
from IO.Time import Time
from Scripting.Script import Script
from IO.ResourceLoader import ResourceLoader
from Logging.Logger import Logger

class GameObject:
    def __init__(self, name, position, rotation, underCenterY, components = None):
        self.__position = position
        self.__rotation = rotation
        self.__name = name
        self.__underCenterY = underCenterY
        self.__tags = set()
        if components == None:
            components = dict()
        self.__components = components
        self.lastRenderTime = 0

    def moveBy(self, v: pygame.Vector2):
        self.__position += v

    def moveTo(self, v: pygame.Vector2):
        self.__position = v

    def getPosition(self):
        return self.__position

    def setPosition(self, v: pygame.Vector2):
        self.__position = v

    def getCoords(self):
        return (self.__position.x, self.__position.y)

    def getCoordsText(self):
        return f"X: {self.x} Y: {self.y}"

    def getRotation(self):
        return self.__rotation

    def setRotation(self, v: float):
        self.__rotation = v

    def getName(self):
        return self.__name

    def setName(self, v):
        self.__name = v

    def getUnderCenterY(self):
        return self.__underCenterY

    def setUnderCenterY(self, v):
        self.__underCenterY = v

    def getComponents(self):
        return self.__components

    def getComponent(self, componentName: str):
        return self.__components.get(f"{componentName}{self.getName()}")

    def setComponents(self, v: dict):
        self.__components = v

    def addComponent(self, v: Components.Component):
        self.__components[v.getName()] = v

    def addTag(self, v):
        self.__tags.add(v)

    def removeTag(self, v):
        self.__tags.remove(v)

    def hasTag(self, v):
        return v in self.__tags

    def getTags(self):
        return self.__tags

    def destroySelf(self, restartAllComponents):
        self.markedForDestruction = True # Destroys the object on the next update loop
        self.markedRestartAllComponents = restartAllComponents
        Logger.log(f"Destroyed {self.getName()}!", LogType.INFO, self)

    def start(self, gameObjects):
        # Runs on the first frame
        for k, v in self.__components.items():
            if isinstance(v, Script):
                if hasattr(v, "start"):
                    v.start()
                else:
                    continue
            else:
                v.start(self, gameObjects)

    def update(self, gameObjects):
        #Runs every frame
        if getattr(self, "markedForDestruction", False):
            return  # Already flagged for death

        for k, v in self.__components.items():
            if isinstance(v, Script):
                if hasattr(v, "update"):
                    v.update()
                else:
                    continue
            else:
                v.update(self, gameObjects)

    #Override
    def draw(self, pygameInstance, screenInstance, rotation):
        pass

class Rectangle(GameObject):
    def __init__(self, name, position, rotation, size, color):
        super().__init__(name, position, rotation, (size.y / 2))
        self.__size = size
        self.__rect = None
        self.color = color

    def changeColor(self, color):
        self.color = color

    def setSize(self, size: pygame.Vector2):
        self.__size = size

    def getSize(self):
        return self.__size

    def getRect(self):
        return self.__rect

    def getColor(self):
        return self.color

    def draw(self, pygameInstance, screenInstance, rotation):
        self.__surface = pygame.Surface(self.__size)
        self.__surface.set_colorkey((0, 0, 0))  # Make black transparent
        self.__surface.fill(self.color)

        # Get the current rect and store the center
        self.__rect = self.__surface.get_rect()
        self.__rect.center = self.getPosition()

        # Save the old center
        oldCenter = self.__rect.center

        # Rotate the surface around the center
        rotated_surface = pygame.transform.rotate(self.__surface, rotation)

        # Get the new rect for the rotated surface and keep the center
        self.__rect = rotated_surface.get_rect()
        self.__rect.center = oldCenter

        # Finally, blit the rotated surface to the screen at the new position
        screenInstance.blit(rotated_surface, self.__rect.topleft)
        #pygameInstance.draw.rect(screenInstance, "green", pygame.Rect(self.getPosition().x, self.getPosition().y, 1, 1))

class Circle(GameObject):
    def __init__(self, name, position, rotation, radius, color):
        super().__init__(name, position, rotation, radius)
        self.radius = radius
        self.color = color

    def changeColor(self, color):
        self.color = color

    def setRadius(self, r):
        self.radius = r

    def getRadius(self):
        return self.radius

    def getColor(self):
        return self.color

    def draw(self, pygameInstance, screenInstance, rotation):
        pygameInstance.draw.circle(screenInstance, self.color, pygame.Vector2(self.x, self.y), self.radius)

# For most uses, you should probably use this GameObject type
class Sprite(GameObject):
    def __init__(self, name, resLoaderPtr: ResourceLoader, position, rotation, size, texture):
        super().__init__(name, position, rotation, (size.y / 2))
        self.__resLoaderPtr = resLoaderPtr
        self.__size = size
        self.__texture = texture

    def setSize(self, size: pygame.Vector2):
        self.__size = size

    def getSize(self):
        return self.__size

    def getTexture(self):
        return self.__texture # Returns a path

    def setTexture(self, v: str):
        self.__texture = v

    # Override
    def draw(self, pygameInstance, screenInstance, rotation):
        # This is a modified example from the pygame wiki
        image = self.__resLoaderPtr.accessResource(self.__texture if self.__texture else "missing_texture")
        image = pygame.transform.scale(image, self.getSize())

        self.__surface = pygame.Surface(self.__size)
        self.__surface.set_colorkey((0, 0, 0))  # Make black transparent

        # Get the current rect and store the center
        self.__rect = image.get_rect()
        self.__rect.center = self.getPosition()

        # Save the old center
        oldCenter = self.__rect.center

        # Rotate the surface around the center
        rotated_surface = pygame.transform.rotate(image, rotation)

        # Get the new rect for the rotated surface and keep the center
        self.__rect = rotated_surface.get_rect()
        self.__rect.center = oldCenter

        # Finally, blit the rotated surface to the screen at the new position
        screenInstance.blit(rotated_surface, self.__rect.topleft)
        # pygameInstance.draw.rect(screenInstance, self.color, pygame.Rect(self.x, self.y, self.width, self.height))
