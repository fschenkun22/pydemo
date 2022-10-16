import pandas as pd

#读取excel的数据到pd
df = pd.read_excel('221012-022.xls', sheet_name='柜体')

for indexs in df.index:
    #print(df.loc[indexs].values)
    #print(df.loc[indexs].values[0])
    print(type(df.loc[indexs].values[8]))
    print(df.loc[indexs].values[8])
    if (df.loc[indexs].values[8] == float('nan') ) :
        print('是空')

