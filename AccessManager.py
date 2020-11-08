# Structural design patern - Proxy
class UserManager:
    def __init__(self):
        self.__users = {}

    def _add_user(self, user_id, data):
        self.__users[user_id] = data

    def _get_user(self, user_id):
        return self.__users[user_id]

class AccessManager(UserManager):
    def __init__(self, um):
        self.um = um

    def add_user(self, user_id, data, password):
        if password == "adminPassword":
            self.um._add_user(user_id, data)
        else:
            print("Wrong password.")

    def get_user(self, user_id, password):
        if password == "userPassword":
            return self.um._get_user(user_id)
        else:
            print("Wrong password.")
