# PYGameEngine - Basic python game engine / physics engine based on pygame.
VERSION = "a0.5"

print(f"\033[92mPYGameEngine - Version {VERSION} - Developed by DcruBro @ \033[33mhttps://www.dcrubro.com/\033[00m")
print(f"\033[92mPYGameEngine\033[00m is licensed under GPLv3.")
print(f"\033[92mPYGameEngine\033[00m uses the following software: \033[92mpython (and its libraries), pygame (and its libraries), SDL (and its libraries), renderpyg (and its libraries) \033[31m- These are licensed under their own licenses.\033[00m\n")

print(f"\033[33mAnything from this point onward should be considered as logs.\033[00m")

import pygame
import cmath
from GameObject import Objects
from IO.ResourceLoader import ResourceLoader
from Components.BoxCollider import BoxCollider
from Components.RigidBody import RigidBody
from GameObjectHandler import GameObjectHandler
from Input.Input import Input
#from GUI.GUI import GUI
#from imgui.integrations.pygame import PygameRenderer
from Utils.Math import Math
from IO.SaveLoad import SaveLoad
from USERDIR.Scripts.PlayerMovement import PlayerMovement
from USERDIR.Scripts.Coin import Coin
from USERDIR.Scripts.GameManager import GameManager

FPS = 60

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# Init the image loader and load some images
resourceLoader = ResourceLoader()
resourceLoader.autoLoadResources("USERDIR/Textures/", ("coolasf", "coolasfnobg"))

# Init SaveLoad
saveLoad = SaveLoad()

# Init the Input Handler
inputHandler = Input(pygame)

# Create a GameManager object for handling game events.
gameManager = Objects.GameObject = Objects.GameObject("GameObject", pygame.Vector2(0, 0), 0, 0)
gMScript = GameManager(gameManager)
gameManager.addComponent(gMScript)

object: Objects.Sprite = Objects.Sprite("PlayerObj", resourceLoader, pygame.Vector2(200, 200), 0, pygame.Vector2(75, 75), "Bird1")
events = pygame.event.get()

gameObjectHandler = GameObjectHandler(pygame.Vector2(1280, 720))

pmScript = PlayerMovement(object, inputHandler)

object.addComponent(RigidBody("RigidBody", object, 720, 1, bounciness=0, friction=0.1, fpsConstant=FPS))
object.addComponent(BoxCollider("BoxCollider", object, 6, 3, pmScript.object1CollisionCallback))
object.addComponent(pmScript)

gameObjectHandler.registerGameObject(object)
#physics = Physics.Physics(720)
#physics.registerObject(object)

coinObject: Objects.Sprite = Objects.Sprite("Coin1", resourceLoader, pygame.Vector2(100, 500), 0, pygame.Vector2(50, 50), "coin1")
coinScript = Coin(coinObject)
coinObject2: Objects.Sprite = Objects.Sprite("Coin2", resourceLoader, pygame.Vector2(400, 500), 0, pygame.Vector2(50, 50), "coin1")
coinScript2 = Coin(coinObject2)
coinObject3: Objects.Sprite = Objects.Sprite("Coin3", resourceLoader, pygame.Vector2(200, 500), 0, pygame.Vector2(50, 50), "coin1")
coinScript3 = Coin(coinObject3)
coinObject4: Objects.Sprite = Objects.Sprite("Coin4", resourceLoader, pygame.Vector2(300, 500), 0, pygame.Vector2(50, 50), "coin1")
coinScript4 = Coin(coinObject4)

coinObject.addComponent(RigidBody("RigidBody", coinObject, 680, 1, bounciness=0, friction=1, fpsConstant=FPS, isSimulated=False))
coinObject.addComponent(BoxCollider("BoxCollider", coinObject, 10, 10, coinScript.collisionCallback))
coinObject.addComponent(coinScript)
coinObject2.addComponent(RigidBody("RigidBody", coinObject2, 680, 1, bounciness=0, friction=1, fpsConstant=FPS, isSimulated=False))
coinObject2.addComponent(BoxCollider("BoxCollider", coinObject2, 10, 10, coinScript2.collisionCallback))
coinObject2.addComponent(coinScript2)
"""
coinObject3.addComponent(RigidBody("RigidBody", coinObject3, 680, 1, bounciness=0, friction=1, fpsConstant=FPS, isSimulated=False))
coinObject3.addComponent(BoxCollider("BoxCollider", coinObject3, 10, 10, coinScript3.collisionCallback))
coinObject3.addComponent(coinScript3)
coinObject4.addComponent(RigidBody("RigidBody", coinObject4, 680, 1, bounciness=0, friction=1, fpsConstant=FPS, isSimulated=False))
coinObject4.addComponent(BoxCollider("BoxCollider", coinObject4, 10, 10, coinScript4.collisionCallback))
coinObject4.addComponent(coinObject4)
"""

gameObjectHandler.registerGameObject(coinObject)
gameObjectHandler.registerGameObject(coinObject2)
#gameObjectHandler.registerGameObject(coinObject3)
#gameObjectHandler.registerGameObject(coinObject4)

# Run the start logic on all GameObjects / Components
gameObjectHandler.start()
gameManager.getComponent("GameManager").start(gameObjectHandler)

#saveLoad.saveData("USERDIR/Saves/object.bin", saveLoad.serializeGameObject(object))

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT or inputHandler.isKeyPressed(pygame.K_ESCAPE):
            running = False
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # RENDER YOUR GAME HERE
    gameManager.getComponent("GameManager").update(pygame.Vector2(1280, 720), gameObjectHandler)
    gameObjectHandler.updateThenDraw(pygame, screen, object.getPosition(), 2)
    gameManager.getComponent("GameManager").lateUpdate(gameObjectHandler)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(FPS)  # limits FPS to 60

resourceLoader.freeAll()
pygame.quit()
