#Parent Class
class Recipe:
    def __init__(self, recipeName, image, serving, cooktime, ingredient, method, link):
        self.__recipeid = ""
        self.__recipeName = recipeName
        self.__image = image
        self.__serving = serving
        self.__cooktime = cooktime
        self.__ingredient = ingredient
        self.__method = method
        self.__link = link

    def get_recipeid(self): #just added get & set
        return self.__recipeid
    def set_recipeid(self, recipeid):
        self.__recipeid = recipeid

    def get_recipeName(self):
        return self.__recipeName
    def set_recipeName(self, recipeName):
        self.__recipeName = recipeName

    def get_image(self):
        return self.__image
    def set_image(self, image):
        self.__image = image

    def get_serving(self):
        return self.__serving
    def set_serving(self, serving):
        self.__serving = serving

    def get_cooktime(self):
        return self.__cooktime
    def set_cooktime(self, cooktime):
        self.__cooktime = cooktime

    def get_ingredient(self):
        return self.__ingredient
    def set_ingredient(self, ingredient):
        self.__ingredient = ingredient

    def get_method(self):
        return self.__method
    def set_method(self, method):
        self.__method = method

    def get_link(self):
        return self.__link
    def set_link(self, link):
        self.__link = link


