# avalanche_data_extraction.py
import pandas as pd
from utils.http_utils import send_request
from .avalanche_model import AvalancheModel

def extract_avalanche_data():
    url = "https://glacier-api.avax.network/v1/networks/mainnet/blockchains/x-chain/transactions"
    headers = {"accept": "application/json"}
    response = send_request(url, headers=headers)

    if response is None:
        return pd.DataFrame()

    transactions = response.get("transactions", [])
    data = []

    for tx in transactions:
        avalanche_tx = AvalancheModel(
            txHash=tx.get("txHash"),
            blockHash=tx.get("blockHash"),
            timestamp=tx.get("timestamp"),
            value = tx.get("value"),
            memo=tx.get("memo"),
            chainFormat=tx.get("chainFormat"),
            
        )
        data.append(avalanche_tx.__dict__)

    return pd.DataFrame(data)
