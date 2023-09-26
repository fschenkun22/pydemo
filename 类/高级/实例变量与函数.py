# 定义实例函数

class Student():
    class_name = 'class的name'

    def __init__(self,name) -> None:
        self.name = name

        print ('我是构造函数')

    # 实例函数有个self
    def say(self):
        self.age = 200
        print('My name is {0}'.format(self.name))
        print('My age is {0}'.format(self.age))


if __name__ == '__main__':
    # 实例化一个对象
    stu1 = Student('yaona')
    stu1.say()
    print(stu1.class_name)
    stu1.可以动态添加属性 = '动态添加的属性'
    print(stu1.可以动态添加属性)

    stu2 = Student('yao')
    print(stu2.class_name)
    stu2.say()