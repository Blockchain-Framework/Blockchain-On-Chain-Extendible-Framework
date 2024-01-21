import pandas as pd
import requests
import time
from datetime import datetime, timedelta, timezone
import json

import os
import sys
sys.path.insert(0, 'D:\\Academics\\FYP\\Repos\\Blockchain-On-Chain-Extendible-Framework')

from src.utils.http_utils import fetch_transactions
from src.blockchain.avalanche.avalanche_model import Avalanche_X_Model, Avalanche_C_Model, Avalanche_P_Model
from src.blockchain.avalanche.avalanche_UTXO_model import AvalancheUTXO
from src.services.data_storage_service import append_dataframe_to_sql

from datetime import datetime
import pytz

def convert_to_gmt_timestamp(date_str):
    # Define the GMT timezone
    gmt = pytz.timezone('GMT')

    # Parse the date string
    dt_naive = datetime.strptime(date_str, "%Y-%m-%d")

    # Localize the date to GMT
    dt_gmt = gmt.localize(dt_naive)

    # Convert to Unix timestamp
    timestamp = int(dt_gmt.timestamp())

    return timestamp


def get_today_start_gmt_timestamp():
    # Define the GMT timezone
    gmt = pytz.timezone('GMT')

    # Get the current time in GMT
    now_gmt = datetime.now(gmt)

    # Set the time to the start of the day (midnight)
    start_of_today_gmt = now_gmt.replace(hour=0, minute=0, second=0, microsecond=0)

    # Convert to Unix timestamp
    timestamp = int(start_of_today_gmt.timestamp())

    return timestamp

def extract_x_chain_data(last_day):
    
    last_timestamp = convert_to_gmt_timestamp(last_day)
    current_day = get_today_start_gmt_timestamp()

    page_token = None

    params = {
        "pageSize": 100
    }

    url = "https://glacier-api.avax.network/v1/networks/mainnet/blockchains/x-chain/transactions"
    
    data = []
    emitted_utxos = []
    consumed_utxos = []
    run = True

    while run:
        
        if page_token:
          params["pageToken"] = page_token

        res_data = fetch_transactions(url, params)
        transactions = res_data.get('transactions', [])

        for tx in transactions:
            timestamp = int(tx.get("timestamp"))

            # Check if the transaction is before the current day
            if timestamp < current_day:
                # Save data to the database for the day that just completed
                current_date = current_day.strftime("%Y-%m-%d")
                
                df_trx = pd.DataFrame(data)
                df_trx['date'] = current_date
                df_emitted_utxos = pd.DataFrame(emitted_utxos)
                df_emitted_utxos['date'] = current_date
                df_consumed_utxos = pd.DataFrame(consumed_utxos)
                df_consumed_utxos['date'] = current_date
                
                append_dataframe_to_sql('x_transactions', df_trx)
                append_dataframe_to_sql('x_emitted_utxos', df_emitted_utxos)
                append_dataframe_to_sql('x_consumed_utxos', df_consumed_utxos)
                
                # Move to the previous day
                current_day -= 86400
                data = []
                emitted_utxos = []
                consumed_utxos = []

            if timestamp <= last_timestamp:
                run = False
                break
            
            txHash = tx.get("txHash")
            blockHash = tx.get("blockHash")
            txType=tx.get("txType")
            amount_unlocked, amount_created = calculate_x_transaction_values(tx)

            avalanche_tx = Avalanche_X_Model(
                txHash=txHash,
                blockHash=blockHash,
                blockHeight = tx.get("blockHeight"),
                timestamp=timestamp,
                memo=tx.get("memo"),
                chainFormat=tx.get("chainFormat"),
                txType=txType,
                amountUnlocked = amount_unlocked,
                amountCreated = amount_created
            )
            
            # emmitted UTXOs
            for e_utxo in tx.get('emittedUtxos', []):
                
                asset =  e_utxo['asset']
                
                emit_utxo = AvalancheUTXO(
                        txHash = txHash,
                        txType = txType,
                        blockHash = blockHash,
                        addresses = e_utxo['addresses'],
                        utxoId= e_utxo['utxoId'],
                        assetId = asset.get('assetId'),
                        asset_name = asset.get('name', ''),
                        symbol = asset.get('symbol', ''),
                        denomination = asset.get('denomination',0),
                        asset_type = asset.get('type',''),
                        amount = asset.get('amount',0)
                    )
                
                emitted_utxos.append(emit_utxo.__dict__)
            
            # consumed UTXOs
            for c_utxo in tx.get('consumedUtxos', []):
                
                asset =  c_utxo['asset']
                
                commit_utxo = AvalancheUTXO(
                        txHash = txHash,
                        txType = txType,
                        blockHash = blockHash,
                        addresses = c_utxo['addresses'],
                        utxoId= c_utxo['utxoId'],
                        assetId = asset.get('assetId'),
                        asset_name = asset.get('name', ''),
                        symbol = asset.get('symbol', ''),
                        denomination = asset.get('denomination',0),
                        asset_type = asset.get('type',''),
                        amount = asset.get('amount',0)
                    )
                consumed_utxos.append(commit_utxo.__dict__)

            page_token = res_data.get('nextPageToken')

            data.append(avalanche_tx.__dict__)
            
    return current_day.strftime("%Y-%m-%d")



