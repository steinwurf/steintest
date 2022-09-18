import pandas as pd 
import numpy as np
import generatereports.report_settings as rs
import fpdf
from pathlib import Path
from datetime import datetime, timedelta

## Important this file must not be run alone it must be run after generate_historical_data.py


TODAY = datetime.utcnow() 

HISTORICAL_DATA_PATH = Path(__file__).resolve().parents[1] / "historical_data" / "historical_data.csv"
PLOT_FOLDER_PATH = Path(__file__).resolve().parents[1] / "plots" / TODAY.strftime("%Y-%m-%d")


TODAY_STRING = datetime.utcnow().strftime('%m-%d-%Y')
REPORT_NAME = 'report-' + TODAY.strftime("%m-%d-%Y") + '.pdf'
REPORT_PATH = Path(__file__).resolve().parents[1].joinpath( "reports", REPORT_NAME)


def generate_report(row):
    print("Generating report...")
    pdf = rs.PDF()
    pdf.frontpage(row['last_report_date'], row['date'])
    pdf.quick_overview( row['num_tests_since_last_report'], 
                        row['deviation_in_num_of_tests'], 
                        row['num_of_tests_singapore'],
                        row['num_of_tests_new_york'],
                        row['num_of_tests_amsterdam'],
                        PLOT_FOLDER_PATH)
    pdf.geographical_coverage(PLOT_FOLDER_PATH)
    pdf.all_time_overview(PLOT_FOLDER_PATH)
    pdf.Appendix()

    pdf.output(REPORT_PATH , 'F')
    print("successfully generated report")
    print("Report generated at: " + str(REPORT_PATH))



def load_row():
    print("Loading historical data...")
    df = pd.read_csv(HISTORICAL_DATA_PATH)
    df['date'] = pd.to_datetime(df['date'])
    df['last_report_date'] = pd.to_datetime(df['last_report_date'], errors="coerce")
    newest_row = df.loc[df['date'].idxmax()]


    # IF the date is older than one day then the program will fail here
    if abs(newest_row['date'] - TODAY) > timedelta(days=1):
        print("The data is not up to date, please run generate_historical_data.py")
        exit()

    return newest_row

def get_report():
    todays_row = load_row()

    generate_report(
        todays_row,
    ) 


if __name__ == "__main__":
    get_report()


      

