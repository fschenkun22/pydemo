


class Student():
    class_name = 'class的name'

    def __init__(self,name) -> None:
        self.name = name

        print ('我是构造函数')

    # 实例函数有个self
    def __say(self):
        self.age = 200
        print('My name is {0}'.format(self.name))
        print('My age is {0}'.format(self.age))

    def say2(self):
        print('My name is {0}'.format(self.name))
        print('My age is {0}'.format(self.age))

if __name__ == '__main__':
    student1 = Student('张三')
    student1.say()
    student1.say2()
    print(student1.age)
    print(student1.name)
    print(student1.class_name)
    print(Student.class_name)
    #