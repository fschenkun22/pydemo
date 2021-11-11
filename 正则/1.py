import re

t = 'B211211-003,B211211-0004,某身高:178,体重100,学号:123456,密码:9527,211111-001WB,,,21522-005,300000-111'

print(re.findall(r'1',t))

print(re.findall(r'\d+',t))

print(re.findall(r'\d?',t))

print(re.findall(r'\d*',t))

print(re.findall(r'\d{6}-\d{3,4}',t))

print(re.findall(r'\d{6}-\d{3,4}|',t))

## 限定位置

print(re.findall(r'^\d{6}-\d{3,4}',t)) ##基本上可以断言赋码 ^表示开头 $表示结尾

print(re.match(r'^\d{6}-\d{3,4}|^B{1}\d{6}-\d{3,4}',t))  # match 如果找不到返回None
