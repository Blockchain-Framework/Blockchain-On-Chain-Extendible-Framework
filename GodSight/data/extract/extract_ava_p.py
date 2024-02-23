from utils.handler.time import convert_to_gmt_timestamp
from utils.handler.http import fetch_transactions


def extract(date):
    start_timestamp = convert_to_gmt_timestamp(date)
    end_timestamp = start_timestamp + 86400
    url = "https://glacier-api.avax.network/v1/networks/mainnet/blockchains/p-chain/transactions"

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
            timestamp = int(tx.get("blockTimestamp"))
            txHash = tx.get('txHash','')
            blockHash = tx.get('blockHash','')
            txType= tx.get(('txType'),'')

            
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

