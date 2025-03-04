#from GameObject import GameObject

class Component:
    def __init__(self, name, ):
        self.__name = name

    def getName(self):
        return self.__name

    def start(self, gameObject, gameObjects):
        # Called on the first frame
        pass

    def update(self, gameObject, gameObjects):
        # Called every frame
        pass