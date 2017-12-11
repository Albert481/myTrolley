class Reports:
    def __init__(self, fault, comment, count, location):
        self.__fault = fault
        self.__comment = comment
        self.__count = count
        self.__location = location

    def get_fault(self):
        return self.__fault
    def get_comment(self):
        return self.__comment
    def get_count(self):
        return self.__count
    def get_location(self):
        return self.__location