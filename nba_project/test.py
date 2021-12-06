
#coding=utf-8
import pandas as pd
csv_data = pd.read_csv('C:\\Users\\46417\\Desktop\\harden_xymade.csv')
list_ = csv_data.values.tolist()
list_made = list()
list_nomade =list()
for i in list_:
    temp = [i[0], i[1]]
    if i[2] == 1:
        list_made.append(temp)
    else:
        list_nomade.append(temp)
print(list_made)
print(list_nomade)