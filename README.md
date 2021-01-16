# PNA-scrapper
Lightweigth scraper for extracting polish ZIP codes from the official **[PNA document](https://www.poczta-polska.pl/hermes/uploads/2013/11/spispna.pdf)** created by Polish Postal Office.data

The aim of this project is create dataset with all zip codes in Poland along with the info about city, municipality, county and voivodeship.

## Running program
To create dataset simply run PNA_00_main.py script in src folder. You can also run each script separately.
To do this please go to the bottom of the script and execute below code:

```
if __name__=='__main__':
    print("__main__")
    main()
```

## Getting started
To get started make sure you have Git, GitHub and environment for programming language of your choice downloaded and connected.

Clone the repository to your local machine and explore the scripts.

```
git clone https://github.com/sebastian-konicz/PNA-scrapper.git
```

## Requirements
The required version of Python for the current release is 3.9.

### Prerequisities
Run the code below:

```
pip install -r requirements.txt
```
Remember that if you add any library to your project scripts you MUST add them to **requirements.txt**

### Input/Output folders
There are exemplary input and output files in respective data folders.

## Authors
Sebastian Konicz - sebastian.konicz@gmail.com

## Project Organization <a id="project"></a>
------------

    +-- data               <- Folder with all necessary data
    ¦   ¦
    ¦   +-- __init__.py                     <- Makes src a Python module
    ¦   ¦
    +-- notebook           <-
    ¦   ¦
    +-- src                <- Source code for use in this project.
	¦   ¦
    ¦   +-- __init__.py    				    <- Makes src a Python module
	¦   ¦
	¦   +-- PNA_OO_main.py         	        <- Folder with code executing all scripts
	¦   ¦
    ¦   +-- PNA_01_scrapper_postal.py       <-
	¦   ¦
    ¦   +-- PNA_02_scrapper_wiki.py       	<-
 	¦   ¦
    ¦   +-- PNA_03_data_cleaning.py         <-
    ¦   ¦
    ¦   +-- PNA_04_.py           	        <-
    ¦   ¦
    ¦   +-- PNA_05_.py         			    <-
    ¦   ¦
    ¦   +-- PNA_06_.py         	            <-
    ¦  
    +-- .gitignore.py      <- File for excluding other files and folders from GitHub repo
    ¦
    +-- LICENSE            <- ?
    ¦
 	+-- README.md          <- The top-level README for developers using this project.
    ¦
    +-- requirements.txt   <- File with all necessary packages


--------