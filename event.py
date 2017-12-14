class Event:
    def __init__(self, eventName, startDate, endDate, image, link):
        self.__eventName = eventName
        self.__startDate = startDate
        self.__endDate = endDate
        self.__image = image
        self.__link = link

    def get_eventName(self):
        return self.__eventName
    def set_eventName(self, eventName):
        self.__eventName = eventName

    def get_startDate(self):
        return self.__startDate
    def set_startDate(self, startDate):
        self.__startDate = startDate

    def get_endDate(self):
        return self.__endDate
    def set_endDate(self, endDate):
        self.__endDate = endDate

    def get_image(self):
        return self.__image
    def set_image(self, image):
        self.__image = image

    def get_link(self):
        return self.__link
    def set_link(self, link):
        self.__link = link

    # def sortdate(self):
    #     if self.__startDate == self.__endDate:
    #         return self.__endDate
    #     else:
    #         return self.__startDate

#event1 = Event('1', 'Simei: Therapeutic Yoga', '02-01-2018', '27-02-2018')
#event2 = Event('2', 'Yin Yoga @ MacPherson', '09-01-2018', '27-03-2018')
#event3 = Event('3', 'Organic Family Movement', '20-01-2018', '20-01-2018')
#event4 = Event('4', 'Mindfulness Foundation Course', '31-01-2018', '21-02-2018', )

