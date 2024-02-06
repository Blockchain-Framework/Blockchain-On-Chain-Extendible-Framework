from utils.database.database_service import batch_insert_dataframes
import pandas as pd

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
