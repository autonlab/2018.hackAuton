import csv
import random
from datetime import date

overdose = []
synthetic = {}

AdmissionsCorePopulatedTable = open("./Data/10000-Patients/AdmissionsCorePopulatedTable.txt","r")
isHead = True
for line in AdmissionsCorePopulatedTable:
    if isHead:
        isHead = False
        continue
    fields = line.split("\t")
    PatientID = fields[0]
    AdmissionID = fields[1]
    AdmissionStartDate = fields[2]
    start_yr = int(AdmissionStartDate[:4])
    start_month = int(AdmissionStartDate[5:7])
    start_date = int(AdmissionStartDate[8:10])
    AdmissionEndDate = fields[3]
    end_yr = int(AdmissionEndDate[:4])
    end_month = int(AdmissionEndDate[5:7])
    end_date = int(AdmissionEndDate[8:10])
    d0 = date(start_yr, start_month, start_date)
    d1 = date(end_yr, end_month, end_date)
    DaysOfStay = (d1 - d0).days

    synthetic[PatientID] = {'DaysOfStay': DaysOfStay}

AdmissionsCorePopulatedTable.close()

PatientCorePopulateTable = open("./Data/10000-Patients/PatientCorePopulatedTable.txt","r")
isHead = True
for line in PatientCorePopulateTable:
    if isHead:
        isHead = False
        continue
    fields = line.split("\t")
    PatientID = fields[0]
    Gender = fields[1]
    DateOfBirth = fields[2]
    Age = 2018 - int(DateOfBirth[:4])
    Race = fields[3]
    MaritalStatus = fields[4]
    Language = fields[5]
    PercentBelowPoverty = float(fields[6][:-1])/100

    data = {'Gender': Gender, 'Age': Age, 'Race': Race, 'MaritalStatus': MaritalStatus,
                    'Language': Language, 'PercentBelowPoverty': PercentBelowPoverty}
    for features in data:
        synthetic[PatientID][features] = data[features]

PatientCorePopulateTable.close()
yrs = [i for i in range(2009, 2018)]
filename = ['fatal_accidental_od_%d.csv'%i for i in yrs]
num_patients = 0
total_age = 0
for f in filename:
    with open('./Data/allegheny/%s'%f) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            num_patients += 1
            overdoses = []
            for i in range(1, 8):
                col_name = 'Combined OD%d'%i
                if len(row[col_name]) > 0:
                    overdoses.append(row[col_name])
            if row['Age'] == '':
                row['Age'] = -1
            else:
                total_age += int(row['Age'])
            overdose.append({'Age': int(row['Age']), 'Sex': row['Sex'], 'Race': row['Race'], 'Overdoses': overdoses})
avg_age = total_age/num_patients
for patient in overdose:
    if patient['Age'] == -1:
        patient['Age'] = avg_age


for patient in overdose:
    similar_patients = []
    for patientID in synthetic:
        if (synthetic[patientID]['Gender'] == patient['Sex'] and 
                    (synthetic[patientID]['Race'] == patient['Race'] or synthetic[patientID]['Race'] == 'Unknown') and 
                    abs(synthetic[patientID]['Age'] - patient['Age']) <= 100):
            similar_patients.append(patientID)
    match_ID = random.choice(similar_patients)
    for features in synthetic[match_ID]:
        patient[features] = synthetic[match_ID][features]

output = []

top_drugs = ['Heroin', 'Fentanyl', 'Cocaine', 'Alcohol', 'Alprazolam', 'Oxycodone']
races = ['Unknown', 'Middle Eastern', 'Hispanic', 'Black', 'Asian', 'White']
languages = ['English', 'Icelandic', 'Unknown', 'Spanish']
MaritalStatus = ['Single', 'Married', 'Divorced', 'Separated', 'Unknown', 'Widowed']
with open('synthetic.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ')
    for row in overdose:
        drugs = [0,0,0,0,0,0,0]
        race = [0,0,0,0,0,0,0]
        language = [0,0,0,0]
        marital = [0,0,0,0,0,0,0]

        for drug in row['Overdoses']:
            if drug in top_drugs:
                idx = top_drugs.index(drug)
                drugs[idx] = 1
            else:
                drugs[6] = 1

        if row['Sex'] == 'Female':
            gender = 1
        else: gender = 0

        race_idx = races.index(row['Race'])
        race[race_idx] = 1

        language_idx = languages.index(row['Language'])
        language[language_idx] = 1

        marital_idx = MaritalStatus.index(row['MaritalStatus'])
        marital[marital_idx] = 1

        result = []
        for i in [row['Age'], gender, race, drugs, marital, language, 
                        row['PercentBelowPoverty']]:
            if (type(i) == list):
                result = result + i
            else:
                result.append(i)
        output.append(result)
        writer.writerow(result)
