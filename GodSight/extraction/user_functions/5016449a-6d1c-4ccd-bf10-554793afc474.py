from GodSight.extraction.utils.scripts.utils.time_utils import convert_to_gmt_timestamp
from GodSight.extraction.utils.scripts.utils.http_utils import fetch_transactions

def calculate_amount_unlocked(transaction):
    amountUnlocked = transaction.get('amountUnlocked', [])
    
    amount_unlocked = {}
    
    for amount in amountUnlocked:
        if int(amount['denomination']) != 0:
            unlocked_value = int(amount['amount']) / int(amount['denomination'])
        else:
            unlocked_value = int(amount['amount'])

        if amount['name'] in amount_unlocked:
            amount_unlocked[amount['name']] += unlocked_value
        else:
            amount_unlocked[amount['name']] = unlocked_value

    return amount_unlocked


def calculate_amount_created(transaction):
    amountCreated = transaction.get('amountCreated', [])

    amount_created = {}
    
    for amount in amountCreated:
        if int(amount['denomination']) != 0:
            created_value = int(amount['amount']) / int(amount['denomination'])
        else:
            created_value = int(amount['amount'])

        if amount['name'] in amount_created:
            amount_created[amount['name']] += created_value
        else:
            amount_created[amount['name']] = created_value
    return amount_created


def getAddress(utxo):
    if 'addresses' in utxo:
        return utxo['addresses']
    elif 'fromAddress' in utxo:
        return [utxo['fromAddress']]
    elif 'toAddress' in utxo:
        return [utxo['toAddress']]
    else:
        return []


def getAssetId(utxo):
    asset = utxo.get('asset', {})
    return asset.get('assetId', '')


def getAssetName(utxo):
    asset = utxo.get('asset', {})
    return asset.get('name', '')


def getSymbol(utxo):
    asset = utxo.get('asset', {})
    return asset.get('symbol', '')


def getDenomination(utxo):
    asset = utxo.get('asset', {})
    return asset.get('denomination',0)


def getAsset_type(utxo):
    asset = utxo.get('asset', {})
    return asset.get('type','')


def getAmount(utxo):
    asset = utxo.get('asset', {})
    return asset.get('amount',0)


def extract(date):
    start_timestamp = convert_to_gmt_timestamp(date)
    end_timestamp = start_timestamp + 86400
    url = "https://glacier-api.avax.network/v1/networks/mainnet/blockchains/c-chain/transactions"

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

            
            if timestamp < start_timestamp:
                run = False
                break
            if timestamp < end_timestamp:
                
                # Process the main transaction details
                trxs.append(tx)
                
                # Process emitted UTXOs
                key = 'emittedUtxos' if 'emittedUtxos' in tx else 'evmOutputs'
                for e_utxo in tx.get(key, []):
                    e_utxo_modified = e_utxo.copy()  
                    e_utxo_modified['txHash'] = txHash
                    e_utxo_modified['blockHash'] = blockHash
                    e_utxo_modified['txType'] = txType
                    emitted_utxos.append(e_utxo_modified)
                
                # Process consumed UTXOs
                key = 'consumedUtxos' if 'consumedUtxos' in tx else 'evmInputs'
                for c_utxo in tx.get(key, []):
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


