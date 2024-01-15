import pandas as pd
import requests
import time
from datetime import datetime
import json

import os
import sys
sys.path.insert(0, 'D:\\Academics\\FYP\\Repos\\Blockchain-On-Chain-Extendible-Framework')

from src.utils.http_utils import fetch_transactions
from src.blockchain.avalanche.avalanche_model import Avalanche_X_Model, Avalanche_C_Model, Avalanche_P_Model
from src.blockchain.avalanche.avalanche_UTXO_model import AvalancheUTXO

def extract_x_chain_data(last_timestamp):
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
            if timestamp <= last_timestamp:
                run = False
                break
            txHash = tx.get("txHash")
            blockHash = tx.get("blockHash")
            amount_unlocked, amount_created = calculate_x_transaction_values(tx)
            
            avalanche_tx = Avalanche_X_Model(
                txHash=txHash,
                blockHash=blockHash,
                blockHeight = tx.get("blockHeight"),
                timestamp=timestamp,
                memo=tx.get("memo"),
                chainFormat=tx.get("chainFormat"),
                txType=tx.get("txType"),
                amountUnlocked = amount_unlocked,
                amountCreated = amount_created
            )
            
            # emmitted UTXOs
            for e_utxo in tx.get('emittedUtxos', []):
                
                print(len(e_utxo['asset']))
                asset =  e_utxo['asset']
                
                emit_utxo = AvalancheUTXO(
                        txHash = txHash,
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
    return pd.DataFrame(data), emitted_utxos, consumed_utxos



def calculate_x_transaction_values(transaction):
    
    amountUnlocked = transaction.get('amountUnlocked', [])
    amountCreated = transaction.get('amountCreated', [])
    
    amount_unlocked = {}
    amount_created = {}
    
    for amount in amountUnlocked:
        if amount['name'] in amount_unlocked:
            amount_unlocked[amount['name']] += int(amount['amount']) / int(amount['denomination'])
        else:
            amount_unlocked[amount['name']] = int(amount['amount']) / int(amount['denomination'])
    
    for amount in amountCreated:
        if amount['name'] in amount_created:
            amount_created[amount['name']] += int(amount['amount']) / int(amount['denomination'])
        else:
            amount_created[amount['name']] = int(amount['amount']) / int(amount['denomination'])
        
    return amount_unlocked, amount_created


# C chain
def extract_c_chain_data(last_timestamp):
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
            print(tx.get("txType"))
            print(tx.keys())
            timestamp=int(tx.get("timestamp"))          
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
                    
                    print(len(env_inputs['asset']))
                    asset =  env_inputs['asset']
                    
                    emit_utxo = AvalancheUTXO(
                            txHash = txHash,
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
                    
                    print(len(e_utxo['asset']))
                    asset =  e_utxo['asset']
                    
                    emit_utxo = AvalancheUTXO(
                            txHash = txHash,
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
                print(tx)
                for env_inputs in tx.get('evmOutputs', []):
                    asset =  env_inputs['asset']
                    
                    emit_utxo = AvalancheUTXO(
                            txHash = txHash,
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
                    
                    print(len(e_utxo['asset']))
                    asset =  e_utxo['asset']
                    
                    emit_utxo = AvalancheUTXO(
                            txHash = txHash,
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
    
    return pd.DataFrame(data),input_env,output_env,consumed_utxos,emitted_utxos



def extract_p_chain_data(last_timestamp):
    print("start p chain extraction")
    page_token = None
    params = {"pageSize": 100}
    url = "https://glacier-api.avax.network/v1/networks/mainnet/blockchains/p-chain/transactions"
    data = []
    run = True

    while run:
        if page_token:
            params["pageToken"] = page_token
        
        res_data = fetch_transactions(url, params)
        transactions = res_data.get('transactions', [])

        for tx in transactions:
            timestamp = int(tx.get("blockTimestamp"))
            if timestamp <= last_timestamp:
                run = False
                break

            amountStaked = calculate_p_transaction_value(tx.get("amountStaked", []))
            amountBurned = calculate_p_transaction_value(tx.get("amountBurned", []))

            # consumed_utxos = [AvalancheUTXO(**utxo) for utxo in tx.get('consumedUtxos', [])]
            # emitted_utxos = [AvalancheUTXO(**utxo) for utxo in tx.get('emittedUtxos', [])]

            p_tx = Avalanche_P_Model(
                txHash=tx.get("txHash"),
                txType=tx.get("txType"),
                blockTimestamp=timestamp,
                blockNumber=tx.get("blockNumber"),
                blockHash=tx.get("blockHash"),
                memo=tx.get("memo"),
                nodeId=tx.get("nodeId"),
                subnetId=tx.get("subnetId"),
                amountStaked=amountStaked,
                amountBurned=amountBurned,
                # consumedUtxos=consumed_utxos,
                # emittedUtxos=emitted_utxos,
                active_adreesess = get_p_chain_active_addresses(tx),
                active_senders = get_p_chain_sender_addresses(tx)
            )
            data.append(p_tx.__dict__)
        page_token = res_data.get('nextPageToken')
        
    return pd.DataFrame(data)

def get_p_chain_active_addresses(transaction):
    active_addresses = set()

    # Add addresses from consumed UTXOs
    for utxo in transaction.get('consumedUtxos', []):
        for address in utxo.get('addresses', []):
            active_addresses.add(address)

    # Add addresses from emitted UTXOs
    for utxo in transaction.get('emittedUtxos', []):
        for address in utxo.get('addresses', []):
            active_addresses.add(address)

    return active_addresses

def get_p_chain_sender_addresses(transaction):
    sender_addresses = set()

    # Add addresses from consumed UTXOs
    for utxo in transaction.get('consumedUtxos', []):
        for address in utxo.get('addresses', []):
            sender_addresses.add(address)

    return sender_addresses


def calculate_p_transaction_value(amounts):
    total_value = sum(int(asset['amount']) for asset in amounts) / 10**9  # Convert to AVAX
    return total_value

# def calculate_x_transaction_value(transaction):
#     #TO DO : Handle whwn asset not avalanche
#     total_consumed = sum(int(utxo['asset']['amount']) for utxo in transaction.get('consumedUtxos', []))
#     total_emitted = sum(int(utxo['asset']['amount']) for utxo in transaction.get('emittedUtxos', []))
#     return (total_consumed - total_emitted) / 10**9

def calculate_c_chain_transaction_value(transaction):
    # Initialize total values
    total_input_value = 0
    total_output_value = 0

    # Calculate the total input value
    if 'evmInputs' in transaction:
        for input_item in transaction['evmInputs']:
            # Ensure the 'amount' field is present
            if 'asset' in input_item and 'amount' in input_item['asset']:
                total_input_value += int(input_item['asset']['amount'])

    # Calculate the total output value
    if 'evmOutputs' in transaction:
        for output_item in transaction['evmOutputs']:
            # Ensure the 'amount' field is present
            if 'asset' in output_item and 'amount' in output_item['asset']:
                total_output_value += int(output_item['asset']['amount'])

    # Convert amounts from smallest unit to AVAX (assuming denomination is 9)
    total_input_value /= 10**9
    total_output_value /= 10**9

    return total_input_value, total_output_value

def extract_avalanche_data(last_x_time, last_c_time,last_p_time):
    x_chain_data = extract_x_chain_data(last_x_time)
    # c_chain_data = extract_c_chain_data(last_c_time)
    # p_chain_data = extract_p_chain_data(last_p_time)

    
    # p_chain_data = extract_p_chain_data(last_block)
    #return x_chain_data, c_chain_data, p_chain_data
    return x_chain_data

class EVMInput:
    def __init__(self, asset, fromAddress, credentials):
        self.asset = Asset(**asset)
        self.fromAddress = fromAddress
        self.credentials = credentials

class Asset:
    def __init__(self, assetId, name, symbol, denomination, type, amount):
        self.assetId = assetId
        self.name = name
        self.symbol = symbol
        self.denomination = denomination
        self.type = type
        self.amount = amount
        
if __name__ == "__main__":
    extract_c_chain_data(1705276800)