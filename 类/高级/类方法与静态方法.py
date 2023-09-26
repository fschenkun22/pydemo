
class Student():
    # 类属性
    类name = '类的name'

    def __init__(self, name):
        # 实例属性
        self.name = name

    @classmethod
    def say(cls):
        print('My name is {0}'.format(cls.类name))
    
    def says(self):
        print('正常打印实例属性：{0}'.format(self.name))

    def 普通方法(self):
        print('普通方法')
        print(Student.类name)

    # 静态方法，只是定义在类范围内的一个函数而已
    @staticmethod
    def 静态方法():
        print('静态方法')
        print("静态方法打印出类的属性："+Student.类name)

if __name__ == '__main__':

    student1 = Student('张三')
    student1.say()
    student1.says()
    student1.普通方法()
    student1.静态方法()

