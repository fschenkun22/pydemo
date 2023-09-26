from pprint import pprint


class Student:
    count = 0

# main
if __name__ == '__main__':

    # 类可以理解为一个对象，类的属性就是对象的属性，属性可以被外部修改
    # 可以修改的属性叫做类的属性，不可以修改的属性叫做类的常量
    # 可以修改的属性是不是可以叫做静态属性，不可以修改的属性是不是可以叫做静态常量

    print(Student.count)
    print(getattr(Student, 'count'))
    # 取得类的属性

    print(hasattr(Student, 'count'))
    # 判断类是否有某个属性

    # 如果属性找不到，默认一个hello
    print(getattr(Student, 'xxx', 'hello'))

    # 在外部修改类的属性
    setattr(Student, 'count', 10)
    print(Student.count)

    # java里叫反射
    Student.count = 100
    print(Student.count)

    # 这样可以添加一个静态变量，嗯 这样也可以
    Student.新建用户名1 = '张三'
    print(Student.新建用户名1)

    # 删除一个变量
    # del Student.新建用户名1
    # print(Student.新建用户名1)

    # delattr(Student, 'count')
    # print(Student.count)

    # 创造两个对象

    s1 = Student()
    s2 = Student()

    # 现在设Student静态变量的值
    Student.count = 1000
    print(s1.count)
    print(s2.count)
    print('------------------')

    # 现在设s1静态变量的值
    s1.count = 2000
    s2.count = 3000
    print(s1.count)
    print(s2.count)
    print(Student.count)

    # 综上所述，python是把类变量存放在__dict__这个字典中，但不要修改这个字典，否则会出现问题
    pprint(Student.__dict__)
