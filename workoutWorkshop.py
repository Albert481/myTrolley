class workoutProgram:
    def __init__(self, weight, height, medical_condition, allergy):
        self.__weight = weight
        self.__height = height
        self.__medical_condition = medical_condition
        self.__allergy = allergy

    def get_weight(self):
        return self.__weight

    def set_weight(self,weight):
        self.__weight = weight

    def get_height(self):
        return self.__height

    def set_height(self, height):
        self.__height = height

    def get_medical_condition(self):
        return self.__medical_condition

    def set_medical_condition(self, medical_condition):
        self.__medical_condition = medical_condition

    def get_allergy(self):
        return self.__allergy

    def set_allergy(self, allergy):
        self.__allergy = allergy
