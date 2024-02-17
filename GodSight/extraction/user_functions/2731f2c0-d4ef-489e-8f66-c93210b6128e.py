from utils.scripts.utils.http_utils import fetch_transactions
from utils.scripts.utils.time_utils import convert_to_gmt_timestamp

def extract(date):
    # Convert the date to GMT timestamp and define the end timestamp for one day laterdef calculate_amount_unlocked(transaction):
    amountUnlocked = transaction.get('amountUnlocked', [])
    
    amount_unlocked = {}
    
    for amount in amountUnlocked:
        if int(amount['denomination']) != 0:
            unlocked_value = int(amount['amount']) / int(amount['denomination'])
        else:
            unlocked_value = int(amount['amount'])def calculate_amount_created(transaction):
    amountCreated = transaction.get('amountCreated', [])def getAssetId(utxo):
    asset =  utxo['asset']
    return asset.get('assetId')def getAssetName(utxo):
    asset =  utxo['asset']
    return asset.get('name', '')def getSymbol(utxo):
    asset =  utxo['asset']
    return asset.get('symbol', '')def getDenomination(utxo):
    asset =  utxo['asset']
    return asset.get('denomination',0)def getAsset_type(utxo):
    asset =  utxo['asset']
    return asset.get('type','')def getAmount(utxo):
    asset =  utxo['asset']
    return asset.get('amount',0