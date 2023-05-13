import pendulum
import pygsheets
import pandas
from datetime import datetime, timedelta
from tempfile import NamedTemporaryFile
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

# Credentials google sheet
gc = pygsheets.authorize(service_account_file='./data/file.json')
sh = gc.open_by_url('your_googlesheet_URL/')

default_args = {
    'owner': 'djamier',
    'depends_on_past': False,
    'start_date': pendulum.datetime(2023, 1, 1, tz="Asia/Jakarta"),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def ingest_from_postgres():
    hook = PostgresHook(postgres_conn_id="postgres_conn")
    conn = hook.get_conn()
    cursor = conn.cursor()
    cursor.execute( """
                    select id, name, job_role from employees 
                    """
                  )

    df = pandas.DataFrame(cursor.fetchall(), columns=["id", "name", "job_role"])
    conn.close()
    return df

def get_last_row_from_gsheet():
    wks = sh[1]
    df_from_gsheet = wks.get_as_df()
    start_row = df_from_gsheet.index[-1]
    return start_row

def insert_data_into_gsheet(df, start_row):
    wks = sh[1]
    wks.set_dataframe(df, start='A{}'.format(start_row), copy_head=False)

def main():
    df = ingest_from_postgres()
    start_row = get_last_row_from_gsheet()
    insert_data_into_gsheet(df, start_row)

with DAG(
    dag_id="postgres_to_gsheet",
    default_args=default_args,
    schedule_interval='0 0 * * *',
    catchup=False
) as dag:

    ingest_data = PythonOperator(
        task_id="ingest_from_postgres",
        python_callable= ingest_from_postgres
    )

    ingest_data