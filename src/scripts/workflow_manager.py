# workflow_manager.py
from blockchain.avalanche.avalanche_data_extraction import fetch_transactions
from services.data_extraction_service import parse_avalanche_transactions

def main():
    json_data = fetch_transactions()
    if json_data:
        transactions = parse_avalanche_transactions(json_data)
        for tx in transactions:
            print(f"`Transaction Hash: {tx.tx_hash}, Block Height: {tx.block_height}, Type: {tx.tx_type}`")

if __name__ == "__main__":
    main()
