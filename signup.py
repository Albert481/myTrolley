class WebUsers:
    def __init__(self, fname, lname, username, nric, email, password, confirmpass):
        self.__fname = fname
        self.__lname = lname
        self.__username = username
        self.__nric = nric
        self.__email = email
        self.__password = password
        self.__confirmpass = confirmpass

    #getter methods
    def get_fname(self):
        return self.__fname
    def get_lname(self):
        return self.__lname
    def get_username(self):
        return self.__username
    def get_nric(self):
        return self.__nric
    def get_email(self):
        return self.__email
    def get_password(self):
        return self.__password
    def get_confirmpass(self):
        return self.__confirmpass

    #setter methods
    def set_fname(self, fname):
        self.__fname = fname
    def set_lname(self, lname):
        self.__lname = lname
    def set_username(self,username):
        self.__username = username
    def set_nric(self,nric):
        self.__nric = nric
    def set_email(self,email):
        self.__email = email
    def set_password(self,password):
        self.__password = password
    def set_confirmpass(self,confirmpass):
        self.__confirmpass = confirmpass
