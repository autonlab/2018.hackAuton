import random
import json
import pickle
import opioid_data_process as opi_process
import patient_data_process as pd_process
from copy import deepcopy

list_opioid_table = ['fatal_accidental_od_2008.csv',
                     'fatal_accidental_od_2009.csv',
                     'fatal_accidental_od_2010.csv',
                     'fatal_accidental_od_2011.csv',
                     'fatal_accidental_od_2012.csv',
                     'fatal_accidental_od_2013.csv',
                     'fatal_accidental_od_2014.csv',
                     'fatal_accidental_od_2015.csv',
                     'fatal_accidental_od_2016.csv']

"""
  :param list_opioid_table : a list of opioid data tables
  :param patient_tables : self defined patient tables
"""
def match_data(output='matched_samples.json'):
    # process opioid table first
    opioid_data_, num_opioid_patients = opi_process.process_opioid_table(list_opioid_table)
    # process patient_table
    patient_data = pd_process.process()
    def get_dob_year(dob_str):
        return dob_str.split('-')[0]
    opioid_data = deepcopy(opioid_data_)
    counter = 0
    for p_id in opioid_data_:
        opioid_patient = opioid_data[p_id]
        similar_patients_ = {k : v for k , v in patient_data.iteritems() \
                             if (v['gender'] == opioid_patient['gender'] or v['gender'].lower() == 'unknown') \
                             and (opioid_patient['race'].lower() == v['race'].lower() \
                                or v['race'].lower() == 'unknown') \
                             and ( v['dob'] != '' and opioid_patient['case_year'] != '' \
                                   and opioid_patient['age'] != '' \
                                   and (abs(int(get_dob_year(v['dob'])) - (int(opioid_patient['case_year']) - int(opioid_patient['age']))) <= 3))}
        similar_patients = similar_patients_.keys()
        if len(similar_patients) == 0: # no similiar patients
            opioid_data.pop(p_id)
            continue
        match_id = random.choice(similar_patients)
        opioid_data[p_id]['id'] = match_id
        for feature in patient_data[match_id]:
            if feature != 'race' and feature != 'gender':
                opioid_data[p_id][feature] = patient_data[match_id][feature]
        patient_data.pop(match_id)
    # file output
    # write into a json file
    with open(output, 'w') as fp:
        fp.write(json.dumps(opioid_data, indent=4))
    # save the matched data into a pickle
    out_pkl = open('matched_data.pkl', 'wb')
    pickle.dump((opioid_data_, patient_data, opioid_data), out_pkl)
    out_pkl.close()
    return opioid_data_, patient_data, opioid_data

if __name__ == "__main__":
    match_data()
