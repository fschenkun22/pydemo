# __str__
# __repr__
# __iter__
# __next__
# __getitem__
# __getattr__
# __call__
# __len__
# __int__
# __float__
# __str__
# __cmp__
# __eq__
# __hash__

class MyDate:
    def __init__(self,year,month,day) -> None:
        super().__init__()
        self.year = year
        self.month = month
        self.day = day
        
    # def __str__(self) -> str:
    #     print('__str__被调用了')
    #     return f'{self.year}-{self.month}-{self.day}'
    
    # __repr__是__str__的备胎 当__str__不存在时，会调用__repr__ 
    def __repr__(self) -> str:
        print('__repr__被调用了，可以用于调试')
        return f'{self.year}-{self.month}-{self.day}'
    
    def __eq__(self, __value: object) -> bool:
        print('__eq__被调用了')
        return self.year == __value.year and self.month == __value.month and self.day == __value.day
    
    def __hash__(self) -> int:
        print('__hash__被调用了')
        return hash((self.year,self.month,self.day))
    
    def __bool__(self) -> bool:
        print('__bool__被调用了')
        return False
    
    def __len__(self) -> int:
        print('__len__被调用了')
        return 365
    
    def __del__(self) -> None:
        print('__del__被调用了')

if __name__ == '__main__':
    my_date = MyDate(2021,9,1)
    my_date2 = MyDate(2021,9,2)
    my_date3 = my_date
    print(my_date)
    print(str(my_date))

    # 当判断两个对象是否相等时候 会触发eq方法，通过eq方法比较两个不同实例中的某些属性是否相等，然后输出结果
    print(my_date == my_date2)
    # 如果是比较两个实例的地址用is,也就是判断地址是否相等
    print(my_date is my_date3)

    date_set = {my_date,my_date2,my_date3}

    # 给对象添加唯一hash 用于判断是否重复
    print(hash(my_date))
    print(hash(my_date2))
    print(hash(my_date3))

    # 当判断对象是否为真时候，会触发bool方法，如果bool方法返回True则为真，否则为假
    print(bool(my_date))

    # 当获取对象长度时候，会触发len方法，len方法返回的是一个整数
    print(len(my_date))