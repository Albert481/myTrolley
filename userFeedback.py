class userFeedback:
    def __init__(self, email_name, user_email, email_comment):
        self.__email_name = email_name
        self.__user_email = user_email
        self.__email_comment = email_comment

    def get_email_name(self):
        return self.__email_name

    def get_user_email(self):
        return self.__user_email

    def get_email_comment(self):
        return self.__email_comment

    def set_email_name(self, email_name):
        self.__email_name = email_name

    def set_user_email(self, user_email):
        self.__user_email = user_email

    def set_email_comment(self, email_comment):
        self.__email_comment = email_comment