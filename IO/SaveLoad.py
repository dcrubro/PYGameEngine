import json
import zlib
import base64

from GameObject.Objects import *
from Components.RigidBody import RigidBody
from Components.BoxCollider import BoxCollider
from Logging.Logger import Logger
from Enums.LogType import LogType

class SaveLoad:
    def __init__(self):
        pass

    @staticmethod
    def serializeGameObject(obj: GameObject):
        data = {}

        # These exist no matter what
        data["name"] = obj.getName()
        data["position"] = (obj.getPosition().x, obj.getPosition().y)
        data["rotation"] = obj.getRotation()
        data["underCenterY"] = obj.getUnderCenterY()

        components = obj.getComponents()
        print(components)

        # Handle specific types
        if isinstance(obj, Rectangle):
            data["specificType"] = "Rectangle"
            data["size"] = (obj.getSize().x, obj.getSize().y)
            data["color"] = obj.getColor()
        elif isinstance(obj, Circle):
            data["specificType"] = "Circle"
            data["radius"] = obj.getRadius()
            data["color"] = obj.getColor()
        elif isinstance(obj, Sprite):
            data["specificType"] = "Sprite"
            data["size"] = (obj.getSize().x, obj.getSize().y)
            # The ResourceLoader pointer and the texture should be redefined on load.
        else:
            data["specificType"] = "GameObject"

        # Handle the components
        componentsJ = []
        for k, v in components.items():
            dC = {}
            if isinstance(v, RigidBody):
                dC["name"] = v.getName()
                dC["isSimulated"] = v.getIsSimulated()
                dC["gravitationalVelocity"] = v.getGravitationalVelocity()
                dC["rotationalForce"] = (v.getRotationalForce().x, v.getRotationalForce().y)
                dC["forceDirection"] = (v.getForceDirection().x, v.getForceDirection().y)
                dC["mass"] = v.getMass()
                dC["g"] = v.getG()
                dC["fpsConstant"] = v.getFPSConstant()
                dC["groundY"] = v.getGroundY()
                dC["bounciness"] = v.getBounciness()
                dC["friction"] = v.getFriction()
                dC["isGrounded"] = v.getIsGrounded()
            if isinstance(v, BoxCollider):
                dC["name"] = v.getName()
                dC["size"] = (v.getSize().x, v.getSize().y)
                dC["position"] = (v.getPosition().x, v.getPosition().y)
                dC["rotation"] = v.getRotation()
                dC["previousPosition"] = (v.getPreviousPosition().x, v.getPreviousPosition().y)
                dC["xTolerance"] = v.getXTolerance()
                dC["yTolerance"] = v.getYTolerance()
                dC["velocity"] = (v.velocity.x, v.velocity.y)

            componentsJ.append(dC)

        data["components"] = componentsJ

        print(data)

        return data

    @staticmethod
    def deserializeGameObject(data):
        # Normally, you'd pass a pointer to the object you want to save this to, but this is Python and we sadly can't do that :(
        object = None
        match data["specificType"]:
            case "GameObject":
                object = GameObject(data["name"],
                                    pygame.Vector2(data["position"][0], data["position"][1]),
                                    data["rotation"],
                                    data["underCenterY"])
            case "Rectangle":
                object = Rectangle(data["name"],
                            pygame.Vector2(data["position"][0], data["position"][1]),
                            data["rotation"],
                            data["underCenterY"],
                            pygame.Vector2(data["size"][0], data["size"][1]),
                            data["color"])
            case "Circle":
                object = Circle(data["name"],
                                   pygame.Vector2(data["position"][0], data["position"][1]),
                                   data["rotation"],
                                   data["underCenterY"],
                                   data["radius"],
                                   data["color"])
            case "Sprite":
                object = Sprite(data["name"],
                                None,
                                pygame.Vector2(data["position"][0], data["position"][1]),
                                data["rotation"],
                                data["underCenterY"],
                                pygame.Vector2(data["size"][0], data["size"][1]),
                                None)
        pass

    @staticmethod
    def saveValue(name, value):
        data = SaveLoad.loadData("USERDIR/Saves/valstore.bin")
        if data is None:
            data = dict()

        data[name] = value
        SaveLoad.saveData("USERDIR/Saves/valstore.bin", data)
        return True

    @staticmethod
    def getValue(name):
        data = SaveLoad.loadData("USERDIR/Saves/valstore.bin")
        if data:
            return data.get(name)
        return None

    @staticmethod
    def saveData(path, data):
        with open(path, "wb") as file:
            json_str = json.dumps(data)
            compressed = zlib.compress(json_str.encode('utf-8'))
            encoded = base64.b64encode(compressed)
            file.write(encoded)
            file.close()
            #Logger.log("Saved data")

    @staticmethod
    def loadData(path):
        try:
            with open(path, "rb") as file:
                encoded = file.read()
                compressed = base64.b64decode(encoded)
                json_str = zlib.decompress(compressed).decode('utf-8')
                data = json.loads(json_str)
                file.close()
                return data
            return None
        except FileNotFoundError:
            Logger.log(f"Couldn't find the file '{path}'. (PYGE_FILE_NOT_FOUND_ERROR, PYGE_NON_FATAL_ERROR)", LogType.ERROR, "SaveLoad")
            return None