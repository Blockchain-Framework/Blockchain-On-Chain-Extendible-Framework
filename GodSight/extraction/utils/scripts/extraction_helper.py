import psycopg2
from GodSight.extraction.utils.database.database_service import batch_insert_dataframes, get_query_results
from GodSight.extraction.utils.database.db import initialize_duck_db
from GodSight.extraction.utils.database.services import delete_existing_records
import pandas as pd
import importlib.util
from sqlalchemy import text


def store_data(chain, current_date, trxs, emitted_utxos, consumed_utxos, config):
    # remove already available records from 3 tables which have given date 
    delete_existing_records(chain, current_date, config)

    if trxs:
        df_trx = pd.DataFrame(trxs)
        df_trx['date'] = pd.to_datetime(current_date)
        df_trx._table_name = f'{chain}_transactions'

    if emitted_utxos:
        df_emitted_utxos = pd.DataFrame(emitted_utxos)
        df_emitted_utxos['date'] = pd.to_datetime(current_date)
        df_emitted_utxos._table_name = f'{chain}_emitted_utxos'

    if consumed_utxos:
        df_consumed_utxos = pd.DataFrame(consumed_utxos)
        df_consumed_utxos['date'] = pd.to_datetime(current_date)
        df_consumed_utxos._table_name = f'{chain}_consumed_utxos'

    batch_insert_dataframes([df_trx, df_emitted_utxos, df_consumed_utxos], config)


def dataframe_to_mapping_dict(df):
    mapping_dict = {}
    for _, row in df.iterrows():
        if row['type'] == 'feature':
            mapping_dict[row['sourcefield']] = (row['targetfield'], 'feature')
        elif row['type'] == 'function':
            mapping_dict[row['sourcefield']] = (row['targetfield'], 'function', row['info'])
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


def get_transaction_mappings(blockchain, subchain, config):
    query = text(f"""
    SELECT * FROM transactions_feature_mappings
    WHERE blockchain = '{blockchain}' AND sub_chain = '{subchain}';
    """)
    return get_query_results(query, config)


def get_emitted_utxo_mappings(blockchain, subchain, config):
    query = text(f"""
    SELECT * FROM emitted_utxos_feature_mappings
    WHERE blockchain = '{blockchain}' AND sub_chain = '{subchain}';
    """)
    return get_query_results(query, config)


def get_consumed_utxo_mappings(blockchain, subchain, config):
    query = text(f"""
    SELECT * FROM consumed_utxos_feature_mappings
    WHERE blockchain = '{blockchain}' AND sub_chain = '{subchain}';
    """)
    return get_query_results(query, config)


# def get_combined_trxs(raw_trxs, raw_emitted_utxos, raw_consumed_utxos, processing_date):
#     conn = initialize_duck_db()
#     # Load the data into DuckDB
#     conn.execute("CREATE TABLE transactions AS SELECT * FROM ?", (raw_trxs,))
#     conn.execute("CREATE TABLE emitted_utxos AS SELECT * FROM ?", (raw_emitted_utxos,))
#     conn.execute("CREATE TABLE consumed_utxos AS SELECT * FROM ?", (raw_consumed_utxos,))
#
#     # Perform the aggregation query
#     result = conn.execute("""
#     SELECT
#         t.*,
#         ARRAY_AGG(DISTINCT cu.addresses) AS inputAddresses,
#         ARRAY_AGG(DISTINCT eu.addresses) AS outputAddresses,
#         SUM(cu.amount) AS inputAmount,
#         SUM(eu.amount) AS outputAmount
#     FROM transactions t
#     LEFT JOIN consumed_utxos cu ON t.txHash = cu.txHash
#     LEFT JOIN emitted_utxos eu ON t.txHash = eu.txHash
#     GROUP BY t.txHash
#     """).fetchall()
#
#     # Convert the result to the desired format and add processing_date
#     final_trxs = [{
#         **row[:len(raw_trxs[0])],  # Transaction fields
#         'inputAddresses': row[-4],
#         'outputAddresses': row[-3],
#         'inputAmount': row[-2],
#         'outputAmount': row[-1],
#         'date': processing_date,  # Add processing date to each transaction
#     } for row in result]
#
#     # Close the DuckDB connection
#     conn.close()
#
#     return final_trxs
