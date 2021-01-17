from pathlib import Path
import pandas as pd
import time
import tabula
import pdfplumber
from IPython.display import Image, display

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def main():
    # start time of function
    start_time = time.time()

    # project directory
    project_dir = str(Path(__file__).resolve().parents[1])

    # file = r'C:\Users\sebas\OneDrive\Pulpit\ZIP\PNA.pdf'
    # official link to the document
    link = r'https://www.poczta-polska.pl/hermes/uploads/2013/11/spispna.pdf'

    # empty table list
    tables_list = []

    # looping throug tabels on page from page 3 to
    for i in range(4, 6):
        table = tabula.read_pdf(link, pages=i)
        table_df = table[0]
        print("table form page {}".format(i))
        # renaming columna
        table_df.columns = ["PNA", "ADRESS", "WOJ"]
        # dropping first row
        table_df = table_df.iloc[1:]
        print(table_df)
        tables_list.append(table_df)

    # concatenating dataframes
    zipcodes = pd.concat(tables_list, axis=0, sort=False)

    # saving dataframe
    print("saving files")
    zipcodes.to_csv(project_dir + r'\data\interim\01_zipcodes.csv', index=False, encoding='UTF-8')

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')

if __name__ == "__main__":
    main()
