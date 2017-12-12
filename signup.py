class WebUsers:
    def __init__(self, username, email, birthday, category, password, accept_rules):
        self.__username = username
        self.__email = email
        self.__birthday = birthday
        self.__category = category
        self.__password = password
        self.__accept_rules = accept_rules

    #getter methods
    def get_username(self):
        return self.__username
    def get_email(self):
        return self.__email
    def get_birthday(self):
        return self.__birthday
    def get_category(self):
        return self.__category
    def get_password(self):
        return self.__password
    def get_accept_rules(self):
        return self.__accept_rules

    #setter methods
    def set_username(self,username):
        self.__username = username
    def set_email(self,email):
        self.__email = email
    def set_birthday(self, homephone):
        self.__homephone = homephone
    def set_category(self, category):
        self.__category = category
    def set_password(self,password):
        self.__password = password
    def set_accept_rules(self,accept_rules):
        self.__accept_rules = accept_rules

