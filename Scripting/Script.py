# Script.py - A simple template for the scripting APi to interact with GameObjects

class Script:
    def __init__(self, name, gameObject):
        # These should not be settable from outside sources. They should also not be modified after creation.
        self.superSecretScriptIdentifierFlag = True
        self.__name = name # names should be unique
        self.__gameObject = gameObject

    def getName(self):
        return self.__name

    @property
    def gameObject(self):
        return self.__gameObject

    # These are implementations for the different methods that scripts can use. They are called, but the script doesn't have to implement them.
    def load(self):
        # Called on script load into memory
        pass

    def start(self):
        # Called on the first frame
        pass

    def update(self):
        # Called every frame
        pass
