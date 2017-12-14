class Product:
    def __init__(self, name, category, price, origin, image_name):
        self.__name = name
        self.__category = category
        self.__price = price
        self.__origin = origin
        self.__image_name = image_name

    def get_name(self):
        return self.__name
    def set_name(self, name):
        self.__name = name

    def get_category(self):
        return self.__category
    def set_category(self, category):
        self.__category = category

    def get_price(self):
        return self.__price
    def set_price(self, price):
        self.__price = price

    def get_origin(self):
        return self.__origin
    def set_origin(self, origin):
        self.__origin = origin

    def get_image_name(self):
        return self.__image_name
    def set_image_name(self, image_name):
        self.__image_name = image_name
