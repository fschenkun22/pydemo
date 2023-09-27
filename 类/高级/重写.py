
# 
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def say(self):
        print(f"我是人类{self.name}, 我的年龄是{self.age}")


class Student(Person):
    def __init__(self, name, age, score):
        super().__init__(name, age)
        Person.__init__(self, name, age)
       

    def say(self):
        print(f"我是学生类{self.name}, 我的年龄是{self.age}")


def render (person:Person):
    person.say()

def main():
    s = Student("张三", 18, 100)
    s.say()

    s1 = Person("李四", 20)
    s1.say()
    render(s)
    render(s1)



if __name__ == "__main__":
    main()
