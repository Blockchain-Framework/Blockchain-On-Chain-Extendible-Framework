from utils.scripts.utils.http_utils import fetch_transactions
from utils.scripts.utils.time_utils import convert_to_gmt_timestamp

def extract(date):
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


def calculate_amount_staked(transation):
    amounts = transation.get("amountStaked", [])
    total_value = sum(int(asset['amount']) for asset in amounts) / 10**9  # Convert to AVAX
    return total_value

def calculate_amount_burned(transation):
    amounts = transation.get("amountBurned", [])
    total_value = sum(int(asset['amount']) for asset in amounts) / 10**9  # Convert to AVAX
    return total_value

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
