filename ='phonenumbers.txt'
#生成密码字典 以130开头11位
def generate_phonenumbers():
    with open(filename,'w') as f:
        for i in range(13000000000,13999999999):
            f.write(str(i)+'\n')

generate_phonenumbers()