# data_storage_service.py
import pandas as pd
from sqlalchemy import create_engine

def store_data(dataframe, file_path, db_connection_string):
    # Store as .tsv.gz
    dataframe.to_csv(file_path, sep='\t', index=False, compression='gzip')
    
    # Store to PostgreSQL
    engine = create_engine(db_connection_string)
    dataframe.to_sql('avalanche_data', engine, if_exists='replace', index=False)
