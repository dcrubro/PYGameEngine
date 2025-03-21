import pygame
import Components.Component
from Scripting.Script import Script

class GameObject:
    def __init__(self, name, position, rotation, underCenterY, components = dict()):
        self.__position = position
        self.__rotation = rotation
        self.name = name
        self.__underCenterY = underCenterY
        self.__components = components

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
        return self.name

    def setName(self, v):
        self.name = v

    def getUnderCenterY(self):
        return self.__underCenterY

    def setUnderCenterY(self, v):
        self.__underCenterY = v

    def getComponents(self):
        return self.__components

    def getComponent(self, componentName: str):
        return self.__components.get(componentName)

    def setComponents(self, v: dict):
        self.__components = v

    def addComponent(self, v: Components.Component):
        self.__components[v.getName()] = v

    def start(self, gameObjects):
        # Runs on the first frame
        for k, v in self.__components.items():
            if isinstance(v, Script):
                try:
                    v.start()
                except AttributeError:
                    continue
            else:
                v.start(self, gameObjects)

    def update(self, gameObjects):
        #Runs every frame
        for k, v in self.__components.items():
            if isinstance(v, Script):
                try:
                    v.update()
                except AttributeError:
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
        pygameInstance.draw.rect(screenInstance, "green", pygame.Rect(self.getPosition().x, self.getPosition().y, 1, 1))

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

    def draw(self, pygameInstance, screenInstance, rotation):
        pygameInstance.draw.circle(screenInstance, self.color, pygame.Vector2(self.x, self.y), self.radius)

class Sprite(GameObject):
    def __init__(self, name, position, rotation, size, texture):
        super().__init__(name, position, rotation, (size.y / 2))
        self.__size = size
        self.__texture = texture

    #def changeColor(self, color):
    #    self.color = color

    def setSize(self, size: pygame.Vector2):
        self.__size = size

    def getSize(self):
        return self.__size

    # Override
    def draw(self, pygameInstance, screenInstance, rotation):
        image = pygame.image.load(self.__texture)
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
