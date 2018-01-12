#Parent class
class trolleys:
    def __init__(self, name, fault, count, location, comments):
        self.__trolleyid = ''
        self.__name = name
        self.__fault = fault
        self.__count = count
        self.__location = location
        self.__comments = comments

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
    def get_trolleyid(self):
        return self.__trolley
    def set_trolleyid(self, trolleyid):
        self.__trolleyid = trolleyid

#Report function for scanner page
class Report:
    def __init__(self, comments):
        self.__comments = comments

    def get_comments(self):
        return self.__comments

class ReportF(Report):
    def __init__(self, fault, count, comments):
        super().__init__(comments)
        self.__fault = fault
        self.__count = count
        self.__comments = comments

    def get_fault(self):
        return self.__fault
    def get_count(self):
        return self.__count
    def get_comments(self):
        return self.__comments

class ReportL(Report):
    def __init__(self, location, comments):
        super().__init__(comments)
        self.__location = location

    def get_location(self):
        return self.__location

# Search function for admin page
class FindTrolley(trolleys):
    def __init__(self, name, fault, count, location, comments):
        super().__init__(name, fault, count, location, comments)