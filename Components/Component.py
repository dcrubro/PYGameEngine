"""
Component.py
A template for all other components to inherit from.
When added to a GameObject, the component name has to be unique, since the components are assigned to a dictionary, and can override others.
"""
class Component:
    def __init__(self, name):
        self.__name = name

    def getName(self):
        return self.__name

    def start(self, gameObject, gameObjects):
        # Called on the first frame
        pass

    def update(self, gameObject, gameObjects):
        # Called every frame
        pass