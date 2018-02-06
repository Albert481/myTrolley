class Users:
    def __init__(self, username, email, password, confirm_pass):
        self.__username = username
        self.__email = email
        self.__password = password
        self.__confirm_pass = confirm_pass
        self.__admin = 0

    def get_username(self):
        return self.__username

    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password

    def get_confirm_pass(self):
        return self.__confirm_pass

    def set_username(self, username):
        self.__username = username

    def set_email(self, email):
        self.__email = email

    def set_password(self, password):
        self.__password = password

    def set_confirm_pass(self, confirm_pass):
        self.__confirm_pass = confirm_pass


class Admin:
    def __init__(self, username, email, admin):
        self.__username = username
        self.__email = email
        self.__admin = admin

    def get_username(self):
        return self.__username

    def get_email(self):
        return self.__email

    def get_admin(self):
        return self.__admin

    def set_admin(self, admin):
        self.__admin = admin
