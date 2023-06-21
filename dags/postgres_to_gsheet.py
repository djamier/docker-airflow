import pendulum
import pygsheets
import pandas as pd
import psycopg2
from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
#from airflow.providers.postgres.hooks.postgres import PostgresHook

# Credentials google sheet
gc = pygsheets.authorize(service_account_file='/opt/airflow/resources/file.json')
sh = gc.open_by_url('your_url/')

default_args = {
    'owner': 'djamier',
    'depends_on_past': False,
    'start_date': pendulum.datetime(2023, 1, 1, tz="Asia/Jakarta"),
    'retries': 0,
    'retry_delay': timedelta(minutes=10),
}

def get_postgres_connection():
    conn = psycopg2.connect(
        user='airflow',
        password='airflow',
        host='postgres',
        port=5432,
        database='airflow'
    )
    return conn

def read_query_file():
    with open('/opt/airflow/resources/query.sql', 'r') as file:
        query = file.read()
        print (query)
    return query

def get_last_row_from_gsheet():
    wks = sh[0]
    df_from_gsheet = wks.get_as_df()
    return df_from_gsheet.index[-1] + 3

def create_dataframe (query):
    conn = get_postgres_connection()
    df = pd.read_sql_query(query, conn)
    print (df)
    conn.close()
    return df

with DAG(
    dag_id='postgres_to_gsheet',
    default_args=default_args,
    schedule_interval='0 0 * * *',
    catchup=False
) as dag:
    
    task_read_query_file = PythonOperator(
        task_id='read_query_file',
        python_callable=read_query_file
    )

    task_get_last_row = PythonOperator(
        task_id="get_last_row_from_gsheet",
        python_callable=get_last_row_from_gsheet
    )

    task_create_dataframe = PythonOperator(
        task_id='create_dataframe',
        python_callable= create_dataframe,
        op_kwargs={
            'query': task_read_query_file.output
        }
    )

    task_read_query_file >> task_get_last_row >> task_create_dataframe
