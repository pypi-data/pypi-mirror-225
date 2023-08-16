
class NewPerson:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def say_hello(self):
        print(f"Hello, my name is {self.name} and I am {self.age} years old.")

    def say_hello_new(self, name, age=27):
        print(f"Hello, my name is {name} and I am {age} years old.")
