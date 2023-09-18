"""
    面向对象，数据分析案例，主业务逻辑代码
    实现步骤：
        1. 设计一个类，可以完成数据的封装 ok
        2. 设计一个抽象类，定义文件读取的相关功能，并使用子类实现具体功能
        3. 读取文件，生产数据对象
        4. 进行数据需求的逻辑计算（计算每一天的销售额）
        5. 绘制图形
        https://blog.csdn.net/qq_44984700/article/details/130120464
"""

from typing import List
from file_define import FileReader, TextFileReader, JsonFileReader
from data_define import Record

textRd = TextFileReader('2011年1月销售数据.txt')
jsonRd = JsonFileReader('2011年2月销售数据.txt')

jan_data: List[Record] = textRd.read_data()
feb_data: List[Record] = jsonRd.read_data()

# 合并jan_data, feb_data
all_data: List[Record] = jan_data + feb_data

data_dict = {}
for record in all_data:
    if record.date in data_dict:
        data_dict[record.date] += record.money
    else:
        data_dict[record.date] = record.money



print(data_dict)