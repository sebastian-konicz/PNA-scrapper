from pathlib import Path
from bs4 import BeautifulSoup
import os
import re
import requests
import pandas as pd
import time
import numpy as np

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def main():
    # start time of function
    start_time = time.time()

    # project directory
    project_dir = str(Path(__file__).resolve().parents[1])

    # gettig the file with TERC data
    # site with the actual data in csv: https://eteryt.stat.gov.pl/eTeryt/rejestr_teryt/udostepnianie_danych/baza_teryt/uzytkownicy_indywidualni/pobieranie/pliki_pelne.aspx?contrast=default
    terc_path = r'\data\raw\TERC_Urzedowy_2021-01-19.csv'
    terc = pd.read_csv(project_dir + terc_path, sep='\t', header=0, encoding='latin')

    # data clean up
    # renaming columns
    terc = terc.rename(columns={'WOJ': 'voivodeship', 'POW': 'county', 'GMI': 'municipality',
                              'RODZ': 'type', 'NAZWA': 'name'})
    # dropping unnecessary columns
    terc.drop(columns=["NAZWA_DOD", 'STAN_NA'], inplace=True)

    # chaniging special characters in dataframe
    dictionary = {'¥': 'Ą', '¹': 'ą', 'Æ': 'Ć', 'Ê': "Ę", 'ê': 'ę',  '£': "Ł", '³': 'ł',  "Ñ": 'Ń', 'ñ': 'ń',
                  "": "Ś", '\x9c': 'ś',  '¯': 'Ż', '¿': 'ż', '': 'ż'}

    # replacing special letters in columns:
    for special_letter, normal_letter in dictionary.items():
            terc['name'] = terc['name'].apply(lambda value: value.replace(special_letter, normal_letter))

    # replacing NaN values with blanks
    terc['county'].replace(np.nan, '')
    terc['municipality'].replace(np.nan, '')
    terc['type'].replace(np.nan, '')
    terc['county'].fillna(axis=0, value="", inplace=True)
    terc['municipality'].fillna(axis=0, value="", inplace=True)
    terc['type'].fillna(axis=0, value="", inplace=True)

    # changing datatypes in columns county and municipality
    terc['county'] = terc['county'].apply(lambda terc: str(int(terc)) if terc != "" else terc)
    terc['municipality'] = terc['municipality'].apply(lambda terc: str(int(terc)) if terc != "" else terc)
    terc['type'] = terc['type'].apply(lambda terc: str(int(terc)) if terc != "" else terc)

    # changin value to get correct TERC code
    terc_code_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    columns_list = ['voivodeship', 'county', 'municipality']
    for number in terc_code_list:
        for column in columns_list:
            terc[column] = terc[column].apply(lambda terc: '0' + str(terc) if str(terc) == number else str(terc))

    # getting voivodeship names
    voivodeship = terc[terc['county'] == ""].copy()
    voivodeship['name'] = voivodeship['name'].apply(lambda v: v.lower())
    voivodeship = voivodeship[['voivodeship', 'name']]
    voi = voivodeship['voivodeship'].tolist()
    voi_name = voivodeship['name'].tolist()
    voivodeship_dict = dict(zip(voi, voi_name))

    # getting county names
    county = terc[terc['municipality'] == ""].copy()
    county = county.drop(county[county['county'] == ""].index)
    county['name'] = county['name'].apply(lambda v: v.lower())
    county['voi_cou'] = county.apply(lambda cou: cou['voivodeship'] + cou['county'], axis=1)
    county = county[['voi_cou', 'name']]
    cou = county['voi_cou'].tolist()
    cou_name = county['name'].tolist()
    county_dict = dict(zip(cou, cou_name))

    # restricting dataframe
    terc = terc[terc['county'] != ""]
    terc = terc[terc['municipality'] != ""]
    terc = terc[(terc['type'] != "4") & (terc['type'] != "5")]

    # new column for computation
    terc['voi_cou'] = terc.apply(lambda terc: terc['voivodeship'] + terc['county'], axis=1)

    # adding voivodeship
    terc['voivodeship_name'] = ""
    for voi_number, voi_name in voivodeship_dict.items():
        terc['voivodeship_name'] = terc.apply(
            lambda terc: voi_name
            if terc['voivodeship'] == voi_number
            else terc['voivodeship_name'], axis=1)

    # adding voivodeship
    terc['county_name'] = ""
    for cou_number, cou_name in county_dict.items():
        terc['county_name'] = terc.apply(
            lambda terc: cou_name
            if terc['voi_cou'] == cou_number
            else terc['county_name'], axis=1)

    # TERC column for computation
    terc['terc'] = terc.apply(lambda terc: str(terc['voivodeship'] + terc['county'] + terc['municipality'] + terc['type']), axis=1)

    # reshaping columns
    terc = terc[['terc', 'name', 'county_name', 'voivodeship_name']]

    # renaming columns
    terc = terc.rename(columns={'name': 'municipality', 'county_name': 'county', 'voivodeship_name': 'voivodeship'})

    # saving dataframe
    print("saving files")
    terc.to_csv(project_dir + r'\data\interim\06_terc.csv', index=False, encoding='UTF-8')

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')

if __name__ == "__main__":
    main()
