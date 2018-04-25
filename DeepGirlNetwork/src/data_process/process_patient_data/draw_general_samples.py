import pickle
import numpy as np
import feature_extraction as fe

""" source : https://www.census.gov/quickfacts/fact/table/alleghenycountypennsylvania/PST045216 """
CURR_YEAR = 2015
# gender
FEMALE_PERCENT = 0.517 # 4327
# MALE = 0.483 # 3134
# age
# BELOW_18 = 0.189 # 0
OVER_65_PERCENT = 0.18 # 4353
# OTHER = 0.631 # 3108
OTHER = 0.82
# race
WHITE = 0.805 # 3184
BLACK = 0.134 # 2294
ASIAN = 0.037 # 1244
# OTHER = 0.024 # 739

def draw_general_sample(num_samples, modified_patient_data, feature='gender', percent=[FEMALE_PERCENT]):
    # check if num_samples is reasonable
    if num_samples > len(modified_patient_data):
        print('data points collected fewer than required!')
        return None
    # check if the feature categories and given number of percentages is correct
    if not ((feature.lower() == 'gender' and len(percent) == 1) \
        or (feature.lower() == 'age' and len(percent) == 1) \
        or (feature.lower() == 'race' and len(percent) == 3)):
        print('unmatched percentage!')
        return None
    # add age
    _add_age(modified_patient_data)
    # draw samples
    if feature.lower() == 'gender':
        FEMALE_PERCENT = percent[0]
        # group patient data
        female_need = int(num_samples * FEMALE_PERCENT)
        male_need = int(num_samples * (1 - FEMALE_PERCENT)) 
        female_group, male_group = _split_gender(modified_patient_data)
        # get id
        fp_id = np.random.choice(list(female_group.keys()), female_need)
        mp_id = np.random.choice(list(male_group.keys()), female_need)
        # get sample
        sample_chosen = {k : v for k, v in modified_patient_data.iteritems() if k in fp_id or k in mp_id}
    elif feature.lower() == 'age':
        OVER_65_PERCENT = percent[0]
        # group patient data
        elder_need = int(num_samples * OVER_65_PERCENT)
        adult_need = int(num_samples * (1 - OVER_65_PERCENT))
        adult, elder = _split_age(modified_patient_data)
        # get id
        ap_id = np.random.choice(list(adult.keys()), elder_need)
        ep_id = np.random.choice(list(elder.keys()), adult_need)
        # get sample
        sample_chosen = {k : v for k, v in modified_patient_data.iteritems() if k in ap_id or k in ep_id}
    elif feature.lower() == 'race':
        WHITE = percent[0]
        BLACK = percent[1]
        ASIAN = percent[2]
        OTHER = 1 - WHITE - BLACK - ASIAN
        # group patient data
        white_need = int(num_samples * WHITE)
        black_need = int(num_samples * BLACK)
        asian_need = int(num_samples * ASIAN)
        other_need = int(num_samples * OTHER)
        white, black, asian, other = _split_race(modified_patient_data)
        # get id
        w_id = np.random.choice(list(white.keys()), white_need)
        b_id = np.random.choice(list(black.keys()), black_need)
        a_id = np.random.choice(list(asian.keys()), asian_need)
        o_id = np.random.choice(list(other.keys()), other_need)
        # get sample
        sample_chosen = {k : v for k, v in modified_patient_data.iteritems() if k in w_id or k in b_id or k in a_id or k in o_id}
    return sample_chosen

def _add_age(modified_patient_data):
    for pid in modified_patient_data:
        data = modified_patient_data[pid]
        birth_year = int(data['dob'].split('-')[0])
        data['age'] = int(CURR_YEAR - birth_year)

def _split_gender(modified_patient_data):
    female_group = {}
    male_group = {}
    for pid in modified_patient_data:
        data = modified_patient_data[pid]
        if data['gender'].lower() == 'female':
            female_group[pid] = data
        elif data['gender'].lower() == 'male':
            male_group[pid] = data
        elif np.random.randint(2): # Unknown case
            female_group[pid] = data
        else:
            male_group[pid] = data
    return female_group, male_group

def _split_age(single_group):
    adult = {}
    elder = {}
    for pid in single_group:
        data = single_group[pid]
        if data['age'] > 65:
            elder[pid] = data
        else:
            adult[pid] = data
    return adult, elder

def _split_race(single_group):
    white = {}
    black = {}
    asian = {}
    other = {}
    for pid in single_group:
        data = single_group[pid]
        if data['race'].lower() == 'white':
            white[pid] = data
        elif data['race'].lower() == 'black':
            black[pid] = data
        elif data['race'].lower() == 'asian':
            asian[pid] = data
        else:
            other[pid] = data
    return white, black, asian, other

if __name__ == "__main__":
    draw_general_sample(2000)

