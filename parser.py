import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
from sqlalchemy import create_engine
from mysql_config import MySQL_config


def main():
    while True:
        try:
            # Getting the current .csv link
            url = 'https://dsa.court.gov.ua/dsa/inshe/oddata/511'
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            doc_link = soup.find(class_='d-flex align-items-center h-100').find('a').get('href')
            doc_response = requests.get(doc_link)

            # Getting and adaptation data from a .csv
            csv_text = doc_response.content.decode('utf-8')
            df = pd.read_csv(StringIO(csv_text), sep=None, engine='python')
            df['number'] = pd.to_numeric(df['number'], errors='coerce').fillna(0).astype(int)
            try:
                df['firm_edrpou'] = df['firm_edrpou'].fillna('').astype(str)
                df['firm_edrpou'] = df['firm_edrpou'].str.split(' ').str[-1]
            except:
                pass
            df['firm_edrpou'] = pd.to_numeric(df['firm_edrpou'], errors='coerce').fillna(0).astype(int)

            # Connecting to the database and updating all records
            engine = create_engine(MySQL_config)
            df.to_sql('court_data', engine, if_exists='replace', index=False)
            print('Success !')
        except Exception as e:
            print(e)

        # Waiting for one day
        time.sleep(86400)


if __name__ == "__main__":
    main()
