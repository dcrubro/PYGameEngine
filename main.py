# Example file showing a basic pygame "game loop"
import pygame
from pygame._sdl2.video import Renderer, Window

from GameObject import Objects
from Components.BoxCollider import BoxCollider
from Components.RigidBody import RigidBody
from GameObjectHandler import GameObjectHandler
from Input.Input import Input

print("PYGameEngine - Version a0.2\n")

FPS = 60

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

object: Objects.Rectangle = Objects.Rectangle("Rect1", pygame.Vector2(0, 500), 0, pygame.Vector2(100, 100), "blue")
object2: Objects.Rectangle = Objects.Rectangle("Rect2", pygame.Vector2(500, 500), 0, pygame.Vector2(100, 100), "red")
moveSpeedY: int = 4
moveSpeedX: int = 4
events = pygame.event.get()

# Some sample callbacks
global object1CanMove
global object2CanMove
object1CanMove = True
object2CanMove = True
def object1CollisionCallback(collidedWith):
    #collidedWith.getParentGameObject().getComponent("RigidBody").setForce(pygame.Vector2(0, 0))
    global object1CanMove
    object1CanMove = False

def object2CollisionCallback(collidedWith):
    #collidedWith.getParentGameObject().getComponent("RigidBody").setForce(pygame.Vector2(0, 0))
    global object2CanMove
    object2CanMove = False

gameObjectHandler = GameObjectHandler()
"""
object.addComponent(RigidBody("RigidBody", object, 720, 1, bounciness=0, friction=0.02, fpsConstant=FPS))
object.addComponent(BoxCollider("BoxCollider", object1CollisionCallback))

object2.addComponent(RigidBody("RigidBody2", object2, 720, 1, bounciness=0, friction=0.02, fpsConstant=FPS))
object2.addComponent(BoxCollider("BoxCollider2", object2CollisionCallback))

gameObjectHandler.registerGameObject(object)
gameObjectHandler.registerGameObject(object2)

#physics = Physics.Physics(720)
#physics.registerObject(object)
"""

object: Objects.Sprite = Objects.Sprite("CoolASF", pygame.Vector2(0, 500), 0, pygame.Vector2(100, 100), "USERDIR/Textures/coolasfnobg.png")
object.addComponent(RigidBody("RigidBody", object, 720, 1, bounciness=0, friction=0.02, fpsConstant=FPS))

gameObjectHandler.registerGameObject(object)

# Init the Renderer
#window = Window("Renderpyg Example", size=(1280, 720))
#renderer = Renderer(window, vsync=True)

# Init the Input Handler
inputHandler = Input(pygame)

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
    if (inputHandler.isKeyPressed(pygame.K_d)):
        forceDir: pygame.Vector2 = object.getComponent("RigidBody").getForceDirection()
        forceDir.x = 8
        object.getComponent("RigidBody").setForce(forceDir, isMassiveY = False)
    if (inputHandler.isKeyPressed(pygame.K_a)):
        forceDir: pygame.Vector2 = object.getComponent("RigidBody").getForceDirection()
        forceDir.x = -8
        object.getComponent("RigidBody").setForce(forceDir, isMassiveY = False)
    if (inputHandler.isKeyPressed(pygame.K_w) and object.getComponent("RigidBody").getIsGrounded()):
        forceDir: pygame.Vector2 = object.getComponent("RigidBody").getForceDirection()
        forceDir.y = -8
        object.getComponent("RigidBody").setForce(forceDir, isMassiveY = False)

    """
    if (inputHandler.isKeyPressed(pygame.K_l)):
        forceDir: pygame.Vector2 = object2.getComponent("RigidBody2").getForceDirection()
        forceDir.x = 8
        object2.getComponent("RigidBody2").setForce(forceDir, isMassiveY = False)
    if (inputHandler.isKeyPressed(pygame.K_j)):
        forceDir: pygame.Vector2 = object2.getComponent("RigidBody2").getForceDirection()
        forceDir.x = -8
        object2.getComponent("RigidBody2").setForce(forceDir, isMassiveY = False)
    if (inputHandler.isKeyPressed(pygame.K_i) and object2.getComponent("RigidBody2").getIsGrounded()):
        forceDir: pygame.Vector2 = object2.getComponent("RigidBody2").getForceDirection()
        forceDir.y = -8
        object2.getComponent("RigidBody2").setForce(forceDir, isMassiveY = False)


    if (not object1CanMove):
        object.getComponent("RigidBody").setForce(object.getComponent("RigidBody").getForceDirection() * -1)
    if (not object2CanMove):
        object2.getComponent("RigidBody2").setForce(object.getComponent("RigidBody2").getForceDirection() * -1)
    #object.setRotation(object.getRotation() + 1)
    #print(object.getPosition(), object.getRotation())

    #print(object.getComponent("RigidBody").getForceDirection())
    
    """

    gameObjectHandler.updateThenDraw(pygame, screen)

    #physics.update()

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(FPS)  # limits FPS to 60

pygame.quit()