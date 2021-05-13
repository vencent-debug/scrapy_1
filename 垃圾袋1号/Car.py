class Car():
    # brand, model, year
    def __init__(self,brand):
        self.brand = brand
        model = 'xxx'
        year = 0

    def set_model(self, model):
        self.model = model
        print("this car's model:"+self.model)

    def set_year(self,year):
        self.year = year
        print("this car's year :" +self.year)

    def get_info(self):
        print(f"Brand:{self.brand},Model:{self.model},Year:{self.year}")

