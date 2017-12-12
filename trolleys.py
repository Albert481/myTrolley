#Parent class
class trolleys:
    def __init__(self, fault, count, location, comments):
        self.__name = ''
        self.__fault = fault
        self.__comments = comments
        self.__count = count
        self.__location = location

    def get_name(self):
        return self.__name
    def get_fault(self):
        return self.__fault
    def get_count(self):
        return self.__count
    def get_location(self):
        return self.__location
    def get_comments(self):
        return self.__comments

#Report function for scanner page
class Reports(trolleys):
    def __init__(self, fault, count, location, comments):
        super().__init__(fault, count, location, comments)
        self.__name = ""
        self.__fault = fault
        self.__comments = comments
        self.__count = count
        self.__location = location

#Search function for admin page
class FindTrolley(trolleys):
    def __init__(self, name, fault, count, location, comments):
        super().__init__(fault, count, location, comments)
        self.__name = name

    def get_name(self):
        return self.__name
