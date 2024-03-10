config = {
    'trx_mapping': {
        'tx_hash': ('txHash', "feature"),
        'block_hash': ('blockHash', "feature"),
        'block_height': ('blockHeight', "feature"),
        'timestamp': ('timestamp', "feature"),
        'memo': ('memo', "feature"),
        'chain_format': ('chainFormat', "feature"),
        'tx_type': ('txType', "feature"),
        'amount_unlocked': ('amount_unlocked', "function", "calculate_amount_unlocked"),
        'amount_created': ('amount_created', "function", "calculate_amount_created")
    },

    'emit_utxo_mapping': {
        'addresses': ('addresses', "feature"),
        'utxo_id': ('utxoId', "feature"),
        'tx_hash': ('txHash', "feature"),
        'tx_type': ('txType', "feature"),
        'asset_id': ('assetId', "function", 'getAssetId'),
        'asset_name': ('asset_name', "function", 'getAssetName'),
        'asset_symbol': ('symbol', "function", 'getSymbol'),
        'denomination': ('denomination', "function", 'getDenomination'),
        'asset_type': ('asset_type', "function", 'getAsset_type'),
        'amount': ('amount', "function", 'getAmount')
    },

    'consume_utxo_mapping': {
        'addresses': ('addresses', "feature"),
        'utxo_id': ('utxoId', "feature"),
        'tx_hash': ('txHash', "feature"),
        'tx_type': ('txType', "feature"),
        'block_hash': ('blockHash', "feature"),
        'asset_id': ('assetId', "function", 'getAssetId'),
        'asset_name': ('asset_name', "function", 'getAssetName'),
        'asset_symbol': ('symbol', "function", 'getSymbol'),
        'denomination': ('denomination', "function", 'getDenomination'),
        'asset_type': ('asset_type', "function", 'getAsset_type'),
        'amount': ('amount', "function", 'getAmount')
    }
}

# Functions
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

def getAssetId(utxo):
    asset = utxo.get('asset', {})
    return asset.get('assetId','')

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