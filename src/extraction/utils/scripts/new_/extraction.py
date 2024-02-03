# Example of a mapping configuration for a hypothetical blockchain
from utils.scripts.new_.model import GeneralTransactionModel
from utils.scripts.new_.model import GeneralUTXOModel
from utils.scripts.utils.http_utils import fetch_transactions
from utils.scripts.avalanche.avalanche_model import Avalanche_X_Model, Avalanche_C_Model, Avalanche_P_Model
from utils.scripts.avalanche.avalanche_UTXO_model import AvalancheUTXO
from utils.database.database_service import append_dataframe_to_sql, get_query_results

from datetime import datetime
import pytz
import requests

def extract_data(transaction_feature_mapping, emit_utxo_mapping, consume_utxo_mapping, emitted_utxos_key, consumed_utxos_key, chain, url):
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

        # Map emitted UTXOs
        emitted_utxos.extend([
            map_utxo(emit_utxo_mapping, e_utxo, txHash, txType, blockHash).__dict__ for e_utxo in tx.get(emit_utxo_mapping, [])
        ])

        # Map consumed UTXOs
        consumed_utxos.extend([
            map_utxo(consume_utxo_mapping, c_utxo, txHash, txType, blockHash).__dict__ for c_utxo in tx.get(consume_utxo_mapping, [])
        ])

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
    


def calculate_amount_unlocked(transaction):
    amountUnlocked = transaction.get('amountUnlocked', [])
    
    amount_unlocked = {}
    
    for amount in amountUnlocked:
        if int(amount['denomination']) != 0:
            unlocked_value = int(amount['amount']) / int(amount['denomination'])
        else:
            unlocked_value = int(amount['amount'])

        if amount['name'] in amount_unlocked:
            amount_unlocked[amount['name']] += unlocked_value
        else:
            amount_unlocked[amount['name']] = unlocked_value

    return amount_unlocked

def calculate_amount_created(transaction):
    amountCreated = transaction.get('amountCreated', [])

    amount_created = {}
    
    for amount in amountCreated:
        if int(amount['denomination']) != 0:
            created_value = int(amount['amount']) / int(amount['denomination'])
        else:
            created_value = int(amount['amount'])

        if amount['name'] in amount_created:
            amount_created[amount['name']] += created_value
        else:
            amount_created[amount['name']] = created_value

    return amount_created

# Mapping of function names to actual functions for dynamic invocation
transformation_functions = {
    "calculate_amount_unlocked": calculate_amount_unlocked,
    "calculate_amount_created": calculate_amount_created,
}

if __name__ == "__main__":
    
    c_feature_mapping =  {
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
    
    url = "https://glacier-api.avax.network/v1/networks/mainnet/blockchains/c-chain/transactions"
    
    extract_data(c_feature_mapping, 'c', url)