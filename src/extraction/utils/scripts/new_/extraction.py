# Example of a mapping configuration for a hypothetical blockchain

from utils.scripts.utils.http_utils import fetch_transactions
from utils.scripts.avalanche.avalanche_model import Avalanche_X_Model, Avalanche_C_Model, Avalanche_P_Model
from utils.scripts.avalanche.avalanche_UTXO_model import AvalancheUTXO
from utils.database.database_service import append_dataframe_to_sql, get_query_results
from utils.scripts.utils.time_utils import convert_to_gmt_timestamp, get_today_start_gmt_timestamp
from utils.scripts.new_.mappers import map_transaction, map_utxo
from datetime import datetime
import pandas as pd

def extract_data(transaction_feature_mapping, emit_utxo_mapping, consume_utxo_mapping, emitted_utxos_keys, consumed_utxos_keys, chain, url, last_day):
    print(f"{chain} start....")
    last_timestamp = convert_to_gmt_timestamp(last_day)
    current_day = get_today_start_gmt_timestamp()

    page_token = None
    
    params = {
        "pageSize": 100
    }
    
    trxs = []
    emitted_utxos = []
    consumed_utxos = []
    run = True

    while run:
        if page_token:
          params["pageToken"] = page_token
        
        res_data = fetch_transactions(url, params)
        transactions = res_data.get('transactions', [])
        
    for tx in transactions:
        timestamp = int(tx.get(transaction_feature_mapping['timestamp'][0]),0)
        txHash = tx.get(transaction_feature_mapping['txHash'][0],'')
        blockHash = tx.get(transaction_feature_mapping['blockHash'][0],'')
        txType= tx.get(transaction_feature_mapping['txType'][0],'')
        
        # Check if the transaction is before the current day
        if timestamp < current_day:
            # Save data to the database for the day that just completed
            current_date = datetime.fromtimestamp(current_day).strftime("%Y-%m-%d")
            
            df_trx = pd.DataFrame(trxs)
            df_trx['date'] = current_date
            
            df_emitted_utxos = pd.DataFrame(emitted_utxos)
            df_emitted_utxos['date'] = current_date
            
            df_consumed_utxos = pd.DataFrame(consumed_utxos)
            df_consumed_utxos['date'] = current_date
            
            df_trx['date'] = pd.to_datetime(df_trx['date'])
            df_emitted_utxos['date'] = pd.to_datetime(df_emitted_utxos['date'])
            df_consumed_utxos['date'] = pd.to_datetime(df_consumed_utxos['date'])
            
            # print(df_trx)
            append_dataframe_to_sql(f'{chain}_transactions', df_trx)
            append_dataframe_to_sql(f'{chain}_emitted_utxos', df_emitted_utxos)
            append_dataframe_to_sql(f'{chain}_consumed_utxos', df_consumed_utxos)
            # print("x transaction",current_date)
            
            # Move to the previous day
            current_day -= 86400
            trxs = []
            emitted_utxos = []
            consumed_utxos = []
        
        if timestamp <= last_timestamp:
            run = False
            break
        
        # Map the transaction itself (existing logic)
        mapped_transaction = map_transaction(transaction_feature_mapping, tx)
        trxs.append(mapped_transaction.__dict__)

        for key in emitted_utxos_keys:
            if key in tx:
                emitted_utxos.extend([
                    map_utxo(emit_utxo_mapping, e_utxo, txHash, txType, blockHash).__dict__ for e_utxo in tx.get(key, [])
                ])
                break  # Stop after finding the first matching key
        
        # Map consumed UTXOs
        for key in consumed_utxos_keys:
            if key in tx:
                consumed_utxos.extend([
                    map_utxo(consume_utxo_mapping, c_utxo, txHash, txType, blockHash).__dict__ for c_utxo in tx.get(key, [])
                ])
                break  # Stop after finding the first matching key

    return current_date

def store_data(chain, current_date, trxs, emitted_utxos, consumed_utxos):
    if trxs:
        df_trx = pd.DataFrame(trxs)
        df_trx['date'] = pd.to_datetime(current_date)
        append_dataframe_to_sql(f'{chain}_transactions', df_trx)

    if emitted_utxos:
        df_emitted_utxos = pd.DataFrame(emitted_utxos)
        df_emitted_utxos['date'] = pd.to_datetime(current_date)
        append_dataframe_to_sql(f'{chain}_emitted_utxos', df_emitted_utxos)

    if consumed_utxos:
        df_consumed_utxos = pd.DataFrame(consumed_utxos)
        df_consumed_utxos['date'] = pd.to_datetime(current_date)
        append_dataframe_to_sql(f'{chain}_consumed_utxos', df_consumed_utxos)


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
    last_day = "2024-02-01"
    extract_data(x_feature_mapping, x_emit_utxo_mapping, x_consume_utxo_mapping, emitted_utxos_key, consumed_utxos_key, 'x', x_url, last_day)
