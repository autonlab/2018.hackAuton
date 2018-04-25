import csv
import operator

important_rank = 6

def process_opioid_table(list_table):
    patient_id = 0
    data = {}
    for table_loc in list_table:
        with open(table_loc, 'rb') as csvfile:
            data_reader = csv.reader(csvfile, delimiter=',')
            header = True
            for row in data_reader:
                if header:
                    header = False
                    continue
                this_patient_data = {}
                this_patient_data['death_date'] = row[0]
                this_patient_data['death_time'] = row[1]
                if row[2] == 'Accident':
                    manner = 0
                else: # Accidents
                    manner = 1
                this_patient_data['manner'] = manner
                this_patient_data['age'] = row[3]
                this_patient_data['gender'] = row[4]
                this_patient_data['race'] = row[5]
                this_patient_data['case_dispo'] = row[6]
                # 7 ~ 13 (inclusive) 7 kinds of doses
                this_patient_data['doses'] = []
                for i in range(7, 14):
                    if row[i] != '':
                        this_patient_data['doses'].append(row[i])
                # incident_zip 14
                this_patient_data['incident_zip'] = row[14]
                # decedent_zip 15
                this_patient_data['decedent_zip'] = row[15]
                # case year 16
                this_patient_data['case_year'] = row[16]
                # store this patient's info
                data[patient_id] = this_patient_data
                patient_id += 1
    return data, patient_id

def sort_important_doses(num_rank, data_list):
    all_kinds = {}
    for data in data_list:
        for patient_id in data:
            doses = data[patient_id]['doses']
            for d in doses:
                if not d in all_kinds:
                    all_kinds[d] = 1
                else:
                    all_kinds[d] += 1
    sorted_all_kinds = sorted(all_kinds.items(), key=operator.itemgetter(1))[::-1]
    selected = []
    selected_num = 0
    total_num = sum(all_kinds.values())
    for i in range(num_rank):
        d, num = sorted_all_kinds[i]
        selected_num += num
        selected.append(d)
    percentage = float(selected_num) / float(total_num)
    return all_kinds, selected, percentage

if __name__ == "__main__":
    # 2015
    data, num_patients = process_opioid_table(['fatal_accidental_od_2015.csv','fatal_accidental_od_2016.csv'])
    all_kinds, selected, percentage = sort_important_doses(important_rank, [data])
    print(selected)

