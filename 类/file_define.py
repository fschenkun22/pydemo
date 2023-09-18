"""
和文件相关的类定义
"""
import json
from data_define import Record
from typing import List
# 先定义一个抽象类用来做顶层设计，确定有哪些功能需要实现


class FileReader:
    """
    读取文件的抽象类
    顶层设计，确定有哪些功能需要实现

    从顶层开始设计，先不考虑具体的实现，只考虑有哪些功能需要实现
    """

    def read_data(self) -> List[Record]:
        """
        读取文件数据，读到的每一条都转换为Record对象，将他们封装到List内返回
        """
        pass


class TextFileReader(FileReader):
    """
    具体的子类实现，用来读取文本文件的类 ， 都要实现父类的read_data方法
    """

    def __init__(self, path):
        self.path = path

    def read_data(self) -> List[Record]:
        f = open(self.path, 'r', encoding='utf-8')
        
        # 读取文件的每一行，然后转换为Record对象，然后封装到List内
        record_list : List[Record] = []

        for line in f.readlines():
            line = line.strip()
            data_list = line.split(',')
            record = Record(data_list[0], data_list[1], int(data_list[2]), data_list[3])
            record_list.append(record)
        
        f.close()
        return record_list
    

class JsonFileReader(FileReader):
    """
    具体的子类实现，用来读取json文件的类 ， 都要实现父类的read_data方法
    """

    def __init__(self, path):
        self.path = path

    def read_data(self) -> List[Record]:
        f = open(self.path, 'r', encoding='utf-8')

        record_list : List[Record] = []

        for line in f.readlines():
            data_dict = json.loads(line)
            record = Record(data_dict['date'], data_dict['order_id'], int(data_dict['money']), data_dict['province'])
            record_list.append(record)
        
        f.close()
        return record_list



if __name__ == '__main__':
    text_reader = TextFileReader('2011年1月销售数据.txt')
    json_reader = JsonFileReader('2011年2月销售数据.txt')

    
    for i in json_reader.read_data():
        print(i.date, i.order_id, i.money, i.province)

    for i in text_reader.read_data():
        print(i.date, i.order_id, i.money, i.province)
    

