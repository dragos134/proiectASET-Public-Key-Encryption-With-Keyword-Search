import copy
from Models import Mail
# Creational design pattern - Prototype
class MailPrototype:

    _type = None
    _value = None

    def clone(self):
        pass

    def getType(self):
        return self._type

    def getValue(self):
        return self._value

class Draft(MailPrototype):

    def __init__(self, Mail : Mail):
        self._type = "Draft"
        self._value = Mail

    def clone(self):
        return copy.copy(self)

class Forward(MailPrototype):

    def __init__(self, Mail : Mail):
        self._type = "Forward"
        self._value = Mail

    def clone(self):
        return copy.copy(self)

class Sent(MailPrototype):

    def __init__(self, Mail : Mail):
        self._type = "Sent"
        self._value = Mail

    def clone(self):
        return copy.copy(self)
