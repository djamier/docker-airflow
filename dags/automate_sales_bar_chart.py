from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import pendulum
import snowflake.connector
import pandas as pd
import streamlit as st
import plotly.express as px

default_args = {
    'owner': 'djamier',
    'depends_on_past': False,
    'start_date': pendulum.datetime(2023, 1, 1, tz="Asia/Jakarta"),
    'retries': 0,
    'retry_delay': timedelta(minutes=10),
}

@st.cache_resource
def get_snowflake_connection():
    conn = snowflake.connector.connect(
        account='ur_account',
        user='ur_user',
        password='ur_pass',
        role='ur_role',
        warehouse='ur_wh',
        database='ur_db',
        schema='ur_schema'
    )
    return conn

def read_query_file():
    with open('/opt/airflow/resources/sales.sql', 'r') as file:
        query = file.read()
    return query

def execute_query(query):
    conn = get_snowflake_connection()
    result = pd.read_sql(query, conn)
    print (result)
    return result

with DAG(
    dag_id='automate_sales_bar_chart',
    default_args=default_args,
    schedule_interval='@once',
    catchup=False
) as dag:
    
    task_read_query_file = PythonOperator(
        task_id='read_query_file',
        python_callable=read_query_file
    )

    task_execute_query = PythonOperator(
        task_id='execute_query',
        python_callable=execute_query,
        op_kwargs = {
            'query': task_read_query_file.output
        }
    )

    task_read_query_file >> task_execute_query