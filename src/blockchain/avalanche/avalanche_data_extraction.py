import pandas as pd
import requests
import time
from datetime import datetime
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
            # for utxo in tx.get('emittedUtxos', []):
            #     print(utxo)
            # consumed_utxos = [AvalancheUTXO(**parse_utxo(utxo)) for utxo in tx.get('consumedUtxos', [])]
            # emitted_utxos = [AvalancheUTXO(**parse_utxo(utxo)) for utxo in tx.get('emittedUtxos', [])]
            txHash = tx.get("txHash")
            blockHash = tx.get("blockHash")
            amount_unlocked, amount_created = calculate_x_transaction_values(tx)
            avalanche_tx = Avalanche_X_Model(
                txHash=txHash,
                blockHash=blockHash,
                blockHeight = tx.get("blockHeight"),
                timestamp=timestamp,
                value=calculate_x_transaction_value(tx),
                memo=tx.get("memo"),
                chainFormat=tx.get("chainFormat"),
                txType=tx.get("txType"),
                # consumedUtxos=consumed_utxos,
                # emittedUtxos=emitted_utxos,
                # amountUnlocked = amount_unlocked,
                # amountCreated = amount_created,
                # active_senders = extract_active_senders(tx),
                # active_adreesess = extract_addresses_from_transaction(tx)
            )
            
            for utxo in tx.get('emittedUtxos', []):
                assets = []
                for asset in utxo['asset']:
                    {
                        "assetId": utxo['assetId'],
                        "name": utxo.get('name', ''),
                        "symbol": utxo.get('symbol', ''),
                        "denomination": utxo.get('denomination',0),
                        "type": utxo.get('type',''),
                        "amount": utxo.get('amount','')
                    }
                AvalancheUTXO(
                    txHash = txHash,
                    blockHash = blockHash,
                    addresses = utxo['addresses'],
                    utxoId= utxo['utxoId'],
                    assets = assets
                    )
            page_token = res_data.get('nextPageToken')
            
            data.append(avalanche_tx.__dict__)

    return pd.DataFrame(data)

def parse_utxo(utxo):
    print(utxo)
    return {
        'utxoId': utxo['utxoId'],
        'txHash': utxo.get('creationTxHash', ''),
        'outputIndex': utxo['outputIndex'],
        'addresses': utxo['addresses'],
        'amount': int(utxo['asset']['amount']),
        'assetId': utxo['asset']['assetId'],
        'assetName': utxo['asset'].get('name', ''),
        'assetSymbol': utxo['asset'].get('symbol', ''),
        'assetDenomination': utxo['asset'].get('denomination', 0),
        'utxoType': utxo.get('utxoType', ''),
        'consumingTxHash': utxo.get('consumingTxHash', ''),
        'consumingTxTimestamp': utxo.get('consumingTxTimestamp', 0),
        'credentials': utxo.get('credentials', [])
    }

def extract_active_senders(transactions):
    active_senders = set()
    for utxo in transactions.get("consumedUtxos", []):
        active_senders.update(utxo.get("addresses", []))

    return active_senders

def extract_addresses_from_transaction(transaction):
    all_addresses = set()

    # Extract addresses from consumed UTXOs
    for utxo in transaction.get("consumedUtxos", []):
        all_addresses.update(utxo.get("addresses", []))

    # Extract addresses from emitted UTXOs
    for utxo in transaction.get("emittedUtxos", []):
        all_addresses.update(utxo.get("addresses", []))

    return all_addresses


def calculate_x_transaction_values(transaction):
    print("ok")
    
    amountUnlocked = transaction.get('amountUnlocked', [])
    amountCreated = transaction.get('amountCreated', [])
    
    amount_unlocked = {}
    amount_created = {}
    
    for amount in amountUnlocked:
        if amount['name'] in amount_unlocked:
            amount_unlocked[amount['name']] += amount['amount'] / amount['denomination']
        else:
            amount_unlocked[amount['name']] = amount['amount'] / amount['denomination']
    
    for amount in amountCreated:
        if amount['name'] in amount_created:
            amount_created[amount['name']] += amount['amount'] / amount['denomination']
        else:
            amount_created[amount['name']] = amount['amount'] / amount['denomination']
        
    return amount_unlocked, amount_created

def extract_c_chain_data(last_timestamp):
    page_token = None
    
    params = {
        "pageSize": 100
    }

    url = "https://glacier-api.avax.network/v1/networks/mainnet/blockchains/c-chain/transactions"

    data = []
    
    run = True

    while run:
        if page_token:
            params["pageToken"] = page_token
        
        res_data = fetch_transactions(url, params)
        transactions = res_data.get('transactions', [])

        for tx in transactions:
            
            timestamp=int(tx.get("timestamp"))          
            if timestamp <= last_timestamp:
                run = False
                break

            total_input_value, total_output_value = calculate_c_chain_transaction_value(tx)
            
            evm_inputs = [EVMInput(**input) for input in tx.get('evmInputs', [])]
            emitted_utxos = [AvalancheUTXO(**utxo) for utxo in tx.get('emittedUtxos', [])]
            deployer_addresses, contract_deploy_count = get_contract_deployer_addresses_and_count(tx)
            active_addresses = get_active_addresses(tx)
            
            avalanche_tx = Avalanche_C_Model(
                txHash=tx.get("txHash"),
                blockHash=tx.get("blockHash"),
                blockHeight=tx.get("blockHeight"),
                txType=tx.get("txType"),
                timestamp=timestamp,
                sourceChain=tx.get("sourceChain"),
                destinationChain=tx.get("destinationChain"),
                memo=tx.get("memo"),
                amountUnlocked = total_input_value,
                amountCreated = total_output_value,
                # evmInputs=evm_inputs,
                # emittedUtxos=emitted_utxos,
                deployer_addresses = deployer_addresses,
                contract_deploy_count = contract_deploy_count,
                active_addresses = active_addresses
            )

            page_token = res_data.get('nextPageToken')
            
            data.append(avalanche_tx.__dict__)
    
    return pd.DataFrame(data)

def get_contract_deployer_addresses_and_count(transaction):
    deployer_addresses = set()
    contract_deploy_count = 0

    if transaction.get('txType') == 'Create':
            # Assuming the contract creator is in evmInputs
            for input_item in transaction.get('evmInputs', []):
                if 'fromAddress' in input_item:
                    deployer_addresses.add(input_item['fromAddress'])
                    contract_deploy_count += 1

    return deployer_addresses, contract_deploy_count

def get_active_addresses(transaction):
    active_addresses = set()
    
    # Add addresses from evmInputs
    for input_item in transaction.get('evmInputs', []):
        if 'fromAddress' in input_item:
            active_addresses.add(input_item['fromAddress'])

    # Add addresses from evmOutputs
    for output_item in transaction.get('evmOutputs', []):
        if 'toAddress' in output_item:
            active_addresses.add(output_item['toAddress'])

    return active_addresses

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

def calculate_x_transaction_value(transaction):
    #TO DO : Handle whwn asset not avalanche
    total_consumed = sum(int(utxo['asset']['amount']) for utxo in transaction.get('consumedUtxos', []))
    total_emitted = sum(int(utxo['asset']['amount']) for utxo in transaction.get('emittedUtxos', []))
    return (total_consumed - total_emitted) / 10**9

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
    c_chain_data = extract_c_chain_data(last_c_time)
    p_chain_data = extract_p_chain_data(last_p_time)

    
    # p_chain_data = extract_p_chain_data(last_block)
    return x_chain_data, c_chain_data, p_chain_data

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