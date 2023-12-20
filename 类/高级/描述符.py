class Student:
    def __init__(self,n1:str,n2):
        self.__first_name = n1
        self.last_name = n2
        print('init')

    @property
    def first_name (self):
        print('getter 被执行')
        return self.__first_name

    @first_name.setter
    def first_name(self,val):
        print('setter 被执行')
        if not isinstance(val,str):
            print('判断')
            raise Exception('Must not be str ')

        self.__first_name = val
        print('进来先调用的setter')



if __name__ == '__main__':
    s = Student(111,111)
    print(s.first_name)
  
    # s.first_name = 111
    print(s.first_name)