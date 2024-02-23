config = {
    'trx_mapping': {
        'txHash': ('txHash', "feature"),
        'txType': ('txType', "feature"),
        'timestamp': ('blockTimestamp', "feature"),
        'blockHeight': ('blockNumber', "feature"),
        'blockHash': ('blockHash', "feature"),
        'sourceChain': ('sourceChain', "feature"),
        'destinationChain': ('destinationChain', "feature"),
        'memo': ('memo', "feature"),
        'rewardAddresses': ('rewardAddresses', "feature"),
        'estimatedReward': ('estimatedReward', "feature"),
        'startTimestamp': ('startTimestamp', "feature"),
        'endTimestamp': ('endTimestamp', "feature"),
        'delegationFeePercent': ('delegationFeePercent', "feature"),
        'nodeId': ('nodeId', "feature"),
        'subnetId': ('subnetId', "feature"),
        'value': ('value', "feature"),
        'amountStaked': ('amountStaked', "function", "calculate_amount_staked"),
        'amountBurned': ('amountBurned', "function", "calculate_amount_burned")
    },

    'emit_utxo_mapping': {
        'addresses': ('addresses', "function", 'getAddress'),
        'utxoId': ('utxoId', "feature"),
        'txHash': ('txHash', "feature"),
        'txType': ('txType', "feature"),
        'blockHash': ('blockHash', "feature"),
        'assetId': ('assetId', "function", 'getAssetId'),
        'asset_name': ('asset_name', "function", 'getAssetName'),
        'symbol': ('symbol', "function", 'getSymbol'),
        'denomination': ('denomination', "function", 'getDenomination'),
        'asset_type': ('asset_type', "function", 'getAsset_type'),
        'amount': ('amount', "function", 'getAmount')
    },

    'consume_utxo_mapping': {
        'addresses': ('toAddress', "function", "getAddress"),
        'utxoId': ('utxoId', "feature"),
        'txHash': ('txHash', "feature"),
        'txType': ('txType', "feature"),
        'blockHash': ('blockHash', "feature"),
        'assetId': ('assetId', "function", 'getAssetId'),
        'asset_name': ('asset_name', "function", 'getAssetName'),
        'symbol': ('symbol', "function", 'getSymbol'),
        'denomination': ('denomination', "function", 'getDenomination'),
        'asset_type': ('asset_type', "function", 'getAsset_type'),
        'amount': ('amount', "function", 'getAmount')
    },
}


def calculate_amount_staked(transation):
    amounts = transation.get("amountStaked", [])
    total_value = sum(int(asset['amount']) for asset in amounts) / 10 ** 9  # Convert to AVAX
    return total_value


def calculate_amount_burned(transation):
    amounts = transation.get("amountBurned", [])
    total_value = sum(int(asset['amount']) for asset in amounts) / 10 ** 9  # Convert to AVAX
    return total_value


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

def getAddress(utxo):
    asset = utxo.get('asset', {})
    return asset.get('addresses',[])