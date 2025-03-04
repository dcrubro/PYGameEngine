import pygame

class Input:
    def __init__(self, pygameInstance: pygame):
        self.__pygameInstance = pygameInstance

    def isKeyPressed(self, keyCode: pygame.constants) -> bool:
        pressedKeys = self.__pygameInstance.key.get_pressed()
        return pressedKeys[keyCode]

    def isMousePressed(self, keyCode: pygame.constants) -> bool:
        pressedKeys = self.__pygameInstance.mouse.get_pressed()
        return pressedKeys[keyCode]

    def getMousePosition(self) -> pygame.Vector2:
        pos = pygame.mouse.get_pos()
        return pygame.Vector2(pos[0], pos[1])