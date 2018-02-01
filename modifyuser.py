class Users:
    def __init__(self, update_username, update_email, update_password):
        self.__update_username = update_username
        self.__update_email = update_email
        self.__update_password = update_password
        self.__admin = 0

    def get_update_username(self):
        return self.__update_username

    def get_update_email(self):
        return self.__update_email

    def get_update_password(self):
        return self.__update_password

    def set_update_username(self, update_username):
        self.__update_username = update_username

    def set_update_email(self, update_email):
        self.__update_email = update_email

    def set_update_password(self, update_password):
        self.__update_password = update_password


