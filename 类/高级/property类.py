
class Student:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.__age = age

    def set_age(self, age: int) -> None:
        print("set_age 被调用")
        if age < 0:
            print("年龄不能为负数")
            return
        self.__age = age

    def get_age(self) -> int:
        print("get_age 被调用")
        return self.__age

    def __str__(self) -> str:
        return f"name:{self.name},age:{self.__age}"

    age = property(fget=get_age, fset=set_age)


def main():
    stu = Student("小明", 18)

    # 操作对应age属性的时候会默认触发对应property修饰的方法,赋值触发fset，取值触发fget
    stu.age = -10

    print(stu.age)


if __name__ == "__main__":
    main()
