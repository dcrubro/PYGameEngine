# PYGameEngine - Basic python game engine / physics engine based on pygame.
from USERDIR.Scripts.PlayerMovement import PlayerMovement

VERSION = "a0.3"

print(f"\033[92mPYGameEngine - Version {VERSION} - Developed by DcruBro @ \033[33mhttps://www.dcrubro.com/\033[00m")
print(f"\033[92mPYGameEngine\033[00m is licensed under GPLv3.")
print(f"\033[92mPYGameEngine\033[00m uses the following software: \033[92mpython (and its libraries), pygame (and its libraries), SDL (and its libraries), renderpyg (and its libraries) \033[31m- These are licensed under their own licenses.\033[00m\n")

print(f"\033[33mAnything from this point onward should be considered as logs.\033[00m")

import pygame
from pygame._sdl2.video import Renderer, Window
import cmath
from GameObject import Objects
from Components.BoxCollider import BoxCollider
from Components.RigidBody import RigidBody
from GameObjectHandler import GameObjectHandler
from Input.Input import Input
from Utils.Math import Math

FPS = 60

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# Init the Input Handler
inputHandler = Input(pygame)

object: Objects.Rectangle = Objects.Rectangle("Rect1", pygame.Vector2(800, 500), 0, pygame.Vector2(100, 100), "blue")
object2: Objects.Rectangle = Objects.Rectangle("Rect2", pygame.Vector2(500, 500), 0, pygame.Vector2(100, 100), "red")
moveSpeedY: int = 4
moveSpeedX: int = 4
events = pygame.event.get()

# Some sample callbacks
global object1CanMove
global object2CanMove
object1CanMove = ""
object2CanMove = ""
colTop1 = False
def object1CollisionCallback(collidedWith, side):
    #if (side[0] != "NONE"): print(side[0])
    global object1CanMove
    object1CanMove = side
    global colTop1
    colTop1 = side[1] == "BOTTOM"

def object2CollisionCallback(collidedWith, side):
    global object2CanMove
    object2CanMove = side

gameObjectHandler = GameObjectHandler()

pmScript = PlayerMovement(object, inputHandler)

object.addComponent(RigidBody("RigidBody", object, 720, 1.2, bounciness=0, friction=0.02, fpsConstant=FPS))
object.addComponent(BoxCollider("BoxCollider", 6, 3, pmScript.object1CollisionCallback))
object.addComponent(pmScript)

object2.addComponent(RigidBody("RigidBody2", object2, 720, 1, bounciness=0, friction=0.02, fpsConstant=FPS))
object2.addComponent(BoxCollider("BoxCollider2", 4, 2, object2CollisionCallback))

gameObjectHandler.registerGameObject(object)
gameObjectHandler.registerGameObject(object2)

#physics = Physics.Physics(720)
#physics.registerObject(object)

"""
object: Objects.Sprite = Objects.Sprite("CoolASF", pygame.Vector2(0, 500), 0, pygame.Vector2(100, 100), "USERDIR/Textures/coolasfnobg.png")
object.addComponent(RigidBody("RigidBody", object, 720, 1, bounciness=0, friction=0.02, fpsConstant=FPS))
"""

gameObjectHandler.registerGameObject(object)

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

    if (inputHandler.isKeyPressed(pygame.K_l)):
        if (object2CanMove[0] != "RIGHT"):
            forceDir: pygame.Vector2 = object2.getComponent("RigidBody2").getForceDirection()
            forceDir.x = 8
            object2.getComponent("RigidBody2").setForce(forceDir, isMassiveY = False)
    if (inputHandler.isKeyPressed(pygame.K_j)):
        if (object2CanMove[0] != "LEFT"):
            forceDir: pygame.Vector2 = object2.getComponent("RigidBody2").getForceDirection()
            forceDir.x = -8
            object2.getComponent("RigidBody2").setForce(forceDir, isMassiveY = False)
    if (inputHandler.isKeyPressed(pygame.K_i) and object2.getComponent("RigidBody2").getIsGrounded()):
        forceDir: pygame.Vector2 = object2.getComponent("RigidBody2").getForceDirection()
        forceDir.y = -8
        object2.getComponent("RigidBody2").setForce(forceDir, isMassiveY = False)

    #object.setRotation(object.getRotation() + 1)
    #print(object.getPosition(), object.getRotation())

    #print(object.getComponent("RigidBody").getForceDirection())

    gameObjectHandler.updateThenDraw(pygame, screen)

    #physics.update()

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(FPS)  # limits FPS to 60

pygame.quit()