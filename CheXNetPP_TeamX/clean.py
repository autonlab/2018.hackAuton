import csv
import numpy
file = open('img_ohe.txt', 'w')
train = open('training.txt', 'w')
val = open ('validation.txt', 'w')
test = open ('test.txt', 'w')
with open('Data_Entry_2017.csv', 'r') as csvfile:
    array = csvfile.readlines()[1:]
    L = ["Atelectasis", "Cardiomegaly", "Effusion", "Infiltration", "Mass", "Nodule", "Pneumonia", "Pneumothorax",
         "Consolidation", "Edema", "Emphysema", "Fibrosis", "Pleural_Thickening", "Hernia"]
    print(len(L))
    L = [s.encode("utf-8") for s in L]
    dic = dict([(L[i], i) for i in range(len(L))])
    ss=[]
    for row in array:
        arr = row.strip().split(',')
        vec=["0"]* 14
        if arr[1].strip() != "No Finding":
            for lbl in arr[1].strip().split('|'):
                vec[dic[lbl.encode("utf-8")]]="1"
        gender = ""
        if arr[5].strip() == "M":
            gender = "0"
        else:
            gender = "1"

        ss.append("".join([arr[0]," "," ".join(vec)," ", arr[2]," ", arr[4], " ",gender, '\n']))

    numpy.random.shuffle(ss)
    training, validation, tes = ss[:80000], ss[80000:92000], ss[92000:]
    train.writelines(training)
    val.writelines(validation)
    test.writelines(tes)

file.close()
