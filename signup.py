class WebUsers:
    def __init__(self, fname, lname, username, email, category, password, confirmpass, accept_rules):
        self.__fname = fname
        self.__lname = lname
        self.__username = username
        self.__email = email
        self.__password = password
        self.__confirmpass = confirmpass
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