def calculate_x_transaction_values(transaction):
    
    amountUnlocked = transaction.get('amountUnlocked', [])
    amountCreated = transaction.get('amountCreated', [])
    
    amount_unlocked = {}
    amount_created = {}
    
    for amount in amountUnlocked:
        if int(amount['denomination']) != 0:
            unlocked_value = int(amount['amount']) / int(amount['denomination'])
        else:
            unlocked_value = int(amount['amount'])

        if amount['name'] in amount_unlocked:
            amount_unlocked[amount['name']] += unlocked_value
        else:
            amount_unlocked[amount['name']] = unlocked_value

    for amount in amountCreated:
        if int(amount['denomination']) != 0:
            created_value = int(amount['amount']) / int(amount['denomination'])
        else:
            created_value = int(amount['amount'])

        if amount['name'] in amount_created:
            amount_created[amount['name']] += created_value
        else:
            amount_created[amount['name']] = created_value

    return amount_unlocked, amount_created

# C chain
def extract_c_chain_data(last_day):
    last_timestamp = convert_to_gmt_timestamp(last_day)
    current_day = get_today_start_gmt_timestamp()
    
    page_token = None
    
    params = {
        "pageSize": 100
    }

    url = "https://glacier-api.avax.network/v1/networks/mainnet/blockchains/c-chain/transactions"

    data = []
    input_env = []
    output_env = []
    emitted_utxos = []
    consumed_utxos = []
    run = True

    while run:
        if page_token:
            params["pageToken"] = page_token
        
        res_data = fetch_transactions(url, params)
        transactions = res_data.get('transactions', [])

        for tx in transactions:
            
            timestamp = int(tx.get("timestamp"))

            # Check if the transaction is before the current day
            if timestamp < current_day:
                # Save data to the database for the day that just completed
                # save_to_database(current_day.strftime("%Y-%m-%d"), pd.DataFrame(data), pd.DataFrame(input_env), pd.DataFrame(output_env), pd.DataFrame(consumed_utxos), pd.DataFrame(emitted_utxos))
                current_date = current_day.strftime("%Y-%m-%d")
                
                df_trx = pd.DataFrame(data)
                df_trx['date'] = current_date
                df_emitted_utxos = pd.DataFrame(emitted_utxos)
                df_emitted_utxos['date'] = current_date
                df_consumed_utxos = pd.DataFrame(consumed_utxos)
                df_consumed_utxos['date'] = current_date
                df_input_env = pd.DataFrame(input_env)
                df_input_env['date'] = current_date
                df_output_env = pd.DataFrame(output_env)
                df_output_env['date'] = current_date
                
                append_dataframe_to_sql('c_transactions', df_trx)
                append_dataframe_to_sql('c_emitted_utxos', df_emitted_utxos)
                append_dataframe_to_sql('c_emitted_utxos', df_consumed_utxos)
                append_dataframe_to_sql('c_consumed_utxos', df_input_env)
                append_dataframe_to_sql('c_consumed_utxos', df_output_env)
                # Move to the previous day
                current_day -= 86400
                data = []
                emitted_utxos = []
                consumed_utxos = []

            if timestamp <= last_timestamp:
                run = False
                break

            txHash=tx.get("txHash")
            blockHash=tx.get("blockHash")
            txType=tx.get("txType")
            amount_unlocked, amount_created = calculate_x_transaction_values(tx)

            avalanche_tx = Avalanche_C_Model(
                txHash=txHash,
                blockHash=blockHash,
                blockHeight=tx.get("blockHeight"),
                txType=txType,
                timestamp=timestamp,
                sourceChain=tx.get("sourceChain"),
                destinationChain=tx.get("destinationChain"),
                memo=tx.get("memo"),
                amountUnlocked=amount_unlocked,
                amountCreated=amount_created
            )
            
            if(txType == "ExportTx"):
                # env inputs 
                for env_inputs in tx.get('evmInputs', []):
                    
                    asset =  env_inputs['asset']
                    
                    emit_utxo = AvalancheUTXO(
                            txHash = txHash,
                            txType = txType,
                            blockHash = blockHash,
                            addresses = env_inputs['fromAddress'],
                            utxoId= None,
                            assetId = asset.get('assetId'),
                            asset_name = asset.get('name', ''),
                            symbol = asset.get('symbol', ''),
                            denomination = asset.get('denomination',0),
                            asset_type = asset.get('type',''),
                            amount = asset.get('amount',0)
                        )
                    
                    input_env.append(emit_utxo.__dict__)
                
                # emmitted UTXOs
                for e_utxo in tx.get('emittedUtxos', []):
                    
                    asset =  e_utxo['asset']
                    
                    emit_utxo = AvalancheUTXO(
                            txHash = txHash,
                            txType = txType,
                            blockHash = blockHash,
                            addresses = e_utxo['addresses'],
                            utxoId= e_utxo['utxoId'],
                            assetId = asset.get('assetId'),
                            asset_name = asset.get('name', ''),
                            symbol = asset.get('symbol', ''),
                            denomination = asset.get('denomination',0),
                            asset_type = asset.get('type',''),
                            amount = asset.get('amount',0)
                        )
                    
                    emitted_utxos.append(emit_utxo.__dict__)
                    
            elif(txType == "ImportTx"):
                
                for env_inputs in tx.get('evmOutputs', []):
                    asset =  env_inputs['asset']
                    
                    emit_utxo = AvalancheUTXO(
                            txHash = txHash,
                            txType = txType,
                            blockHash = blockHash,
                            addresses = env_inputs['toAddress'],
                            utxoId= None,
                            assetId = asset.get('assetId'),
                            asset_name = asset.get('name', ''),
                            symbol = asset.get('symbol', ''),
                            denomination = asset.get('denomination',0),
                            asset_type = asset.get('type',''),
                            amount = asset.get('amount',0)
                        )
                    
                    output_env.append(emit_utxo.__dict__)

                # emmitted UTXOs
                for e_utxo in tx.get('consumedUtxos', []):
                    
                    
                    asset =  e_utxo['asset']
                    
                    emit_utxo = AvalancheUTXO(
                            txHash = txHash,
                            txType = txType,
                            blockHash = blockHash,
                            addresses = e_utxo['addresses'],
                            utxoId= e_utxo['utxoId'],
                            assetId = asset.get('assetId'),
                            asset_name = asset.get('name', ''),
                            symbol = asset.get('symbol', ''),
                            denomination = asset.get('denomination',0),
                            asset_type = asset.get('type',''),
                            amount = asset.get('amount',0)
                        )
                    consumed_utxos.append(emit_utxo.__dict__)
            page_token = res_data.get('nextPageToken')
            
            data.append(avalanche_tx.__dict__)
    
    return current_day.strftime("%Y-%m-%d")



