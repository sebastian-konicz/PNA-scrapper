from pathlib import Path
import pandas as pd
import time
import camelot
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
    # link = r'https://www.poczta-polska.pl/hermes/uploads/2013/11/spispna.pdf'

    file = "http://lab.fs.uni-lj.si/lasin/wp/IMIT_files/neural/doc/seminar8.pdf"
    tables = camelot.read_pdf(file, pages='12')
    print(tables[0].df)

    # pages with zip code table 3 -
    table_start = camelot.read_pdf(file, pages=3)
    table_middle_1 = camelot.read_pdf(file, pages=14)
    table_middle_2 = camelot.read_pdf(file, pages=100)
    table_middle_3 = camelot.read_pdf(file, pages=824)
    table_end = camelot.read_pdf(file, pages=1648)

    print("first table")
    print(table_start[0].head())
    print("middle table 1")
    print(table_middle_1[0].head())
    print("middle table 2")
    print(table_middle_2[0].head())
    print("middle table 3")
    print(table_middle_3[0].head())
    print("last table")
    print(table_end[0].head())


    table_start = table_start[0]
    table_middle_1 = table_middle_1[0]
    table_middle_2 = table_middle_2[0]
    table_middle_3 = table_middle_3[0]
    table_end = table_end[0]

    # saving dataframe
    print("saving files")
    table_start.to_csv(project_dir + r'\data\interim\0_table_start.csv', index=False, encoding='UTF-8')
    table_middle_1.to_csv(project_dir + r'\data\interim\1_table_middle_1.csv', index=False, encoding='UTF-8')
    table_middle_2.to_csv(project_dir + r'\data\interim\1_table_middle_2.csv', index=False, encoding='UTF-8')
    table_middle_3.to_csv(project_dir + r'\data\interim\1_table_middle_3.csv', index=False, encoding='UTF-8')
    table_end.to_csv(project_dir + r'\data\interim\2_table_end.csv', index=False, encoding='UTF-8')

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')

if __name__ == "__main__":
    main()
