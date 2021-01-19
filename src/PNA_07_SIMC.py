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

    # gettig the file with SIMC data
    # site with the actual data in csv: https://eteryt.stat.gov.pl/eTeryt/rejestr_teryt/udostepnianie_danych/baza_teryt/uzytkownicy_indywidualni/pobieranie/pliki_pelne.aspx?contrast=default
    terc_path = r'\data\raw\SIMC_Urzedowy_2021-01-19.csv'
    simc = pd.read_csv(project_dir + terc_path, sep=';', header=0, encoding='latin')

    # data clean up
    # renaming columns
    simc = simc.rename(columns={'ï»¿WOJ': 'voi_no', 'POW': 'cou_no', 'GMI': 'mun_no', 'RODZ_GMI': 'mun_typ_no', 'RM': 'rm',
                                'MZ': 'mz', 'NAZWA': 'city', 'SYM': 'sym', 'SYMPOD': 'sympod'})
    # dropping unnecessary columns
    simc.drop(columns=['STAN_NA'], inplace=True)

    # chaniging special characters in dataframe
    dictionary = {'¥': 'Ą', 'Ä': 'ą', 'Ä': 'Ć', 'Ê': "Ę", 'Ä': 'ę',  'Å': "Ł", 'Å': 'ł',  "Ñ": 'Ń', 'Å': 'ń',
                  'Ã³': 'ó', 'asdf': 'Ó', "Å": "Ś", 'Å': 'ś',  'Å»': 'Ż', 'Å¼': 'ż', 'Å¹': "Ź", 'Åº': 'ż'}

    # replacing special letters in columns:
    for special_letter, normal_letter in dictionary.items():
            simc['city'] = simc['city'].apply(lambda value: value.replace(special_letter, normal_letter))

    # changing datatypes in columns county and municipality
    simc['voi_no'] = simc['voi_no'].apply(lambda simc: str(int(simc)))
    simc['cou_no'] = simc['cou_no'].apply(lambda simc: str(int(simc)))
    simc['mun_no'] = simc['mun_no'].apply(lambda simc: str(int(simc)))
    simc['mun_typ_no'] = simc['mun_typ_no'].apply(lambda simc: str(int(simc)))

    # changin value to get correct TERC code
    terc_code_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    columns_list = ['voi_no', 'cou_no', 'mun_no']
    for number in terc_code_list:
        for column in columns_list:
            simc[column] = simc[column].apply(lambda terc: '0' + str(terc) if str(terc) == number else str(terc))

    # TERC column for computation
    simc['terc'] = simc.apply(
        lambda simc: str(simc['voi_no'] + simc['cou_no'] + simc['mun_no'] + simc['mun_typ_no']), axis=1)

    # reshaping dataframe columns
    simc = simc[['terc', 'city', 'rm', 'mz', 'sym', 'sympod']]

    # saving dataframe
    print("saving files")
    simc.to_csv(project_dir + r'\data\interim\07_simc.csv', index=False, encoding='UTF-8')

    # loading terc file
    terc_path = r'\data\interim\06_terc.csv'
    terc = pd.read_csv(project_dir + terc_path, sep=',', header=0, encoding='UTF-8')
    terc = terc.astype({"terc": object})

    # loading simc file
    simc_path = r'\data\interim\07_simc.csv'
    simc = pd.read_csv(project_dir + simc_path, sep=',', header=0, encoding='UTF-8')
    simc = simc.astype({"terc": object})

    simc_merge = simc.merge(terc, how='inner', left_on='terc', right_on='terc', sort=False)

    # reshaping dataframe columns
    simc_merge = simc_merge[['terc', 'city', 'municipality', 'county', 'voivodeship', 'rm', 'mz', 'sym', 'sympod']]
    print(simc_merge.head())

    # saving dataframe
    print("saving files")
    simc_merge.to_csv(project_dir + r'\data\interim\07_simc_merge.csv', index=False, encoding='UTF-8')

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')

if __name__ == "__main__":
    main()
