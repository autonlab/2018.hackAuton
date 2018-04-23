import re
with open("./dataset/val_1.txt",'r') as f:
    ss=""
    for row in f.readlines()[:5000]:
        tmp=row[row.find('/')+1:]
        ss="".join([ss,tmp])
    with open("val_1.txt",'w') as f:
        f.write(ss)
