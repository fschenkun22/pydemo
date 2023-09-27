from abc import ABC, abstractmethod
import time

class Action(ABC):
    def __init__(self):
        pass
    
    # 定义一个标准的接口，继承Action的类必须实现do方法
    @abstractmethod
    def do(self):
        pass


class Student(Action):
    def __init__(self):
        pass
    
    def do(self):
        print('学生上课')

class Student2(Action):
    def __init__(self):
        pass
    
    def do(self):
        print('学生上课2')


# 定义一个函数，必须接受定义的标准do接口
def excute(action:Action):
    action.do()

def main():

    # 下面两个类都继承了Action，所以都可以传入excute函数
    # excute(Student())
    # excute(Student2())

    s1 = Student()
    s2 = Student2()


    # excute能接受这两个实例的原因是，这两个类都继承了Action,do方法必须按标准实现，所以可以传入
    excute(s1)
    excute(s2)





if __name__ == '__main__':
    main()

    
