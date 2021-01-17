from pathlib import Path
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import time
import re
import numpy as np

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def main():
    # start time of function
    start_time = time.time()

    # project directory
    project_dir = str(Path(__file__).resolve().parents[1])

    # dataframe with 'dirty' data
    zip_path = r'\data\interim\01_zipcodes_test.csv'

    # dataframe with 'municipalities data
    mun_path = r'\data\interim\02_municipalities.csv'

    # read dataframes
    zip = pd.read_csv(project_dir + zip_path, sep=',')
    mun = pd.read_csv(project_dir + mun_path, sep=',')

    # MUNICIPALITIES DATA
    mun["concat"] = mun.apply(lambda mun: (mun["municipality"] + " " + mun["county"]).lower(), axis=1)
    concat = mun["concat"].tolist()
    concat = list(dict.fromkeys(concat))
    concat.sort()

    # # list of municipalities (in lovercase)
    # mun['municipality'] = mun['municipality'].apply(lambda text: text.lower())
    # municipalities = mun["municipality"].tolist()
    # # removing duplicates
    # municipalities = list(dict.fromkeys(municipalities))
    # municipalities.sort()
    # print(municipalities)

    # # list of counties
    # mun['county'] = mun['county'].apply(lambda text: text.lower())
    # counties = mun["county"].tolist()
    # # removing duplicates
    # counties = list(dict.fromkeys(counties))
    # counties.sort()
    # print(counties)

    # ZIP-CODE DATA
    # dropping empty values and filling them with values form previous rows
    zip['PNA'].fillna(axis=0, method='ffill', inplace=True)
    zip['ADRESS'].fillna(axis=0, method='ffill', inplace=True)
    zip['WOJ'].fillna(axis=0, method='ffill', inplace=True)
    print("saving file")
    # print(zip)
    zip.to_csv(project_dir + r'\data\interim\02_zipcodes_clean_1.csv', index=False, encoding='UTF-8')

    # new column with ZIP code
    zip['PNA_code'] = ""
    # rearanging columns
    zip = zip[['PNA_code', "PNA", 'ADRESS', 'WOJ']]
    zip.columns = ["PNA", "CITY", "ADRESS", "WOJ"]

    # PNA - extracting zip code to
    zip['PNA'] = zip['CITY'].map(lambda statement: zip_code_extr(statement))

    # CITY - dropping zip code from
    zip['CITY'] = zip['CITY'].map(lambda statement: zip_code_remv(statement))

    # ADRESS - to lowercase
    zip['ADRESS'] = zip['ADRESS'].apply(lambda text: text.lower())

    # CONCAT - extracting right municipality and county
    zip['CONCAT'] = ""
    # comapring counties with the counties in ADRESS
    zip["CONCAT"] = zip.apply(lambda zip: concat_match(zip["ADRESS"], concat), axis=1)

    # CONCAT - extracting municipalites / county with too long names
    # extracting counties with names longer than 20 characters
    mun['county_length'] = mun.apply(lambda mun: len(mun['county']), axis=1)
    county_long = mun[mun['county_length'] >= 20].copy()
    county_long["concat"] = county_long.apply(lambda cl: (cl["municipality"] + " " + cl["county"]).lower(), axis=1)
    county_long = county_long['concat'].tolist()
    county_long = list(dict.fromkeys(county_long ))
    county_long.sort()
    # comapring long counties with the counties in ADRESS
    zip["CONCAT_LONG"] = zip.apply(lambda zip: county_long_match(zip["ADRESS"], county_long), axis=1)

    # MUN_COU - creating one column with municipality and county
    zip['MUN_COU'] = zip.apply(
        lambda zip: zip['CONCAT']
        if zip['CONCAT'] != ""
        else zip['CONCAT_LONG'], axis=1)

    print(zip['MUN_COU'])
    # filling missing values in municipality and county column
    zip['MUN_COU'] = zip.apply(lambda zip: zip['MUN_COU'].replace(r'^\s*$', np.nan, regex=True), axis=1)
    zip['MUN_COU'].fillna(axis=0, method='ffill', inplace=True)

    # # dropping unnecessary columns
    # zip.drop(columns=['CONCAT', 'CONCAT_LONG'], inplace=True)

    # ADRESS_2 - cleaned column for better municipality association
    zip['ADRESS_2'] = ""
    # strippirng counties from adress column
    zip['ADRESS_2'] = zip.apply(lambda zip: strippping_concat(zip['ADRESS'], zip['MUN_COU']), axis=1)

    # # COU - extracting right municipality
    # zip['COU'] = ""
    # # comapring counties with the counties in ADRESS
    # zip["COU"] = zip.apply(lambda zip: county_match(zip["ADRESS"], counties), axis=1)

    # # MUN - extracting right municipality
    # zip['MUN'] = ""
    # # comapring municipalites with the municipalities in ADRESS
    # zip["MUN"] = zip.apply(lambda zip: municip_match(zip["ADRESS_2"], municipalities), axis=1)

    # saving dataframe
    print("saving file")
    zip.to_csv(project_dir + r'\data\interim\02_zipcodes_clean_2.csv', index=False, encoding='UTF-8')

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')

# extracting zip-code do PNA
def zip_code_extr(statement):
    pattern_zip = re.compile("([0-9])\w+-([0-9])\w+")
    zip_code = ''
    if type(pattern_zip.search(statement)) == re.Match:
        zip_code = re.search(pattern_zip, statement).group()
    else:
        pass
    return zip_code

# removing zip-code form CITY
def zip_code_remv(statement):
    pattern_zip = re.compile("([0-9])\w+-([0-9])\w+")
    city = ''
    if type(pattern_zip.search(statement)) == re.Match:
        city = statement.replace(pattern_zip.search(statement).group(), "")
    else:
        pass
    return city

# finding match for municipality in ADRESS_2 column
def concat_match(text, concat):
    result = ''
    for con in concat:
        ratio = fuzz.partial_ratio(text, con)
        if (ratio == 100) & (len(con) <= len(text)):
            print(len(con))
            print(len(text))
            print(text)
            print(con)
            print(ratio)
            result = con
        else:
            pass
    return result

# finding match for municipality in ADRESS_2 for the counties that are longer than 19 characters
def county_long_match(text, county_long):
    result = ''
    for county in county_long:
        ratio = fuzz.partial_ratio(county, text)
        if (ratio == 100) & (len(text) > 12):
            print(text)
            print(county)
            print(ratio)
            result = county
        else:
            pass
    return result

# # finding match for municipality in ADRESS_2 column
# def municip_match(text, municipalities):
#     result = ''
#     for mun in municipalities:
#         ratio = fuzz.partial_ratio(text, mun)
#         if (ratio == 100) & (len(mun) <= len(text)):
#             # print(len(mun))
#             # print(len(text))
#             # print(text)
#             # print(mun)
#             # print(ratio)
#             result = mun
#         else:
#             pass
#     return result

# # finding match for county in ADRESS column
# def county_match(text, counties):
#     result = ''
#     for cou in counties:
#         ratio = fuzz.partial_ratio(text, cou)
#         if (ratio == 100):
#             # print(text)
#             # print(cou)
#             # print(ratio)
#             result = cou
#         else:
#             pass
#     return result

def strippping_concat(text, concat):
    if (text.find(concat) != -1) & (concat != ''):
        index = text.find(concat)
        text = text[:index]
    elif concat == '':
        text = text
    return text

if __name__ == "__main__":
    main()
