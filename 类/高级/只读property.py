
class Square:
    def __init__(self, width):
        self.__width = width
        # 建立面积缓存
        self.__area = None
    
    # 这里注册一个width的property
    @property
    def width(self):
        return self.__width
    
    # 这里注册一个width的setter,如果有给s1的实例对象赋值，就会调用这个setter
    # 调用这个setter后，会把self.__area设置为None，这样下次读取面积的时候，就会重新计算面积
    @width.setter
    def width(self, value):
        self.__width = value
        self.__area = None

    # 这里注册一个area的property，如果有读取s1.area，就会调用这个area
    # 如果self.__area为None，就会计算面积，如果self.__area不为None，就直接返回self.__area
    @property
    def area(self):
        if self.__area is None:
            print("Calculating area...")
            self.__area = self.__width ** 2
        return self.__area

def main():
    # 第一次计算面积时候，slef.width = 5 
    s1 = Square(5)

    # 第一次读取面积时候，因为self.__area = None，所以会计算面积
    print(s1.area)

    # 第二次读取面积时候，因为self.__area = 25，所以不会计算面积
    print(s1.area)
    print(s1.area)
    print(s1.area)

    s1.width = 6
    print(s1.area)
    print(s1.area)

    s1.width = 7
    print(s1.area)
    print(s1.area)

if __name__ == "__main__":
    main()