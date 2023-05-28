import pendulum
import pygsheets
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
#from airflow.providers.postgres.hooks.postgres import PostgresHook

# Credentials google sheet
gc = pygsheets.authorize(service_account_file='./resources/file.json')
sh = gc.open_by_url('your_url/')

default_args = {
    'owner': 'djamier',
    'depends_on_past': False,
    'start_date': pendulum.datetime(2023, 1, 1, tz="Asia/Jakarta"),
    'retries': 0,
    #'retry_delay': timedelta(minutes=10),
}

def get_data_from_postgres() -> str:
    conn = create_engine('postgresql+psycopg2://airflow:airflow@postgres/airflow')
    try:
        df = pd.read_sql('select id, name, job_role from public.employees', conn)
        return df
    finally:
        conn.dispose()


def get_last_row_from_gsheet() ->str:
    wks = sh[1]
    df_from_gsheet = wks.get_as_df()
    return df_from_gsheet.index[-1] + 3

def insert_data_into_gsheet(df, start_row :str) ->str:
    wks = sh[1]
    return wks.set_dataframe(df, start='A{}'.format(start_row), copy_head=False)


with DAG(
    dag_id="postgres_to_gsheet",
    default_args=default_args,
    schedule_interval='0 0 * * *',
    catchup=False
) as dag:

    task_get_data = PythonOperator(
        task_id="get_data_from_postgres",
        python_callable= get_data_from_postgres
    )

    task_get_last_row = PythonOperator(
        task_id="get_last_row_from_gsheet",
        python_callable=get_last_row_from_gsheet
    )

    task_insert_data = PythonOperator(
        task_id="insert_data_into_gsheet",
        python_callable=insert_data_into_gsheet,
        op_kwargs={
            'df': task_get_data.output,
            'start_row': task_get_last_row.output
        }
    )

    task_get_data >> task_get_last_row >> task_insert_data