def extract_p_chain_data(last_day):
    
    last_timestamp = convert_to_gmt_timestamp(last_day)
    current_day = get_today_start_gmt_timestamp()
    
    page_token = None
    params = {"pageSize": 100}
    url = "https://glacier-api.avax.network/v1/networks/mainnet/blockchains/p-chain/transactions"
    data = []
    emitted_utxos= []
    consumed_utxos = []
    env_inputs = []
    env_outputs = []
    
    run = True

    while run:
        if page_token:
            params["pageToken"] = page_token
        
        res_data = fetch_transactions(url, params)
        transactions = res_data.get('transactions', [])

        for tx in transactions:
            timestamp = int(tx.get("timestamp"))

            # Check if the transaction is before the current day
            if timestamp < current_day:
                # Save data to the database for the day that just completed
                # save_to_database(current_day.strftime("%Y-%m-%d"), pd.DataFrame(data), pd.DataFrame(emitted_utxos), pd.DataFrame(consumed_utxos))
                current_date = current_day.strftime("%Y-%m-%d")
                
                df_trx = pd.DataFrame(data)
                df_trx['date'] = current_date
                df_emitted_utxos = pd.DataFrame(emitted_utxos)
                df_emitted_utxos['date'] = current_date
                df_consumed_utxos = pd.DataFrame(consumed_utxos)
                df_consumed_utxos['date'] = current_date
                
                append_dataframe_to_sql('p_transactions', df_trx)
                append_dataframe_to_sql('p_emitted_utxos', df_emitted_utxos)
                append_dataframe_to_sql('p_consumed_utxos', df_consumed_utxos)
                
                # Move to the previous day
                current_day -= 86400
                data = []
                emitted_utxos = []
                consumed_utxos = []

            if timestamp <= last_timestamp:
                run = False
                break
                
            amountStaked = calculate_p_transaction_value(tx.get("amountStaked", []))
            amountBurned = calculate_p_transaction_value(tx.get("amountBurned", []))

            txHash=tx.get("txHash")
            blockHash=tx.get("blockHash")
            txType=tx.get("txType")
            
            p_tx = Avalanche_P_Model(
                txHash=tx.get("txHash"),
                txType=tx.get("txType"),
                blockTimestamp=timestamp,
                blockNumber=tx.get("blockNumber"),
                blockHash=tx.get("blockHash"),
                sourceChain = tx.get("sourceChain",''),
                destinationChain =  tx.get("destinationChain",''),
                memo=tx.get("memo"),
                rewardAddresses = tx.get("rewardAddresses",''),
                estimatedReward = tx.get("estimatedReward",''),
                startTimestamp = tx.get("startTimestamp",''),
                endTimestamp = tx.get("endTimestamp",''),
                delegationFeePercent = tx.get("delegationFeePercent",''),
                nodeId=tx.get("nodeId",''),
                subnetId=tx.get("subnetId",''),
                value = tx.get("value",''),
                amountStaked=amountStaked,
                amountBurned=amountBurned,
            )
            
            # emmitted UTXOs
            for e_utxo in tx.get('emittedUtxos', []):
                
                
                asset =  e_utxo['asset']
                
                emit_utxo = AvalancheUTXO(
                        txHash = txHash,
                        txType=txType,
                        blockHash = blockHash,
                        addresses = e_utxo['addresses'],
                        utxoId= e_utxo['utxoId'],
                        assetId = asset.get('assetId'),
                        asset_name = asset.get('name', ''),
                        symbol = asset.get('symbol', ''),
                        denomination = asset.get('denomination',0),
                        asset_type = asset.get('type',''),
                        amount = asset.get('amount',0)
                    )
                
                emitted_utxos.append(emit_utxo.__dict__)
            
            # consumed UTXOs
            for c_utxo in tx.get('consumedUtxos', []):
                
                asset =  c_utxo['asset']
                
                commit_utxo = AvalancheUTXO(
                        txHash = txHash,
                        txType = txType,
                        blockHash = blockHash,
                        addresses = c_utxo['addresses'],
                        utxoId= c_utxo['utxoId'],
                        assetId = asset.get('assetId'),
                        asset_name = asset.get('name', ''),
                        symbol = asset.get('symbol', ''),
                        denomination = asset.get('denomination',0),
                        asset_type = asset.get('type',''),
                        amount = asset.get('amount',0)
                    )
                consumed_utxos.append(commit_utxo.__dict__)
                
            data.append(p_tx.__dict__)
        page_token = res_data.get('nextPageToken')
    
    return current_day.strftime("%Y-%m-%d")


def calculate_p_transaction_value(amounts):
    total_value = sum(int(asset['amount']) for asset in amounts) / 10**9  # Convert to AVAX
    return total_value

#---------------------------------------------------------

def extract_avalanche_data(last_x_time, last_c_time,last_p_time):
    x_chain_data = extract_x_chain_data(last_x_time)
    c_chain_data = extract_c_chain_data(last_c_time)
    p_chain_data = extract_p_chain_data(last_p_time)

    return x_chain_data, c_chain_data, p_chain_data
    # return x_chain_data

class EVM:
    def __init__(self, txHash, txType, blockHash, assetId, asssetName, symbol, denomination, type, amount, fromAddress):
        self.txHash = txHash
        self.txType = txType
        self.blockHash = blockHash
        self.assetId = assetId
        self.asssetName = asssetName
        self.symbol = symbol
        self.denomination = denomination
        self.type = type
        self.amount = amount
        self.fromAddress = fromAddress


if __name__ == "__main__":
    # extract_p_chain_data(1705276800)
    # extract_c_chain_data(1705276800)
    extract_x_chain_data("2024-01-19")