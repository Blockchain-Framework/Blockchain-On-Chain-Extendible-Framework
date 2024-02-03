# Example of a mapping configuration for a hypothetical blockchain
from utils.scripts.new_.model import GeneralTransactionModel
from utils.scripts.new_.model import GeneralUTXOModel
from utils.scripts.utils.http_utils import fetch_transactions
from utils.scripts.avalanche.avalanche_model import Avalanche_X_Model, Avalanche_C_Model, Avalanche_P_Model
from utils.scripts.avalanche.avalanche_UTXO_model import AvalancheUTXO
from utils.database.database_service import append_dataframe_to_sql, get_query_results
from utils.scripts.utils.time_utils import convert_to_gmt_timestamp, get_today_start_gmt_timestamp
from utils.scripts.new_.helper import calculate_amount_unlocked, calculate_amount_created
from datetime import datetime

def extract_data(transaction_feature_mapping, emit_utxo_mapping, consume_utxo_mapping, emitted_utxos_keys, consumed_utxos_keys, chain, url):
    print("x start....")
    last_timestamp = convert_to_gmt_timestamp(last_day)
    current_day = get_today_start_gmt_timestamp()

    page_token = None

    params = {
        "pageSize": 100
    }

    url = "https://glacier-api.avax.network/v1/networks/mainnet/blockchains/x-chain/transactions"
    
    trxs = []
    emitted_utxos = []
    consumed_utxos = []
    run = True

    while run:
        if page_token:
          params["pageToken"] = page_token
        
        res_data = fetch_transactions(url, params)
        transactions = res_data.get('transactions', [])
    
    transformed_data_list = []
    
    for tx in transactions:
        timestamp = int(tx.get(transaction_feature_mapping['timestamp'][0]),0)
        txHash = tx.get(transaction_feature_mapping['txHash'][0],'')
        blockHash = tx.get(transaction_feature_mapping['blockHash'][0],'')
        txType= tx.get(transaction_feature_mapping['txType'][0],'')
        
        # Check if the transaction is before the current day
        if timestamp < current_day:
            # Save data to the database for the day that just completed
            current_date = datetime.fromtimestamp(current_day).strftime("%Y-%m-%d")
        
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

    return transformed_data_list

def map_utxo(feature_mapping, utxo, txHash, txType, blockHash):
    transformed_data = {
        'txHash': txHash,
        'txType': txType,
        'blockHash': blockHash
    }
    
    for general_attr, details in feature_mapping.items():
        api_attr, attr_type = details[:2]
        if attr_type == "feature":
            transformed_data[general_attr] = utxo.get(api_attr)
        elif attr_type == "function":
            function_name = details[2]
            if function_name in transformation_functions:
                transformed_data[general_attr] = transformation_functions[function_name](utxo)
    
    GeneralUTXOModel(**transformed_data)
    
def map_transaction(blockchain_feature_mapping,tx):
    transformed_data = {}
    for general_attr, details in blockchain_feature_mapping.items():
        api_attr, attr_type = details[:2]
        
        if attr_type == "feature":
            transformed_data[general_attr] = tx.get(api_attr)
        elif attr_type == "function":
            function_name = details[2]
            if function_name in transformation_functions:
                transformed_data[general_attr] = transformation_functions[function_name](tx)
    
    GeneralTransactionModel(**transformed_data)
    


# Mapping of function names to actual functions for dynamic invocation
transformation_functions = {
    "calculate_amount_unlocked": calculate_amount_unlocked,
    "calculate_amount_created": calculate_amount_created,
}

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
            'amountUnlocked': ('amount_unlocked',"function","function name"),
            'amountCreated': ('amount_created',"function", "function name")
        }
    
    x_emit_utxo_mapping = {
        'txType': ('txType',"feature"),
        'addresses': ('addresses',"feature"),
        'value': ('value',"feature"),
        'assetId': ('assetId',"feature"),
        'asset_name': ('asset_name',"feature"),
        'symbol': ('symbol',"feature"),
        'denomination': ('denomination',"feature"),
        'asset_type': ('asset_type',"feature"),
        'amount': ('amount',"feature")
    }
    
    x_consume_utxo_mapping = {
        'txType': ('txType',"feature"),
        'addresses': ('addresses',"feature"),
        'value': ('value',"feature"),
        'assetId': ('assetId',"feature"),
        'asset_name': ('asset_name',"feature"),
        'symbol': ('symbol',"feature"),
        'denomination': ('denomination',"feature"),
        'asset_type': ('asset_type',"feature"),
        'amount': ('amount',"feature")
    }
    emitted_utxos_key = ['emittedUtxos',"envInputs"]
    consumed_utxos_key = ['envOutputs','consumedUtxos']

    x_url = "https://glacier-api.avax.network/v1/networks/mainnet/blockchains/c-chain/transactions"
    
    extract_data(x_feature_mapping, x_emit_utxo_mapping, x_consume_utxo_mapping, emitted_utxos_key, consumed_utxos_key, 'x', x_url)
