from copy import deepcopy

patient_core_populated_table_loc = 'PatientCorePopulatedTable.txt'
admission_diagnose_core_populated_table_loc = 'AdmissionsDiagnosesCorePopulatedTable.txt'
admission_core_populated_table_loc = 'AdmissionsCorePopulatedTable.txt'

def _process_patient_core_populated_table(table_loc):
    file = open(table_loc, 'r')
    head = True
    data = {}
    for line in file:
        if head:
            head = False
            continue
        splited = line.split()
        this_patient = {}
        this_patient_id = splited[0]
        this_patient['gender'] = splited[1]
        this_patient['dob'] = splited[2]
        if splited[4].lower() == 'african':
            this_patient['race'] = 'Black'
            this_patient['marital_status'] = splited[6]
            this_patient['lang'] = splited[7]
            this_patient['poverty'] = splited[8]
        else:
            this_patient['race'] = splited[4]
            this_patient['marital_status'] = splited[5]
            this_patient['lang'] = splited[6]
            this_patient['poverty'] = splited[7]
        data[this_patient_id] = this_patient
    return data

def _process_admission_diagnose_core_populated_table(table_loc):
    file = open(table_loc, 'r')
    head = True
    data = {}
    for line in file:
        if head:
            head = False
            continue
        splited = line.split()
        this_patient_id = splited[0]
        code = splited[2]
        if this_patient_id in data:
            p_data = data[this_patient_id]
            p_data.append(code)
        else:
            p_data = []
            p_data.append(code)
            data[this_patient_id] = p_data
    return data

def _process_admission_core_populated_table(table_loc):
    file = open(table_loc, 'r')
    head = True
    data = {}
    for line in file:
        if head:
            head = False
            continue
        splited = line.split()
        this_patient_id = splited[0]
        start_data = splited[2]
        end_data = splited[4]
        if this_patient_id in data:
            p_data = data[this_patient_id]
            p_data.append((start_data, end_data))
        else:
            p_data = []
            p_data.append((start_data, end_data))
            data[this_patient_id] = p_data
    return data

def _join_all_data(p_core, p_diag, p_admission):
    data = deepcopy(p_core)
    for patient_id in data:
        diag = p_diag[patient_id]
        admission = p_admission[patient_id]
        p_data = data[patient_id]
        p_data['diagnose'] = diag
        p_data['admission_dates'] = admission
    return data

def process():
    p_core = _process_patient_core_populated_table(patient_core_populated_table_loc)
    p_diag = _process_admission_diagnose_core_populated_table(admission_diagnose_core_populated_table_loc)
    p_admission = _process_admission_core_populated_table(admission_core_populated_table_loc)
    data = _join_all_data(p_core, p_diag, p_admission)
    return data

if __name__ == "__main__":
    process()