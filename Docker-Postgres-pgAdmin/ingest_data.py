import os
import argparse
from time import time
import pandas as pd
from sqlalchemy import create_engine
import logging
logging.basicConfig(level=logging.INFO)


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    csv_file = 'output.csv'

    #download the csv
    logging.info('Downloading the file')
    os.system(f"wget {url} -O {csv_file} --no-check-certificate")
    logging.info('INFO: Finished file download')
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}") #creating an engine to 

    logging.info("INFO: Reading the csv")
    df_iter = pd.read_csv('output.csv', iterator=True,chunksize=100000, engine='python')
    df = next(df_iter)

    logging.info('INFO: Inserting into table...........')
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    df.to_sql(name=table_name, con=engine, if_exists='append')

    while True:
        t_start = time()
        df = next(df_iter)
        df.to_sql(name=table_name, con=engine, if_exists='append')
        t_end = time()
        print('Inserted another chunk, took %.3f seconds' %(t_end-t_start))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Ingest CSV data to Postgres")

    #user, password, host, port, database name, table name, url of thr csv

    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of table where we will write results to')
    parser.add_argument('--url', help='url of the csv file')


    args = parser.parse_args()
    main(args)


