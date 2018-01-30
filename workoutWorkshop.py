class workoutProgram:
    def __init__(self, name, gender, age, weight, height, medical_history, allergy):
        self.__name = name
        self.__gender = gender
        self.__age = age
        self.__weight = weight
        self.__height = height
        self.__medical_history = medical_history
        self.__allergy = allergy

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_gender(self):
        return self.__gender

    def set_gender(self, gender):
        self.__gender = gender

    def get_age(self):
        return self.__age

    def set_age(self, age):
        self.__age = age

    def get_weight(self):
        return self.__weight

    def set_weight(self,weight):
        self.__weight = weight

    def get_height(self):
        return self.__height

    def set_height(self, height):
        self.__height = height

    def get_medical_history(self):
        return self.__medical_history

    def set_medical_history(self, medical_history):
        self.__medical_history = medical_history

    def get_allergy(self):
        return self.__allergy

    def set_allergy(self, allergy):
        self.__allergy = allergy
