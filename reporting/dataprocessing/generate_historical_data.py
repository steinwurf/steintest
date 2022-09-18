import pandas as pd 
import numpy as np
from datetime import datetime
import dataprocessing.queries as q
from pathlib import Path


## IMPORTANT to notice that these file are not 100% changeable, so if you add a server this file will need to be updated

SERVERS = ["Singapore", "New_York", "Amsterdam"]
CONTINENTS = ["Asia", "Europe", "North_America", "South_America", "Oceania", "Africa"]
EXPLICIT_COLUMNS = ["date", "num_tests_since_last_report", "last_report_date", "deviation_in_num_of_tests"]
INITIAL_RUN = False
TODAY_STRING = datetime.utcnow().strftime('%m-%d-%Y')
TODAY_DATETIME = datetime.utcnow()
TODAY_UNIX_TIME = int(TODAY_DATETIME.timestamp()) * 1000



DATA_FOLDER = Path(__file__).resolve().parents[1] / "historical_data"
HISTORICAL_DATA_PATH = DATA_FOLDER.joinpath("historical_data.csv")
LAST_REPORT_DATETIME = None
LAST_REPORT_STRING = None
LAST_REPORT_UNIX_TIME = None

def create_columns():
    columns_continent = [f"num_of_tests_{continent.lower()}" for continent in CONTINENTS]
    columns_server = [f"num_of_tests_{server.lower()}" for server in SERVERS]
    columns = EXPLICIT_COLUMNS + columns_server + columns_continent
    return columns


def initalize_dataframe():
    df = pd.DataFrame(columns=create_columns())
    df.to_csv(HISTORICAL_DATA_PATH, index=False)


def load_dataframe():
    df = pd.read_csv(HISTORICAL_DATA_PATH)

    if not INITIAL_RUN:
        df['date'] = pd.to_datetime(df['date'])
    
    set_last_report_date(df)
    
    return df

def save_dataframe(df):
    df.to_csv(HISTORICAL_DATA_PATH, index=False)

def set_last_report_date(df):
    global LAST_REPORT_DATETIME

    if not INITIAL_RUN:
        LAST_REPORT_DATETIME = df['date'].max()

        global LAST_REPORT_STRING
        LAST_REPORT_STRING = df['date'].max().strftime('%m-%d-%Y')

        global LAST_REPORT_UNIX_TIME 
        LAST_REPORT_UNIX_TIME = int(LAST_REPORT_DATETIME.timestamp()) * 1000
    else:
        LAST_REPORT_DATETIME = 0

def calculate_deviation_from_last_report(df, num_tests_since_last_report):
    if INITIAL_RUN:
        return None

    last_report_num_tests = df[df['date'] == LAST_REPORT_DATETIME]['num_tests_since_last_report'].values[0]
    
    if last_report_num_tests == 0:
        return None

    deviation = (num_tests_since_last_report - last_report_num_tests) / last_report_num_tests * 100

    return round(deviation, 2)


def generate_historical_data():
    if INITIAL_RUN:
            initalize_dataframe()

    df = load_dataframe()
    
    num_tests_since_last_report = q.get_num_tests_since_last_report(LAST_REPORT_UNIX_TIME)

    num_tests_per_server = q.get_num_tests_per_server(LAST_REPORT_UNIX_TIME, SERVERS)

    deviation_in_num_of_tests = calculate_deviation_from_last_report(df, num_tests_since_last_report)

    num_tests_per_continent = q.get_num_tests_per_continent(LAST_REPORT_UNIX_TIME, CONTINENTS)

    row = { "date": TODAY_DATETIME, 
            "num_tests_since_last_report": num_tests_since_last_report, 
            "last_report_date": LAST_REPORT_DATETIME,
            "deviation_in_num_of_tests": deviation_in_num_of_tests, 
            **num_tests_per_server,
            **num_tests_per_continent}
    df = df.append(row, ignore_index=True)

    save_dataframe(df)





if __name__ == "__main__":

    generate_historical_data()

