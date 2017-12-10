class Reports:
    def __init__(self, fault, comment, count):
        self.__fault = fault
        self.__comment = comment
        self.__count = count

    def get_fault(self):
        return self.__fault
    def get_comment(self):
        return self.__comment
    def get_count(self):
        return self.__count