class Workout:
    def __init__(self, time, diff_level, body_focus):
        self.__time = time
        self.__diff_level = diff_level
        self.__body_focus = body_focus

    def get_time(self):
        return self.__time

    def set_time(self, time):
        self.__time = time

    def get_diff_level(self):
        return self.__diff_level

    def set_diff_level(self, diff_level):
        self.__diff_level = diff_level

    def get_body_focus(self):
        return self.__body_focus

    def set_body_focus(self, body_focus):
        self.__body_focus = body_focus
