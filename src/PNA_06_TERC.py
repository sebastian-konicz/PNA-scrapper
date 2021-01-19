from pathlib import Path
from bs4 import BeautifulSoup
import os
import re
import requests
import pandas as pd
import time

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def main():
    # start time of function
    start_time = time.time()

    # project directory
    project_dir = str(Path(__file__).resolve().parents[1])

    # gettig the file page with city list
    # site with the actual data in xlsx: https://dane.gov.pl/pl/dataset/188,wykaz-urzedowych-nazw-miejscowosci-i-ich-czesci
    city_list_path = r'\data\raw\city_list.xlsx'
    city_list = pd.read_excel(project_dir + city_list_path, header=1, engine='openpyxl')


    # cleaning data
    # column names
    city_list.columns = ['city', 'type', 'municipality', 'county', 'voivodeship', 'teryt', 'dap', 'remarks',
                         'genitive', 'adjective', 'unnamed_1', 'unnamed_2']

    # dropping unnecessary columns
    city_list.drop(columns=['remarks', 'genitive', 'adjective', 'unnamed_1', 'unnamed_2'], inplace=True)

    # cleaning data
    column_list = ['city', 'type', 'municipality', 'county', 'voivodeship']
    for column in column_list:
        city_list[column] = city_list[column].apply(lambda x: x.replace('\n', ""))
        city_list[column] = city_list[column].apply(lambda x: x.replace('--', "-"))

    # saving dataframe
    print("saving files")
    city_list.to_csv(project_dir + r'\data\interim\03_city_list.csv', index=False, encoding='UTF-8')

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')


def mun_remv(mun):
    word = "gmina "
    if mun.find(word) != -1:
        mun = mun.replace(word, "")
    else:
        pass
    return mun

if __name__ == "__main__":
    main()
