from pathlib import Path
import pandas as pd
from fuzzywuzzy import fuzz
import time
import numpy as np

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def main():
    # start time of function
    start_time = time.time()

    # project directory
    project_dir = str(Path(__file__).resolve().parents[1])

    # dataframe with 'dirty' data
    # zip_path = r'\data\interim\04_zipcodes_clean_test.csv'
    zip_path = r'\data\interim\04_zipcodes_clean.csv'

    # dataframe with 'municipalities data
    mun_path = r'\data\interim\02_municipalities.csv'

    # read dataframes
    zip = pd.read_csv(project_dir + zip_path, sep=',')
    mun = pd.read_csv(project_dir + mun_path, sep=',')

    # COUNTIES THAT HAVE CHANGED ITS NAME - FIXING THE MISTAKES
    # counties that have changed its name
    counties_changed = mun[mun["county"] == 'karkonoski[a]'].copy()
    counties_changed["county"] = "jeleniogórski"
    counties_changed["concat"] = counties_changed.apply(lambda cc: (cc["municipality"] + " " + cc["county"]).lower(), axis=1)
    concat = counties_changed["concat"].tolist()
    concat = list(dict.fromkeys(concat))
    concat.sort()

    # comapring counties that changed name with the counties in ADRESS
    zip["CONCAT"] = zip.apply(lambda zip: concat_match(zip["ADRESS"], concat)
                              if zip["ADRESS"].find('jeleniogórski') != -1
                              else zip['CONCAT'], axis=1)
    # MUN_COU - creating one column with municipality and county
    zip['MUN_COU'] = zip.apply(
        lambda zip: zip['CONCAT']
        if str(zip['CONCAT']).find('jeleniogórski') != -1
        else zip['MUN_COU'], axis=1)

    # strippirng counties that changed name from adress column
    zip['ADRESS_2'] = zip.apply(lambda zip: strippping_concat(zip['ADRESS'], zip['MUN_COU'])
                                if str(zip['MUN_COU']).find('jeleniogórski') != -1
                                else zip['ADRESS_2'], axis=1)

    # COUNTIES WITH TOO LONG NAMES - FIXING THE ADRESS 2 COLUMN
    # extracting counties with names longer than 20 characters
    mun['county_length'] = mun.apply(lambda mun: len(mun['county']), axis=1)
    county_long = mun[mun['county_length'] >= 20].copy()
    county_long["concat"] = county_long.apply(lambda cl: (cl["municipality"] + " " + cl["county"]).lower(), axis=1)
    county_long = county_long['concat'].tolist()
    county_long = list(dict.fromkeys(county_long ))
    county_long.sort()
    county_long_list = []
    for county in county_long:
        if county.find('-') != -1:
            split_list  = county.split('-')
            county_long_list.append(split_list[0])
            county_long_list.append(split_list[1])
        else:
            split_list = county.split(' ')
            county_long_list.append(split_list[0])
            county_long_list.append(split_list[1])
    county_long_list = list(dict.fromkeys(county_long_list))
    county_long_list.sort()

    zip["CONCAT"].replace('', np.nan)
    concat = zip[zip["CONCAT"].isnull()]

    zip['ADRESS_2'] = zip.apply(lambda zip: strippping_adress(zip["ADRESS"], county_long_list)
                                if (pd.isna(zip["CONCAT"]) == True)
                                else zip["ADRESS_2"], axis=1)

    # dropping unnecessary columns
    zip.drop(columns=["CONCAT", 'CONCAT_LONG'], inplace=True)

    # MUNICIPALITIES AND COUNTIES - GETTING THE RIGHT NAMES
    # filling empty values with nan and then copy the previous value
    zip["MUN_COU_2"] = zip["MUN_COU"]
    zip["MUN_COU_2"].replace('', np.nan)
    zip['MUN_COU_2'].fillna(axis=0, method='ffill', inplace=True)
    # print(zip["MUN_COU_2"])

    # ADRES_3 - GETTING FULL ADRESS FOR ROWS THAT ARE SPLITED
    zip["MUN_COU"].replace('', np.nan)
    # crating new column
    zip["ADRESS_3"] = zip["ADRESS_2"]

    # getting rid off adress data in empty / duplicated rows
    zip["ADRESS_2"] = zip.apply(lambda zip: np.nan
                                if (pd.isna(zip["MUN_COU"]) == True)
                                else zip["ADRESS_2"], axis=1)

    zip['ADRESS_2'].replace('', np.nan)
    zip['ADRESS_2'].fillna(axis=0, method='ffill', inplace=True)

    zip["ADRESS_4"] = zip.apply(lambda zip: zip['ADRESS_2'] + " " + zip['ADRESS_3']
                                if (pd.isna(zip["MUN_COU"]) == True)
                                else zip["ADRESS_3"], axis=1)

    # dropping unnecessary columns
    zip.drop(columns=["ADRESS", 'ADRESS_2', 'ADRESS_3'], inplace=True)

    zip["PNA"].replace('', np.nan)
    zip["CITY"].replace('', np.nan)
    zip['PNA'].fillna(axis=0, method='ffill', inplace=True)
    zip['CITY'].fillna(axis=0, method='ffill', inplace=True)

    # renaming columns
    zip = zip.rename(columns={'PNA': 'pna', 'CITY': 'city', 'WOJ': 'voivodeship', 'MUN_COU': 'mun_cou_old',
                              'MUN_COU_2': 'mun_cou', 'ADRESS_4': 'adress'})

    # rearanging dataframe
    zip = zip[['pna', 'city', 'adress', 'mun_cou', 'voivodeship', 'mun_cou_old']]

    # ASSIGNING CORRECT MUNICIPALITIES AND COUNTIES FROM MUNICIPALITY DATAFRAME
    mun = mun[['municipality', 'county']]
    mun['mun_cou'] = mun.apply(lambda mun: (mun["municipality"] + " " + mun["county"]).lower(), axis=1)
    zip_merge = zip.merge(mun, how='inner', left_on='mun_cou', right_on='mun_cou', sort=False)

    # rearanging dataframe
    zip_merge = zip_merge[['pna', 'city', 'adress', 'municipality', 'county', 'voivodeship', 'mun_cou']]

    # dropping duplicate values
    zip_merge.drop_duplicates(keep='first', inplace=True)

    # saving dataframe
    print("saving file")
    zip.to_csv(project_dir + r'\data\interim\05_zipcodes_clean.csv', index=False, encoding='UTF-8')
    zip_merge.to_csv(project_dir + r'\data\interim\05_zipcodes_clean_merge.csv', index=False, encoding='UTF-8')

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')

# finding match for municipality in ADRESS_2 column
def concat_match(text, concat):
    result = ''
    for con in concat:
        ratio = fuzz.partial_ratio(text, con)
        if (ratio == 100) & (len(con) <= len(text)):
            result = con
        else:
            pass
    return result

def strippping_concat(text, concat):
    if (text.find(concat) != -1) & (concat != ''):
        index = text.find(concat)
        text = text[:index]
    elif concat == '':
        text = text
    return text

def strippping_adress(text, county_long_list):
    new_text = ''
    for county in county_long_list:
        if (text.find(county) != -1):
            index = text.find(county)
            text = text[:index]
            new_text = text
        else:
            new_text = text
    return new_text

if __name__ == "__main__":
    main()
