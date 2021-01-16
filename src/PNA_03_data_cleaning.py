from pathlib import Path
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import time
import re

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def main():
    # start time of function
    start_time = time.time()

    # project directory
    project_dir = str(Path(__file__).resolve().parents[1])

    # dataframe with 'dirty' data
    zip_path = r'\data\interim\01_zipcodes.csv'

    # dataframe with 'municipalities data
    mun_path = r'\data\interim\02_municipalities.csv'

    # read dataframes
    zip = pd.read_csv(project_dir + zip_path)
    mun = pd.read_csv(project_dir + mun_path)

    # MUNICIPALITIES DATA
    # list of municipalities (in lovercase)
    mun['municipality'] = mun['municipality'].apply(lambda text: text.lower())
    municipalities = mun["municipality"].tolist()
    # removing duplicates
    municipalities = list(dict.fromkeys(municipalities))
    municipalities.sort()
    print(municipalities)

    # list of counties
    mun['county'] = mun['county'].apply(lambda text: text.lower())
    counties = mun["county"].tolist()
    # removing duplicates
    counties = list(dict.fromkeys(counties))
    counties.sort()
    print(counties)

    # ZIP-CODE DATA
    # new column with ZIP code
    zip['PNA_code'] = ""
    # rearanging columns
    zip = zip[['PNA_code', "PNA", 'ADRESS', 'WOJ']]
    zip.columns = ["PNA", "CITY", "ADRESS", "WOJ"]

    # dropping empty values and filling them with values form previous rows
    zip = zip.ffill(axis=0)

    # PNA - extracting zip code to
    zip['PNA'] = zip['CITY'].map(lambda statement: zip_code_extr(statement))

    # CITY - dropping zip code from
    zip['CITY'] = zip['CITY'].map(lambda statement: zip_code_remv(statement))

    # ADRESS - to lowercase
    zip['ADRESS'] = zip['ADRESS'].apply(lambda text: text.lower())

    # # COU - extracting right municipality
    # zip['COU'] = ""
    # # comapring counties with the counties in ADRESS
    # zip["COU"] = zip.apply(lambda zip: county_match(zip["ADRESS"], counties), axis=1)

    # ADRESS_2 - cleaned column for better municipality association
    zip['ADRESS_2'] = ""
    # strippirng counties from adress column
    zip['ADRESS_2'] = zip.apply(lambda zip: strippping_counties(zip["ADRESS"], zip["COU"]), axis=1)

    # # MUN - extracting right municipality
    # zip['MUN'] = ""
    # # comapring municipalites with the municipalities in ADRESS
    # zip["MUN"] = zip.apply(lambda zip: municip_match(zip["ADRESS_2"], municipalities), axis=1)

    # saving dataframe
    print("saving file")
    zip.to_csv(project_dir + r'\data\interim\02_zipcodes_clean.csv', index=False, encoding='UTF-8')

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

def strippping_counties(text, county):
    if text.find(county) != -1:
        index = text.find(county)
        text = text[: index]
    else:
        pass
    return text

if __name__ == "__main__":
    main()
