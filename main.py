# PYGameEngine - Basic python game engine / physics engine based on pygame.
from Enums.LogType import LogType
from GameObject.Objects import GameObject
from Logging.Logger import Logger
from USERDIR.Scripts.Doodle.GameManagerDoodle import GameManagerDoodle
from USERDIR.Scripts.Doodle.PlatSpawner import PlatSpawner
from USERDIR.Scripts.Doodle.PlayerMovementDoodle import PlayerMovementDoodle
from USERDIR.Scripts.PipeSpawner import PipeSpawner

VERSION = "a0.6"

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
from Sound.Sound import Sound
#from GUI.GUI import GUI
#from imgui.integrations.pygame import PygameRenderer
from Utils.Math import Math
from IO.SaveLoad import SaveLoad
from USERDIR.Scripts.PlayerMovement import PlayerMovement
from USERDIR.Scripts.Coin import Coin
from USERDIR.Scripts.GameManager import GameManager

FPS = 60
DEMO = "DOODLE" # FLAPPY or DOODLE

# pygame setup
pygame.init()
screenFlags = pygame.DOUBLEBUF
screenBpp = 16
screen = pygame.display.set_mode((1280, 720), screenFlags, screenBpp)
clock = pygame.time.Clock()
pygame.font.init()
running = True

# Init the image loader and load some images
resourceLoader = ResourceLoader()
resourceLoader.autoLoadResources("USERDIR/", ("coolasf", "coolasfnobg")) # Pre load all valid "resource" files in the USERDIR directory.

# Init Sound
sound = Sound(resourceLoader)

# Init SaveLoad
saveLoad = SaveLoad()

# Init the Input Handler
inputHandler = Input(pygame)

if DEMO == "FLAPPY":
    # Create a GameManager object for handling game events.
    gameManager = Objects.GameObject = Objects.GameObject("GameManager", pygame.Vector2(0, 0), 0, 0)
    gMScript = GameManager(gameManager, resourceLoader, screen)
    gameManager.addComponent(gMScript)

    # Simple background
    bgObj = Objects.Sprite("BackgroundObj", resourceLoader, pygame.Vector2(640, 360), 0, pygame.Vector2(1280, 720), "bgUp")
    bgObj.addTag("BG")

    object: Objects.Sprite = Objects.Sprite("PlayerObj", resourceLoader, pygame.Vector2(200, 200), 0, pygame.Vector2(75, 75), "Bird1")
    events = pygame.event.get()

    gameObjectHandler = GameObjectHandler(pygame.Vector2(1280, 720))
    gameObjectHandler.registerGameObject(bgObj)

    pmScript = PlayerMovement(object, inputHandler, sound)

    object.addComponent(RigidBody("RigidBody", object, 720, 1, bounciness=0, friction=0.1, fpsConstant=FPS))
    object.addComponent(BoxCollider("BoxCollider", object, 1, 1, pmScript.object1CollisionCallback))
    object.addComponent(pmScript)

    gameObjectHandler.registerGameObject(object)
    #physics = Physics.Physics(720)
    #physics.registerObject(object)

    pipeSpawner: Objects.GameObject = GameObject("PipeSpawner", pygame.Vector2(0, 0), 0, 0)
    pSScript = PipeSpawner(pipeSpawner, gameObjectHandler, resourceLoader, sound)
    pipeSpawner.addComponent(pSScript)

    gameObjectHandler.registerGameObject(pipeSpawner)

    #pipe: Objects.Sprite = Objects.Sprite("Pipe", resourceLoader, pygame.Vector2(400, 500), 0, pygame.Vector2(125, 125), "PipeEnd")
    #gameObjectHandler.registerGameObject(pipe)

    # Run the start logic on all GameObjects / Components
    gameObjectHandler.start()
    gameManager.getComponent("GameManager").start(gameObjectHandler)

    #saveLoad.saveData("USERDIR/Saves/object.bin", saveLoad.serializeGameObject(object))

    while running:
        pygame.display.set_caption(f'PYGameEngine - FPS: {round(clock.get_fps(), 2)}')

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

elif DEMO == "DOODLE":
    # Create a GameManager object for handling game events.
    gameManager = Objects.GameObject = Objects.GameObject("GameManager", pygame.Vector2(0, 0), 0, 0)
    gMScript = GameManagerDoodle(gameManager, resourceLoader, screen)
    gameManager.addComponent(gMScript)

    # Simple background
    #bgObj = Objects.Sprite("BackgroundObj", resourceLoader, pygame.Vector2(640, 360), 0, pygame.Vector2(1280, 720),
    #                       "bgUp")
    #bgObj.addTag("BG")

    object: Objects.Sprite = Objects.Sprite("PlayerObj", resourceLoader, pygame.Vector2(200, 200), 0,
                                            pygame.Vector2(75, 75), "DoodleChar")

    platformTest: Objects.Rectangle = Objects.Rectangle("PlatformTest", pygame.Vector2(200, 200), 0,
                                            pygame.Vector2(75, 10), "red")
    platformTest.addComponent(RigidBody("RigidBody", platformTest, 720, 1, bounciness=0, friction=0.1, fpsConstant=FPS, isSimulated=False))
    platformTest.addComponent(BoxCollider("BoxCollider", platformTest, 1, 21, None))

    events = pygame.event.get()

    gameObjectHandler = GameObjectHandler(pygame.Vector2(1280, 720))
    #gameObjectHandler.registerGameObject(bgObj)

    pmScript = PlayerMovementDoodle(object, inputHandler, sound)

    object.addComponent(RigidBody("RigidBody", object, 720, 1, bounciness=0, friction=0.1, fpsConstant=FPS, doAirResistance=True))
    object.addComponent(BoxCollider("BoxCollider", object, 1, 6, pmScript.object1CollisionCallback))
    object.addComponent(pmScript)

    gameObjectHandler.registerGameObject(object)
    gameObjectHandler.registerGameObject(platformTest)
    # physics = Physics.Physics(720)
    # physics.registerObject(object)

    platSpawner: Objects.GameObject = GameObject("PlatSpawner", pygame.Vector2(0, 0), 0, 0)
    pSScript = PlatSpawner(platSpawner, gameObjectHandler, resourceLoader, sound)
    platSpawner.addComponent(pSScript)

    gameObjectHandler.registerGameObject(platSpawner)

    # pipe: Objects.Sprite = Objects.Sprite("Pipe", resourceLoader, pygame.Vector2(400, 500), 0, pygame.Vector2(125, 125), "PipeEnd")
    # gameObjectHandler.registerGameObject(pipe)

    # Run the start logic on all GameObjects / Components
    gameObjectHandler.start()
    gameManager.getComponent("GameManager").start(gameObjectHandler)

    while running:
        pygame.display.set_caption(f'PYGameEngine - FPS: {round(clock.get_fps(), 2)}')

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

else:
    Logger.log("Unknown demo name. (PYGE_LOAD_ERROR, PYGE_FATAL_ERROR)", LogType.ERROR, "Main")

Logger.log("Killing PYGE...", LogType.IMPORTANT, "Main")
resourceLoader.freeAll()
pygame.quit()
Logger.log("Exited.", LogType.IMPORTANT, "Main")