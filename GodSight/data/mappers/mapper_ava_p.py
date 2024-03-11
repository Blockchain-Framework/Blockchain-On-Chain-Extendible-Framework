config = {
    'trx_mapping': {
        'tx_hash': ('txHash', "feature"),
        'tx_type': ('txType', "feature"),
        'timestamp': ('blockTimestamp', "feature"),
        'block_height': ('blockNumber', "feature"),
        'block_hash': ('blockHash', "feature"),
        'source_chain': ('sourceChain', "feature"),
        'destination_chain': ('destinationChain', "feature"),
        'memo': ('memo', "feature"),
        'reward_addresses': ('rewardAddresses', "feature"),
        'estimated_reward': ('estimatedReward', "feature"),
        'start_timestamp': ('startTimestamp', "feature"),
        'end_timestamp': ('endTimestamp', "feature"),
        'delegation_fee_percent': ('delegationFeePercent', "feature"),
        'node_id': ('nodeId', "feature"),
        'subnet_id': ('subnetId', "feature"),
        'amount_staked': ('amountStaked', "function", "calculate_amount_staked"),
        'amount_burned': ('amountBurned', "function", "calculate_amount_burned")
    },

    'emit_utxo_mapping': {
        'addresses': ('addresses', "function", 'getAddress'),
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
    },

    'consume_utxo_mapping': {
        'addresses': ('toAddress', "function", "getAddress"),
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