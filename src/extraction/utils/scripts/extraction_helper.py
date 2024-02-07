from utils.database.database_service import batch_insert_dataframes, get_query_results
import pandas as pd
import importlib.util
from sqlalchemy import text

def store_data(chain, current_date, trxs, emitted_utxos, consumed_utxos):
    # TODO: Store the data in the database as a batch transaction
    if trxs:
        df_trx = pd.DataFrame(trxs)
        df_trx['date'] = pd.to_datetime(current_date)
        df_trx._table_name = f'{chain}_transactions1'
        # append_dataframe_to_sql(f'{chain}_transactions', df_trx)

    if emitted_utxos:
        df_emitted_utxos = pd.DataFrame(emitted_utxos)
        df_emitted_utxos['date'] = pd.to_datetime(current_date)
        df_emitted_utxos._table_name = f'{chain}_emitted_utxos1'
        # append_dataframe_to_sql(f'{chain}_emitted_utxos', df_emitted_utxos)

    if consumed_utxos:
        df_consumed_utxos = pd.DataFrame(consumed_utxos)
        df_consumed_utxos['date'] = pd.to_datetime(current_date)
        df_consumed_utxos._table_name = f'{chain}_consumed_utxos1'
        # append_dataframe_to_sql(f'{chain}_consumed_utxos', df_consumed_utxos)
    
    batch_insert_dataframes([df_trx,df_emitted_utxos,df_consumed_utxos])


def dataframe_to_mapping_dict(df):
    mapping_dict = {}
    for _, row in df.iterrows():
        if row['type'] == 'feature':
            mapping_dict[row['source_field']] = (row['target_field'], 'feature')
        elif row['type'] == 'function':
            mapping_dict[row['source_field']] = (row['target_field'], 'function', row['info'])
    return mapping_dict

def extract_function_names(df):
    # Filter the DataFrame to include only rows where the type is 'function'
    functions_df = df[df['type'] == 'function']
    # Extract the 'info' column which contains the function names
    function_names = functions_df['info'].tolist()
    return function_names


def get_function(file_path, function_name):
    spec = importlib.util.spec_from_file_location("module.name", file_path)
    function_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(function_module)
    return getattr(function_module, function_name, None)  # Returns None if the function does not exist

def load_functions_from_file(file_path, function_names):
    functions = {}
    for name in function_names:
        func = get_function(file_path, name)
        if func:
            functions[name] = func
    return functions

def get_transaction_mappings(blockchain, subchain):
    query = text(f"""
    SELECT * FROM transactions_feature_mappings
    WHERE blockchain = '{blockchain}' AND subchain = '{subchain}';
    """)
    return get_query_results(query)

def get_emitted_utxo_mappings(blockchain, subchain):
    query = text(f"""
    SELECT * FROM emitted_utxos_feature_mappings
    WHERE blockchain = '{blockchain}' AND subchain = '{subchain}';
    """)
    return get_query_results(query)

def get_consumed_utxo_mappings(blockchain, subchain):
    query = text(f"""
    SELECT * FROM consumed_utxos_feature_mappings
    WHERE blockchain = '{blockchain}' AND subchain = '{subchain}';
    """)
    return get_query_results(query)