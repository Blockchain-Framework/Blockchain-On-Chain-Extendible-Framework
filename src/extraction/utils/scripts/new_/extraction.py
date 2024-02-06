# Example of a mapping configuration for a hypothetical blockchain
import os
import sys
sys.path.insert(0, r"D:\Academics\FYP\Repos new\Blockchain-On-Chain-Extendible-Framework\src\extraction")

from utils.scripts.utils.http_utils import fetch_transactions

from utils.scripts.utils.time_utils import convert_to_gmt_timestamp
from utils.scripts.new_.mappers import data_mapper
from utils.scripts.new_.helper import store_data

import pandas as pd

# @keymapper("x")
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
    emitted_utxos = []
    consumed_utxos =[]
    
    run = True
    
    while run:
        if page_token:
          params["pageToken"] = page_token
        
        res_data = fetch_transactions(url, params)
        transactions = res_data.get('transactions', [])
        
        for tx in transactions:
            timestamp = int(tx.get("timestamp"))
            txHash = tx.get('txHash','')
            blockHash = tx.get('blockHash','')
            txType= tx.get(('txType'),'')
            
            print(timestamp, txHash, blockHash, txType)
            
            if timestamp < start_timestamp:
                run = False
                break
            if timestamp < end_timestamp:
                
                # Process the main transaction details
                trxs.append(tx)
                
                # Process emitted UTXOs
                for e_utxo in tx.get('emittedUtxos', []):
                    e_utxo_modified = e_utxo.copy()  
                    e_utxo_modified['txHash'] = txHash
                    e_utxo_modified['blockHash'] = blockHash
                    e_utxo_modified['txType'] = txType
                    # print(e_utxo_modified)
                    # print()
                    emitted_utxos.append(e_utxo_modified)
                
                # Process consumed UTXOs
                for c_utxo in tx.get('consumedUtxos', []):
                    c_utxo_modified = c_utxo.copy()
                    c_utxo_modified['txHash'] = txHash
                    c_utxo_modified['blockHash'] = blockHash
                    c_utxo_modified['txType'] = txType
                    consumed_utxos.append(c_utxo_modified)

        if 'nextPageToken' in res_data:
            page_token = res_data['nextPageToken']
        else:
            run = False
        
    return  trxs, emitted_utxos, consumed_utxos


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

def getAssetId(utxo):
    asset =  utxo['asset']
    return asset.get('assetId')

def getAssetName(utxo):
    asset =  utxo['asset']
    return asset.get('name', '')

def getSymbol(utxo):
    asset =  utxo['asset']
    return asset.get('symbol', '')

def getDenomination(utxo):
    asset =  utxo['asset']
    return asset.get('denomination',0)

def getAsset_type(utxo):
    asset =  utxo['asset']
    return asset.get('type','')

def getAmount(utxo):
    asset =  utxo['asset']
    return asset.get('amount',0)


if __name__ == "__main__":
    # meta_data ={
    #     blockchain
    #     subchain
    #     last_date
    #     description
    #     extraction_function
    #     metrics = [metric_keys]  
    # }
    x_feature_mapping =  {
            'txHash' : ('transactionId',"feature"),
            'blockHash':('blockHash',"feature"),
            'blockHeight': ('blockHeight',"feature"),
            'timestamp':('timestamp',"feature"),
            'memo':('memo',"feature"),
            'chainFormat':('chainFormat','feature'),
            'txType':('txType',"feature"),
            'amountUnlocked': ('amount_unlocked',"function","calculate_amount_unlocked"),
            'amountCreated': ('amount_created',"function", "calculate_amount_created")
        }
    
    x_emit_utxo_mapping = {
        'addresses': ('addresses',"feature"),
        'utxoId': ('utxoId',"feature"),
        'txHash':('txHash',"feature"),
        'txType':('txType',"feature"),
        'assetId': ('assetId',"function", 'getAssetId'),
        'asset_name': ('asset_name',"function", 'getAssetName'),
        'symbol': ('symbol',"function", 'getSymbol'),
        'denomination': ('denomination',"function", 'getDenomination'),
        'asset_type': ('asset_type',"function", 'getAsset_type'),
        'amount': ('amount',"function", 'getAmount')
    }
    
    x_consume_utxo_mapping = {
        'addresses': ('addresses',"feature"),
        'utxoId': ('utxoId',"feature"),
        'txHash':('txHash',"feature"),
        'txType':('txType',"feature"),
        'blockHash':('blockHash',"feature"),
        'assetId': ('assetId',"function", 'getAssetId'),
        'asset_name': ('asset_name',"function", 'getAssetName'),
        'symbol': ('symbol',"function", 'getSymbol'),
        'denomination': ('denomination',"function", 'getDenomination'),
        'asset_type': ('asset_type',"function", 'getAsset_type'),
        'amount': ('amount',"function", 'getAmount')
    }

    transformation_functions = {
        "calculate_amount_unlocked": calculate_amount_unlocked,
        "calculate_amount_created": calculate_amount_created,
    }

    utxo_functions = {
        "getAssetId": getAssetId,
        "getAssetName":getAssetName,
        "getSymbol":getSymbol,
        "getDenomination":getDenomination,
        "getAsset_type":getAsset_type,
        "getAmount":getAmount
    }
    
    x_url = "https://glacier-api.avax.network/v1/networks/mainnet/blockchains/x-chain/transactions"
    
    day = "2024-02-01"

    trxs, emitted_utxos, consumed_utxos = extract_avalanche_data(day)
    
    config = [
        x_feature_mapping,
        x_emit_utxo_mapping,
        x_consume_utxo_mapping,
        transformation_functions,
        utxo_functions
    ]
    trxs, emitted_utxos, consumed_utxos = data_mapper(config, trxs, emitted_utxos, consumed_utxos)
    
    store_data('x', day, trxs, emitted_utxos, consumed_utxos)