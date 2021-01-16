# PNA-scrapper
Lightweigth scraper for extractin polish ZIP codes from the official PNA document created by Polish Postal Office

The aim of this project is gather in one place all the programs used by NOC NORDIC SO team.
# NORDIC BAU SOprog production tool


Before running or changing code please read [Confluence documentation](https://adlm.nielsen.com/confluence/display/NPI/Denmark)

To run program with GUI please run <b>'SOprog.py'</b> file.

If there are any problems with GUI you can also run single program separately.
To do this please go to the bottom of the script and execute below code:

```
if __name__=='__main__':
    print("__main__")
    main()
```

Also remember to provide proper values for period, country, etc.

## Getting started
To get started make sure you have Git, Github and enviroment for programming language of your choice downloaded and connected.

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
There are exemplary input and output files in their respective folders. They are used as templates and should not be deleted.

## Authors
Sebastian Konicz - sebastian.konicz@nielsen.com
Grzegorz Laskowski - grzegorz.laskowski@nielsen.com
Wojciech Piotrowski - wojciech.piotrowski@nielsen.com

## Project Organization <a id="project"></a>
------------

    +-- build              <- ?
    +-- dist               <- ?
    +-- IMG                <- Folder with images for the window application.
    +-- old scripts        <- Folder containg all old scripts (do not delete - program might stop working)
    +-- src                <- Source code for use in this project.
	¦   ¦
    ¦   +-- __init__.py    				<- Makes src a Python module
	¦   ¦
	¦   +-- _databases                              <- Folder with scripts neded for conecting to database
    ¦   ¦ 	+-- db_madras.py        		<- Script connecting to MADRAS database
    ¦   ¦ 	+-- db_madras_c19
    ¦   ¦   +-- db_sirval.py
	¦   ¦
	¦   +-- _main          				<- Folder with main scripts for window application
    ¦   ¦   +-- master_file.py			<- File conataining constants, path etc.
	¦   ¦
    ¦   +-- a_production           			<- Scripts concerning input production and checks
	¦   ¦	¦
    ¦   ¦ 	+-- a_preproduction       		<- Preproduction programs.
	¦   ¦	¦   +-- Cells_Denamrk.py
	¦   ¦   ¦   +-- HiiDenmark.py
	¦   ¦	¦
    ¦   ¦ 	+-- b_input_creation        	        <- Input creation files for all countries.
	¦   ¦	¦   +-- CellIndustry2.py
	¦   ¦	¦   +-- CharSample.py
	¦   ¦	¦   +-- MUS.py
	¦   ¦	¦   +-- New_Shops.py
	¦   ¦	¦   +-- ShopIndustry.py
	¦   ¦   ¦   +-- ShopSample.py
	¦   ¦	¦
    ¦   ¦ 	+-- c_checks     			<- Checks
	¦   ¦	¦   +-- LegacyACV.py
	¦   ¦   ¦   +-- LegacyCells.py
	¦   ¦	¦
    ¦   ¦ 	+-- d_c19            			<- C19 additional programs
	¦   ¦	    +-- CausalCellWire.py
	¦   ¦ 	    +-- NonCensusCellWire.py 
    ¦   ¦
    ¦   +-- b_postproduction           		<- Scripts concerning post-production tasks and checks
	¦   ¦	¦
    ¦   ¦ 	+-- CheckRFE.py       			<- RFE check.
	¦   ¦	¦   +-- CheckRFE.py.py
	¦   ¦	¦   +-- CheckRFE_DK.py.py
	¦   ¦	¦   +-- CheckRFE_NO.py.py
	¦   ¦   ¦   +-- CheckRFE_SE.py
	¦   ¦	¦
    ¦   ¦ 	+-- Estimation.py       		<- Estimation check.
	¦   ¦	¦   +-- Estimation_1.py
	¦   ¦	¦   +-- Estimation_1_NO.py
	¦   ¦	¦   +-- Estimation_2.py
	¦   ¦	¦   +-- Estimation_2_DK.py
	¦   ¦	¦   +-- Estimation_2_NO.py
	¦   ¦   ¦   +-- Estimation_2_SE.py
	¦   ¦	¦
    ¦   ¦ 	+-- SirparStorelist        		<- SirparStorelist checks
	¦   ¦	¦   +-- SirparStorelist_DK.py
	¦   ¦	¦   +-- SirparStorelist_NO.py
	¦   ¦   ¦   +-- SirparStorelist_SE.py
	¦   ¦	¦
    ¦   ¦ 	+-- KPI_CSSI.py
	¦   ¦ 	+-- RS_sample_and_uni.py
    ¦   ¦   +-- scrap_net.py
    ¦   ¦
    ¦   +-- c_other         			<- Other useful programs
	¦   ¦ 	+-- Causal_sample_selection.py
	¦   ¦ 	+-- KPI_CSSI.py
    ¦   ¦   +-- out_of_uni.py
    ¦   ¦
    ¦   +-- d_not_classified         		<- Work in progress scripts or files for deletion
    ¦   ¦
    ¦   +-- inputs         			        <- Input template files (not used)
    ¦   ¦
    ¦   +-- outputs  			        <- Output template files (not used)
    ¦  
    +-- .gitignore.py      <- File for excluding other files and folders from BitBucket repo
    +-- .gitignore.py      <- ?
 	+-- Eforte.py          <- eForte check (can't be moved due to dependecies)
    +-- LegacyMBDs.py      <- LegacyMBDs check (can't be moved due to dependecies)
 	+-- README.md          <- The top-level README for developers using this project.
    +-- requirements.txt   <- File with all necessary packages
    +-- SOprog.py          <- MAIN APPLICATION¦
    +-- TracebackLog       <- ?     					<- ?


--------