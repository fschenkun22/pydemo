# 在当前文件夹下建立一个新文件夹，文件夹命名用随机命名 包括字母A-Z a-z 0-9 6位 例如：A1b2C3


# 1. 生成随机文件夹名
import random
import string
import os
import shutil

def random_name():
    # return ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    # 返回文件夹名随机6-128位
    return ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(6, 128)))

folder_name = random_name()

# 2. 创建文件夹
os.mkdir(folder_name)

# 循环10次 生成10个文件夹
for i in range(10):
    folder_name = random_name()
    os.mkdir(folder_name)
    # 进入这个文件夹 建立一个随机大小的文件，文件名同样随机，大小在1k - 1M之间
    os.chdir(folder_name)
    file_name = random_name()
    file_size = random.randint(1, 1024) * 1024
    with open(file_name, 'wb') as f:
        f.write(os.urandom(file_size))
    os.chdir('..')



