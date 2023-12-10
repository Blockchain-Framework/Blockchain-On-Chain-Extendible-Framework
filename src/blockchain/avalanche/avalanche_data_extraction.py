import pandas as pd
from src.utils.http_utils import send_request
from src.blockchain.avalanche.avalanche_model import Avalanche_X_Model  

def extract_avalanche_data():
    url = "https://glacier-api.avax.network/v1/networks/mainnet/blockchains/x-chain/transactions"
    headers = {"accept": "application/json"}
    response = send_request(url, headers=headers)

    if response is None:
        return pd.DataFrame()

    transactions = response.get("transactions", [])
    data = []

    for tx in transactions:
        avalanche_tx = Avalanche_X_Model(
            txHash=tx.get("txHash"),
            blockHash=tx.get("blockHash"),
            timestamp=tx.get("timestamp"),
            value=calculate_transaction_value(tx),
            memo=tx.get("memo"),
            chainFormat=tx.get("chainFormat"),
            txType=tx.get("txType")  # Assuming txType is required
        )
        data.append(avalanche_tx.__dict__)
        
    return pd.DataFrame(data)

def calculate_transaction_value(transaction):
    total_consumed = sum(int(utxo['asset']['amount']) for utxo in transaction.get('consumedUtxos', []))
    total_emitted = sum(int(utxo['asset']['amount']) for utxo in transaction.get('emittedUtxos', []))
    return (total_consumed - total_emitted) / 10**9