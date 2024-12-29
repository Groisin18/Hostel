class Person:

    def __init__(self, info_dict: dict):
        self.family = info_dict['family'] 
        self.name = info_dict['name'] 
        self.surname = info_dict['surname'] 
        self.sex = info_dict['sex'] 
        self.age = info_dict['age'] 

