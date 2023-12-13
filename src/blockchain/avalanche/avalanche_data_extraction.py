import pandas as pd
import requests
import time
from datetime import datetime
from src.utils.http_utils import fetch_transactions
from src.blockchain.avalanche.avalanche_model import Avalanche_X_Model, Avalanche_C_Model, Avalanche_P_Model

def extract_x_chain_data(last_block):
    page_token = None

    params = {
        "pageSize": 100
    }

    url = "https://glacier-api.avax.network/v1/networks/mainnet/blockchains/x-chain/transactions"
    
    data = []
    
    run = True

    while run:
        
        if page_token:
          params["pageToken"] = page_token
    
        res_data = fetch_transactions(url, params)
        transactions = res_data.get('transactions', [])

        for tx in transactions:
          block_height = tx.get("blockHeight")
          if block_height<= last_block:
            run = False
            break

          avalanche_tx = Avalanche_X_Model(
            txHash=tx.get("txHash"),
            blockHash=tx.get("blockHash"),
            blockHeight = block_height,
            timestamp=tx.get("timestamp"),
            value=calculate_x_transaction_value(tx),
            memo=tx.get("memo"),
            chainFormat=tx.get("chainFormat"),
            txType=tx.get("txType") 
          )
            
          page_token = res_data.get('nextPageToken')
          
          data.append(avalanche_tx.__dict__)
        
    return pd.DataFrame(data)

def extract_c_chain_data(last_block):
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
          block_height = tx.get("blockHeight")
                    
          if block_height<= last_block:
            run = False
            break

          total_input_value, total_output_value = calculate_c_chain_transaction_value(tx)
          
          avalanche_tx = Avalanche_C_Model(
              txHash=tx.get("txHash"),
              blockHash=tx.get("blockHash"),
              blockHeight=block_height,
              txType=tx.get("txType"),
              timestamp=tx.get("timestamp"),
              sourceChain=tx.get("sourceChain"),
              destinationChain=tx.get("destinationChain"),
              memo=tx.get("memo"),
              total_input_value = total_input_value,
              total_output_value = total_output_value
          )

          page_token = res_data.get('nextPageToken')
          
          data.append(avalanche_tx.__dict__)
    
    return pd.DataFrame(data)


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

def extract_avalanche_data(last_x_block, last_c_block):
    x_chain_data = extract_x_chain_data(last_x_block)
    c_chain_data = extract_c_chain_data(last_c_block)
    print(type(c_chain_data))
    
    # p_chain_data = extract_p_chain_data(last_block)
    return x_chain_data, c_chain_data