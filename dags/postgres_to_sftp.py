import csv
import logging
import pendulum
from datetime import datetime, timedelta
from tempfile import NamedTemporaryFile
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.sftp.operators.sftp import SFTPOperator

default_args = {
    'owner': 'djamier',
    'depends_on_past': False,
    'start_date': pendulum.datetime(2023, 1, 1, tz="Asia/Jakarta"),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

now = datetime.now(pendulum.timezone('Asia/Jakarta'))
now2 = now.strftime('%Y%m%d')

def ingest_from_postgres():
    #getdata dari postgres dan convert ke format csv
    hook = PostgresHook(postgres_conn_id="postgres_conn")
    conn = hook.get_conn()
    cursor = conn.cursor()
    cursor.execute(""" select 
                      id, name, job_role
                      from employees """)
    with open(f"dags/test.csv", "w") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(cursor)
        f.flush()
        cursor.close()
        conn.close()
        logging.info("Saved file: %s", f"dags/test_{now2}.csv")


with DAG(
    dag_id="postgres_to_sftp",
    default_args=default_args,
    schedule_interval='0 0 * * *',
    catchup=False
) as dag:

    ingest_data = PythonOperator(
        task_id="ingest_from_postgres",
        python_callable= ingest_from_postgres
    )

    upload_file = SFTPOperator(
        task_id="put-file",
        ssh_conn_id="ssh-conn", #nama bucket
        remote_filepath=f"namafolder/test_{now2}.csv", #folder dalam bucket
        local_filepath=f"dags/test_{now2}.csv", #folder dari local airflow
        operation="put"
    )
    
    ingest_data >> upload_file
