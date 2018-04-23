import re
with open("test_1.txt",'r') as f:
    ss=""
    for row in f.readlines():
        tmp=row[row.find('/')+1:]
        ss="".join([ss,tmp])
    with open("out.txt",'w') as f:
        f.write(ss)