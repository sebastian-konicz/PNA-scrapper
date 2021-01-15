from pathlib import Path
import pandas as pd
import time
import tabula

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def main():
    # start time of function
    start_time = time.time()

    # project directory
    project_dir = str(Path(__file__).resolve().parents[1])

    file = r'C:\Users\sebas\OneDrive\Pulpit\ZIP\PNA.pdf'
    table1 = tabula.read_pdf(file, pages=3)
    table2 = tabula.read_pdf(file, pages=4)
    table3 = tabula.read_pdf(file, pages=5)

    print("Pierwsza tabela")
    print(table1[0])
    print("Druga tabela")
    print(table2[0])
    print("Trzecia tabela")
    print(table3[0])

    # saving dataframe
    print("saving files")
    table1.to_csv(project_dir + r'\data\interim\Table1.csv', index=False, encoding='UTF-8')
    table2.to_csv(project_dir + r'\data\interim\Table2.csv', index=False, encoding='UTF-8')
    table3.to_csv(project_dir + r'\data\interim\Table3.csv', index=False, encoding='UTF-8')

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')

if __name__ == "__main__":
    main()
