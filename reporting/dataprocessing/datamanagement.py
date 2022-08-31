import pandas as pd 
import numpy as np
from datetime import datetime
import queries 

COLUMNS = ["date", "num_tests_since_last_report", "last_report_date"]
INITIAL_RUN = False
TODAY_STRING = datetime.utcnow().strftime('%m-%d-%Y')
TODAY_DATETIME = datetime.utcnow()
TODAY_UNIX_TIME = int(TODAY_DATETIME.timestamp()) * 1000

HISTORICAL_DATA_PATH = "historical_data.csv"
LAST_REPORT_DATETIME = None
LAST_REPORT_STRING = None




def initalize_dataframe():
    df = pd.DataFrame(columns=COLUMNS)
    df.to_csv(HISTORICAL_DATA_PATH, index=False)


def load_dataframe():
    df = pd.read_csv(HISTORICAL_DATA_PATH)
    df['date'] = pd.to_datetime(df['date'])
    set_last_report_date(df)
    return df

def save_dataframe(df):
    df.to_csv(HISTORICAL_DATA_PATH, index=False)

def set_last_report_date(df):
    global LAST_REPORT_DATETIME
    LAST_REPORT_DATETIME = df['date'].max()

    global LAST_REPORT_STRING
    LAST_REPORT_STRING = df['date'].max().strftime('%m-%d-%Y')

    global LAST_REPORT_UNIX_TIME 
    LAST_REPORT_UNIX_TIME = int(LAST_REPORT_DATETIME.timestamp()) * 1000






if __name__ == "__main__":
    if INITIAL_RUN:
        initalize_dataframe()

    df = load_dataframe()
    
    num_tests_since_last_report = queries.get_num_tests_since_last_report(LAST_REPORT_UNIX_TIME)
    print(LAST_REPORT_UNIX_TIME)

    row = {"date": TODAY_DATETIME, "num_tests_since_last_report": num_tests_since_last_report, "last_report_date": LAST_REPORT_DATETIME}
    df = df.append(row, ignore_index=True)

    save_dataframe(df)

