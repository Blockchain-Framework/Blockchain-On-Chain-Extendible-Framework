# Example of a mapping configuration for a hypothetical blockchain
import os
import sys
sys.path.insert(0, r"D:\Academics\FYP\Repos new\Blockchain-On-Chain-Extendible-Framework\src\extraction")

from utils.scripts.utils.http_utils import fetch_transactions
from utils.scripts.avalanche.avalanche_model import Avalanche_X_Model, Avalanche_C_Model, Avalanche_P_Model
from utils.scripts.avalanche.avalanche_UTXO_model import AvalancheUTXO
from utils.database.database_service import append_dataframe_to_sql, get_query_results, batch_insert_dataframes
from utils.scripts.utils.time_utils import convert_to_gmt_timestamp, get_today_start_gmt_timestamp
from utils.scripts.new_.mappers import map_transaction, map_utxo, data_mapper_for_trx_a_day
from datetime import datetime
import pandas as pd


def extract_avalanche_data(date):
    start_timestamp = convert_to_gmt_timestamp(date)
    end_timestamp = start_timestamp + 86400
    url = "https://glacier-api.avax.network/v1/networks/mainnet/blockchains/x-chain/transactions"
    
    print(start_timestamp, end_timestamp)
    page_token = None
    
    params = {
        "pageSize": 100
    }
    
    trxs = []
    run = True
    
    while run:
        if page_token:
          params["pageToken"] = page_token
        
        res_data = fetch_transactions(url, params)
        transactions = res_data.get('transactions', [])
          
        for tx in transactions:
            timestamp = int(tx.get("timestamp"))
            if timestamp < start_timestamp:
                run = False
                break
            if timestamp < end_timestamp:
                trxs.append(tx)
        if 'nextPageToken' in res_data:
            page_token = res_data['nextPageToken']
        else:
            run = False
    return  trxs

def store_data(chain, current_date, trxs, emitted_utxos, consumed_utxos):
    # TODO: Store the data in the database as a batch transaction
    if trxs:
        df_trx = pd.DataFrame(trxs)
        df_trx['date'] = pd.to_datetime(current_date)
        df_trx['_table_name'] = f'{chain}_transactions'
        # append_dataframe_to_sql(f'{chain}_transactions', df_trx)

    if emitted_utxos:
        df_emitted_utxos = pd.DataFrame(emitted_utxos)
        df_emitted_utxos['date'] = pd.to_datetime(current_date)
        df_emitted_utxos['_table_name'] = f'{chain}_emitted_utxos'
        # append_dataframe_to_sql(f'{chain}_emitted_utxos', df_emitted_utxos)

    if consumed_utxos:
        df_consumed_utxos = pd.DataFrame(consumed_utxos)
        df_consumed_utxos['date'] = pd.to_datetime(current_date)
        df_consumed_utxos['_table_name'] = f'{chain}_consumed_utxos'
        # append_dataframe_to_sql(f'{chain}_consumed_utxos', df_consumed_utxos)

   
    batch_insert_dataframes([df_trx,df_emitted_utxos,df_consumed_utxos])

if __name__ == "__main__":
    
    x_feature_mapping =  {
            'txHash' : ('transactionId',"feature"),
            'blockHash' : ('time',"feature"),
            'blockHash':('blockHash',"feature"),
            'blockHeight': ('blockHeight',"feature"),
            'timestamp':('timestamp',"feature"),
            'memo':('memo',"feature"),
            'chainFormat':('chainFormat',"feature"),
            'txType':('txType',"feature"),
            'amountUnlocked': ('amount_unlocked',"function","calculate_amount_unlocked"),
            'amountCreated': ('amount_created',"function", "calculate_amount_created")
        }
    
    x_emit_utxo_mapping = {
        'txType': ('txType',"feature"),
        'addresses': ('addresses',"feature"),
        'value': ('value',"feature"),
        'assetId': ('assetId',"function", 'getAssetId'),
        'asset_name': ('asset_name',"function", 'getAssetName'),
        'symbol': ('symbol',"function", 'getSymbol'),
        'denomination': ('denomination',"function", 'getDenomination'),
        'asset_type': ('asset_type',"function", 'getAsset_type'),
        'amount': ('amount',"function", 'getAmount')
    }
    
    x_consume_utxo_mapping = {
        'txType': ('txType',"feature"),
        'addresses': ('addresses',"feature"),
        'value': ('value',"feature"),
        'assetId': ('assetId',"function", 'getAssetId'),
        'asset_name': ('asset_name',"function", 'getAssetName'),
        'symbol': ('symbol',"function", 'getSymbol'),
        'denomination': ('denomination',"function", 'getDenomination'),
        'asset_type': ('asset_type',"function", 'getAsset_type'),
        'amount': ('amount',"function", 'getAmount')
    }
    
    emitted_utxos_key = ['emittedUtxos',"envInputs"]
    consumed_utxos_key = ['envOutputs','consumedUtxos']

    x_url = "https://glacier-api.avax.network/v1/networks/mainnet/blockchains/c-chain/transactions"
    
    day = "2024-02-01"

    data = extract_avalanche_data(day)

    trxs, emitted_utxos, consumed_utxos = data_mapper_for_trx_a_day(config, data)
    
    store_data('x', "2024-02-04", trxs, emitted_utxos, consumed_utxos)