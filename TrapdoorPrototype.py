import copy
from abc import ABCMeta, abstractmethod
class Trapdoor(metaclass = ABCMeta):
    def __init__(self):
        self.type = None
        self.key = None
        self.message = str()

    @abstractmethod
    def TypeCript(self):
        pass

    def get_type(self):
        return self.type

    def get_key(self):
        return self.key

    def get_Message(self):
        return self.message

    def set_Message(self, sid):
        self.message = sid

    def clone(self):
        return copy.copy(self)

class Cript(Trapdoor):
    def __init__(self):
        super().__init__()
        self.type = "Algoritmul de criptare"

    def TypeCript(self):
        print("message crypted and informations stored")

class DeCript(Trapdoor):
    def __init__(self):
        super().__init__()
        self.type = "Algoritmul de decriptare"

    def TypeCript(self):
        print("message crypted and informations stored")

class TrapdoorCache ():
    cache = {}

    @staticmethod
    def get_message(sid,message,type):
        Informatii = Trapdoor.cache.get(sid,message,type, None)
        return Informatii.clone()

    @staticmethod
    def load():
        decriptare = DeCript()
        TrapdoorCache.cache[decriptare.get_id()] = [decriptare.get_key(),decriptare.get_Message()]

        criptare = DeCript()
        TrapdoorCache.cache[criptare.get_id()] = [criptare.get_key(), criptare.get_Message()]

"prototipTrapdoor"

