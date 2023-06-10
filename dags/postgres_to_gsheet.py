import pendulum
import pygsheets
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
 
gc = pygsheets.authorize(service_account_file='./resources/file.json')
sh = gc.open_by_url('your_url/')

def get_connection():
    conn = create_engine('postgresql+psycopg2://djamier:djamier@localhost:5435/postgres')
    return conn

def read_query_file():
    with open('./resources/query.sql', 'r') as file:
        query = file.read()
    return query

def execute_query(query, conn):
    df = pd.read_sql(query, conn)
    return df

def get_last_row_from_gsheet(sheet_name):
    wks = gc.open_by_url(sh).worksheet_by_title(sheet_name)
    df_from_gsheet = wks.get_as_df()
    return df_from_gsheet.index[-1] + 3

def insert_data_into_gsheet(df, sheet_name, start_row):
    wks = gc.open_by_url(sh).worksheet_by_title(sheet_name)
    return wks.set_dataframe(df, start='A{}'.format(start_row), copy_head=False)

def main():
    conn = get_connection()
    query = read_query_file()
    start_row = get_last_row_from_gsheet(sh)
    df = execute_query(query, conn)
    print(df)
    insert_data_into_gsheet(df, sh, start_row)


if __name__ == '__main__':
    main()