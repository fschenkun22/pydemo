
class 父类:
    def __init__(self) -> None:
        self.属性 = "父类的属性😒"
        print("父类的构造方法执行")


class 子类(父类):
    # 如果子类没有进行__init__方法实现，父类的将会被自动调用
    # 如果一旦实现了__init__方法，父类的__init__方法将不会被自动调用,需要super
    def __init__(self) -> None:
        super().__init__()
        self.属性 = "子类的属性😄"
        print("子类的构造方法执行")
    pass

class 子类2():
    pass

def main():
    对象 = 子类()
    print(对象.属性)

    # 判断当前对象是不是前面对象生的
    print(isinstance(对象, 子类2))

    # 判断当前类是不是后面类的子类
    print(issubclass(子类, 父类))



if __name__ == "__main__":
    main()

         
    


