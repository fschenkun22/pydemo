import xlrd

# 用xlrd打开221012-022.xls
data = xlrd.open_workbook('221012-022.xls') 
print("sheets 数量: ", data.nsheets)
print('sheets 名称: ', data.sheet_names())
sh = data.sheet_by_name('玻璃门') # 用索引取第一个sheet

for d in sh:
    print(d)














