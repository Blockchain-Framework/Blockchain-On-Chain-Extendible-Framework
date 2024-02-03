import pandas as pd
import psycopg2
import time
from datetime import datetime
import logging

import os
import sys
# sys.path.insert(0, 'D:\\Academics\\FYP\\Repos\\Blockchain-On-Chain-Extendible-Framework')

from utils.scripts.utils.http_utils import fetch_transactions
from utils.scripts.avalanche.avalanche_model import Avalanche_X_Model, Avalanche_C_Model, Avalanche_P_Model
from utils.scripts.avalanche.avalanche_UTXO_model import AvalancheUTXO
from utils.database.database_service import append_dataframe_to_sql, get_query_results

from datetime import datetime
import pytz


def execute_query(query):
    """
    Execute a database query safely.
    Returns a DataFrame or None if an exception occurs.
    """
    try:
        return get_query_results(query)
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(f"Database error: {error}")
        return None

def key_mapper(key):
    def decorator(func):
        func._key = key
        return func
    return decorator


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

# X chain
@key_mapper("x")
def extract_x_chain_data(last_day):
    print("x start....")
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
                current_date = datetime.fromtimestamp(current_day).strftime("%Y-%m-%d")
                
                df_trx = pd.DataFrame(data)
                df_trx['date'] = current_date
                df_emitted_utxos = pd.DataFrame(emitted_utxos)
                df_emitted_utxos['date'] = current_date
                df_consumed_utxos = pd.DataFrame(consumed_utxos)
                df_consumed_utxos['date'] = current_date
                
                df_trx['date'] = pd.to_datetime(df_trx['date'])
                df_emitted_utxos['date'] = pd.to_datetime(df_emitted_utxos['date'])
                df_consumed_utxos['date'] = pd.to_datetime(df_consumed_utxos['date'])
                
                # print(df_trx)
                append_dataframe_to_sql('x_transactions', df_trx)
                append_dataframe_to_sql('x_emitted_utxos', df_emitted_utxos)
                append_dataframe_to_sql('x_consumed_utxos', df_consumed_utxos)
                # print("x transaction",current_date)
                
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
            amount_unlocked, amount_created = calculate_amount_unlocked_created(tx)

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
            
    return current_date

# C chain
@key_mapper("c")
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
                current_date = datetime.fromtimestamp(current_day).strftime("%Y-%m-%d")
                
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
                
                df_trx['date'] = pd.to_datetime(df_trx['date'])
                df_emitted_utxos['date'] = pd.to_datetime(df_emitted_utxos['date'])
                df_consumed_utxos['date'] = pd.to_datetime(df_consumed_utxos['date'])
                df_input_env['date'] = pd.to_datetime(df_input_env['date'])
                df_output_env['date'] = pd.to_datetime(df_output_env['date'])

                append_dataframe_to_sql('c_transactions', df_trx)
                append_dataframe_to_sql('c_emitted_utxos', df_emitted_utxos)
                append_dataframe_to_sql('c_emitted_utxos', df_consumed_utxos)
                append_dataframe_to_sql('c_consumed_utxos', df_input_env)
                append_dataframe_to_sql('c_consumed_utxos', df_output_env)
                # print("c transaction",current_date)
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
            amount_unlocked, amount_created = calculate_amount_unlocked_created(tx)

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
            else:
                print(txType)
                print(tx)
            data.append(avalanche_tx.__dict__)
            page_token = res_data.get('nextPageToken')
    return current_date

# P chain
@key_mapper("p")
def extract_p_chain_data(last_day):
    
    last_timestamp = convert_to_gmt_timestamp(last_day)
    current_day = get_today_start_gmt_timestamp()
    
    page_token = None
    params = {"pageSize": 100}
    url = "https://glacier-api.avax.network/v1/networks/mainnet/blockchains/p-chain/transactions"
    data = []
    emitted_utxos= []
    consumed_utxos = []
    
    run = True

    while run:
        if page_token:
            params["pageToken"] = page_token
        
        res_data = fetch_transactions(url, params)
        transactions = res_data.get('transactions', [])

        for tx in transactions:
            timestamp = int(tx.get("blockTimestamp"))

            # Check if the transaction is before the current day
            if timestamp < current_day:
                # Save data to the database for the day that just completed
                # save_to_database(current_day.strftime("%Y-%m-%d"), pd.DataFrame(data), pd.DataFrame(emitted_utxos), pd.DataFrame(consumed_utxos))
                current_date = current_date = datetime.fromtimestamp(current_day).strftime("%Y-%m-%d")
                
                df_trx = pd.DataFrame(data)
                df_trx['date'] = current_date
                df_emitted_utxos = pd.DataFrame(emitted_utxos)
                df_emitted_utxos['date'] = current_date
                df_consumed_utxos = pd.DataFrame(consumed_utxos)
                df_consumed_utxos['date'] = current_date
                
                df_trx['date'] = pd.to_datetime(df_trx['date'])
                df_emitted_utxos['date'] = pd.to_datetime(df_emitted_utxos['date'])
                df_consumed_utxos['date'] = pd.to_datetime(df_consumed_utxos['date'])
                
                append_dataframe_to_sql('p_transactions', df_trx)
                append_dataframe_to_sql('p_emitted_utxos', df_emitted_utxos)
                append_dataframe_to_sql('p_consumed_utxos', df_consumed_utxos)
                # print("p transaction",current_date)
                
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
    
    return current_date


def calculate_p_transaction_value(amounts):
    total_value = sum(int(asset['amount']) for asset in amounts) / 10**9  # Convert to AVAX
    return total_value


def calculate_amount_unlocked_created(transaction):   
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



if __name__ == "__main__":
    extract_c_chain_data("2024-01-19")
    # extract_x_chain_data("2024-01-19")
    # extract_p_chain_data("2024-01-19")