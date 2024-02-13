config = {
    'trx_mapping': {
        'txHash': ('txHash', "feature"),
        'blockHash': ('blockHash', "feature"),
        'blockHeight': ('blockHeight', "feature"),
        'txType': ('txType', "feature"),
        'timestamp': ('timestamp', "feature"),
        'sourceChain': ('sourceChain', "feature"),
        'destinationChain': ('destinationChain', "feature"),
        'memo': ('memo', "feature"),
        'amountUnlocked': ('amount_unlocked', "function", "calculate_amount_unlocked"),
        'amountCreated': ('amount_created', "function", "calculate_amount_created")
    },

    'emit_utxo_mapping': {
        'addresses': ('addresses', "function", 'getAddress'),
        'txHash': ('txHash', "feature"),
        'txType': ('txType', "feature"),
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