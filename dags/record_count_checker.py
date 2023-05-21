from sqlalchemy import create_engine, text
import pandas as pd
import os

username = os.getenv ('username')
password = os.getenv ('password')
hostname = os.getenv ('hostname')

def get_dir_path() ->str:
    path = './resources/query.sql'
    return path

def read_file() ->str:
    path = get_dir_path()
    with open(path, 'r') as file:
        query = file.read()
    return query

def execute_query_source(query :str) -> str: 
    source_conn = create_engine(f'postgresql+psycopg2://{username}:{password}@{hostname}:5435/source')
    conn = source_conn.connect() #open connection
    execute_query = conn.execute(text(query))
    record_count = execute_query.fetchone()[0]
    conn.close() #close connection
    return record_count

def execute_query_destination(query :str) -> str:
    destination_conn = create_engine(f'postgresql+psycopg2://{username}:{password}@{hostname}:5435/destination')
    conn = destination_conn.connect() #open connection
    execute_query = conn.execute(text(query))
    record_count = execute_query.fetchone()[0]
    conn.close() #close connection
    return record_count

def main():
    query = read_file()
    record_count_source = execute_query_source(query)
    record_count_destination = execute_query_destination(query)
    print (f'record di table source total {record_count_source} row')
    print (f'record di table destination total {record_count_destination} row')

if __name__ == '__main__':
    main()

