# FACT test task

URL = https://dsa.court.gov.ua/dsa/inshe/oddata/511/
Parsing script to download CSV data from URL daily and save it to MySQL database.

Instructions:
* сreate a new virtual environment and clone this repository using git
* in terminal RUN: pip install -r requirements.txt
* to connect the database in mysql_config.py, specify your data
* in terminal RUN: python parser.py



Script with UI for receive a csv file with firm_edrpou column and return a file with the result in which only those numbers that are in the database remain.

Instructions:
* in terminal RUN: python firm_edrpou_checker.py
* click Choose file and select csv file with the column "firm_edrpou"
* wait a few seconds and you will receive a notification about success or failure
* new file will be in the same folder with the same name + (result)
