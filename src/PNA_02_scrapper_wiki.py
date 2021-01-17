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

    # gettig the main page with municipality divide table
    main_page = requests.get('https://pl.wikipedia.org/wiki/Lista_gmin_w_Polsce')
    html_main_page = BeautifulSoup(main_page.content, 'html.parser')

    table_body = html_main_page.find("table", class_='sortable wikitable')
    table_rows = table_body.find_all("tr")

    # empty lists for values
    teryt_list = []
    mun_list = []
    pow_list = []
    woj_list = []

    # looping throug tabels on page from page 3 to
    for row in table_rows:
        # headers
        col_head = row.find_all('th')
        # values
        col_boady = row.find_all('td')

        if len(col_head) != 0:
            pass
        else:
            # getting values for specific columns
            teryt = col_boady[0].text.rstrip('\n')
            mun = col_boady[1].text.rstrip('\n')
            pow = col_boady[2].text.rstrip('\n')
            woj = col_boady[3].text.rstrip('\n')
            # appending values to the list
            teryt_list.append(teryt)
            mun_list.append(mun)
            pow_list.append(pow)
            woj_list.append(woj)

    # zipping lists
    data_tuples = list(zip(teryt_list, mun_list, pow_list, woj_list))

    # creating dataframe
    municipalities = pd.DataFrame(data_tuples, columns=["teryt", "municipality", "county", "voivodeship"])

    # removing name "Gmina" from col municipality
    municipalities['municipality'] = municipalities['municipality'].map(lambda mun: mun_remv(mun))

    print(municipalities)

    # saving dataframe
    print("saving files")
    municipalities.to_csv(project_dir + r'\data\interim\02_municipalities.csv', index=False, encoding='UTF-8')

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
