class Email:
    def __init__(self, name, user_email, feedback):
        self.__name = name
        self.__user_email = user_email
        self.__feedback = feedback

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__user_email

    def get_feedback(self):
        return self.__feedback

    def set_name(self, name):
        self.__name = name

    def set_email(self, user_email):
        self.__user_email = user_email

    def set_feedback(self, feedback):
        self.__feedback = feedback
