import pickle
import match_data as md
import opioid_data_process as opi_process
import patient_data_process as pd_process
import numpy as np

IDC_10_NUM = 22
num_rank = 6
pickle_file_name = 'matched_data.pkl'

def extract_features(matched_data, is_general=False):
    # encoding features 
    matched_data_list = matched_data.values()
    general_features = ['lang', 'marital_status', 'gender', 'race']
    # general feature encoding
    feature_cats, feature_encodings = _general_encoding(matched_data_list, general_features)

    # DIAGNOSE 2 d list
    diagnose_encodings = _encode_diagnose(matched_data_list)
    # TODO: encode admissions as a discounted num days in hospital

    # ENCODE ALL IN THIS ORDER:
    # age, poverty
    # lang, marital_status, gender, race (categorical), diagnose
    def is_int(s):
        try: 
            int(s)
            return True
        except ValueError:
            return False
    all_encodings = []
    for i in range(len(matched_data_list)):
        data = matched_data_list[i]
        p_encoding = [float(data['age']), float(data['poverty'])]
        for feature in general_features:
            p_encoding.append(feature_encodings[feature][i])
        p_encoding.extend(diagnose_encodings[i])
        all_encodings.append(p_encoding)

    # encoding target/doses
    if is_general:
        target_encoding = _encode_non_oddeath_target(matched_data)
    else:
        _, target_encoding = _encode_dose_target(matched_data_list, matched_data)
    return all_encodings, target_encoding 

def _encode_non_oddeath_target(general_data):
    all_encodings = []
    for data in general_data:
        d_cats = [0 for i in range(num_rank + 2)]
        d_cats[-1] = 1
        all_encodings.append(d_cats)
    return all_encodings

def _encode_dose_target(matched_data_list, matched_data):
    all_kinds, selected, percentage = opi_process.sort_important_doses(num_rank, [matched_data])
    all_encodings = []
    for data in matched_data_list:
        d_cats = [0 for i in range(len(selected) + 2)]
        doses = data['doses']
        for d in doses:
            if not d in selected:
                d_cats[len(selected)] = 1
            else:
                d_cats[selected.index(d)] = 1
        all_encodings.append(d_cats)
    return selected, all_encodings

def _general_encoding(matched_data_list, features_list):
    # generate features categories
    all_features_cats = {}
    for feature in features_list:
        all_features_cats[feature] = []
    for data in matched_data_list:
        for feature in features_list:
            certain_feature = data[feature]
            if not certain_feature in all_features_cats[feature]:
                all_features_cats[feature].append(certain_feature)
    # encode feature categories
    all_features_res = {}
    for feature in features_list:
        all_features_res[feature] = []
    for data in matched_data_list:
        for feature in features_list:
            certain_feature = data[feature]
            all_features_res[feature].append(all_features_cats[feature].index(certain_feature))
    return all_features_cats, all_features_res

def _encode_diagnose(matched_data_list):
    # encode directly according to ICD-10
    res = []
    def encode_icd_10(icd_str):
        fst = icd_str.split('.')[0]
        fst_letter = fst[0]
        snd_letter_val = int(fst[1])
        if fst_letter == 'A' or fst_letter == 'B':
            return 0
        elif fst_letter == 'C' or (fst_letter == 'D' and snd_letter_val < 5):
            return 1
        elif fst_letter < 'S':
            return ord(fst_letter) - ord('A')
        elif fst_letter == 'S' or fst_letter == 'T':
            return 18
        elif fst_letter == 'V' or fst_letter == 'Y':
            return 19
        elif fst_letter == 'Z':
            return 20
        else:
            return 21
    for data in matched_data_list:
        p_diag_all_cats = [0 for i in range(IDC_10_NUM)]
        diag = data['diagnose']
        for d in diag:
            d_code = encode_icd_10(d)
            p_diag_all_cats[d_code] += 1
        res.append(p_diag_all_cats)
    return res

if __name__ == "__main__":
    pkl_file = open(pickle_file_name, 'rb')
    _, _, matched_data = pickle.load(pkl_file)
    pkl_file.close()
    all_encodings, target_encoding = extract_features(matched_data, False)
