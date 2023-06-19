class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.introduce()

    def introduce(self):
        print(f"Hello, my name is {self.name} and I'm {self.age} years old.")


# Creating an object of the Person class
john = Person("John", 25)
