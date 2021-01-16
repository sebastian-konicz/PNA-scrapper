from pathlib import Path
import pandas as pd
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
    file_path = r'\data\interim\zipcodes_copy.csv'

    # read dataframe
    zip = pd.read_csv(project_dir + file_path)

    # new column with ZIP code
    zip['PNA_code'] = ""
    # rearanging columns
    zip = zip[['PNA_code', "PNA", 'ADRES', 'WOJ']]
    zip.columns = ["PNA", "CITY", "ADRES", "WOJ"]

    # dropping empty values and filling them with values form previous rows
    zip = zip.ffill(axis=0)

    # extracting zip code to PNA
    zip['PNA'] = zip['CITY'].map(lambda statement: zip_code_extr(statement))

    # dropping zip code from CITY
    zip['CITY'] = zip['CITY'].map(lambda statement: zip_code_remv(statement))

    print(zip.head())

    # saving dataframe
    print("saving files")
    zip.to_csv(project_dir + r'\data\interim\02_zipcodes_clean.csv', index=False, encoding='UTF-8')

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')

# extracting zip-code do PNA
def zip_code_extr(statement):
    pattern_zip = re.compile("([0-9])\w+-([0-9])\w+")
    zip_code = re.search(pattern_zip, statement).group()
    return zip_code

# removing zip-code form CITY
def zip_code_remv(statement):
    pattern_zip = re.compile("([0-9])\w+-([0-9])\w+")

    if type(pattern_zip.search(statement)) == re.Match:
        city = statement.replace(pattern_zip.search(statement).group(), "")

    return city


if __name__ == "__main__":
    main()
