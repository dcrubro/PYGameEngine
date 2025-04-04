# PYGameEngine - Basic python game engine / physics engine based on pygame.
VERSION = "a0.5"

print(f"\033[92mPYGameEngine - Version {VERSION} - Developed by DcruBro @ \033[33mhttps://www.dcrubro.com/\033[00m")
print(f"\033[92mPYGameEngine\033[00m is licensed under GPLv3.")
print(f"\033[92mPYGameEngine\033[00m uses the following software: \033[92mpython (and its libraries), pygame (and its libraries), SDL (and its libraries), renderpyg (and its libraries) \033[31m- These are licensed under their own licenses.\033[00m\n")

print(f"\033[33mAnything from this point onward should be considered as logs.\033[00m")

import pygame
import cmath
from GameObject import Objects
from Renderer.ImageLoader import ImageLoader
from Components.BoxCollider import BoxCollider
from Components.RigidBody import RigidBody
from GameObjectHandler import GameObjectHandler
from Input.Input import Input
from GUI.GUI import GUI
from imgui.integrations.pygame import PygameRenderer
from Utils.Math import Math

from USERDIR.Scripts.PlayerMovement import PlayerMovement
from USERDIR.Scripts.Coin import Coin

FPS = 60

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# Init the image loader and load some images
imageLoader = ImageLoader()
imageLoader.autoLoadImages("USERDIR/Textures/")

# Init the Input Handler
inputHandler = Input(pygame)

object: Objects.Rectangle = Objects.Rectangle("Rect1", pygame.Vector2(800, 500), 0, pygame.Vector2(100, 100), "blue")
object2: Objects.Rectangle = Objects.Rectangle("Rect2", pygame.Vector2(500, 500), 0, pygame.Vector2(100, 100), "red")
moveSpeedY: int = 4
moveSpeedX: int = 4
events = pygame.event.get()

gameObjectHandler = GameObjectHandler(pygame.Vector2(1280, 720))

pmScript = PlayerMovement(object, inputHandler)

object.addComponent(RigidBody("RigidBody", object, 720, 1, bounciness=0, friction=0.02, fpsConstant=FPS))
object.addComponent(BoxCollider("BoxCollider", object, 6, 3, pmScript.object1CollisionCallback))
object.addComponent(pmScript)

gameObjectHandler.registerGameObject(object)
#physics = Physics.Physics(720)
#physics.registerObject(object)

coinObject: Objects.Sprite = Objects.Sprite("Coin1", imageLoader, pygame.Vector2(100, 500), 0, pygame.Vector2(75, 75), "coin1")
coinScript = Coin(coinObject)
coinObject2: Objects.Sprite = Objects.Sprite("Coin2", imageLoader, pygame.Vector2(200, 500), 0, pygame.Vector2(75, 75), "coin1")
coinScript2 = Coin(coinObject2)

coinObject.addComponent(RigidBody("RigidBody", coinObject, 700, 1, bounciness=0, friction=1, fpsConstant=FPS))
coinObject.addComponent(coinScript)
coinObject2.addComponent(RigidBody("RigidBody", coinObject2, 700, 1, bounciness=0, friction=1, fpsConstant=FPS))
coinObject2.addComponent(coinScript2)
gameObjectHandler.registerGameObject(coinObject)
gameObjectHandler.registerGameObject(coinObject2)
"""
"""

#gui = GUI()
#gui.start()

# Init the Renderer
#window = Window("Renderpyg Example", size=(1280, 720))
#renderer = Renderer(window, vsync=True)

# Run the start logic on all GameObjects / Components
gameObjectHandler.start()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT or inputHandler.isKeyPressed(pygame.K_ESCAPE):
            running = False
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # RENDER YOUR GAME HERE
    #object.getComponent("RigidBody").addForce(pygame.Vector2(0.05, 0), ForceType.INSTANT)

    # Basic Movement

    #object.setRotation(object.getRotation() + 1)
    #print(object.getPosition(), object.getRotation())

    #print(object.getComponent("RigidBody").getForceDirection())

    gameObjectHandler.updateThenDraw(pygame, screen, object.getPosition(), 2)

    #physics.update()

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(FPS)  # limits FPS to 60

pygame.quit()