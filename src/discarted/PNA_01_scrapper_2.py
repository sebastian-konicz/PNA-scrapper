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

    file = r'C:\Users\sebas\OneDrive\Pulpit\ZIP\PNA.pdf'
    # official link to the document
    # link = r'https://www.poczta-polska.pl/hermes/uploads/2013/11/spispna.pdf'

    with pdfplumber.open(file) as pdf:
        first_page = pdf.pages[3]
        table = first_page.extract_table()
        print(table)
        im = first_page.to_image()
        im1 = im.draw_rects(first_page.extract_words())
        im2 = im.debug_tablefinder()
        im2.save(r'C:\Users\sebas\OneDrive\Pulpit\PNA-scrapper\data\interim\image.jpg')
        display(Image(im))

    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')

if __name__ == "__main__":
    main()
