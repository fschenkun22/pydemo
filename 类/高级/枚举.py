from enum import Enum


class VIP(Enum):
    YELLOW = 1
    GREEN = 2
    BLACK = 3
    RED = 4

class Student:
    def __init__(self):
        self.color = VIP.BLACK.name
        print(self.color)


s = Student()

for temp in VIP:
    print(temp)