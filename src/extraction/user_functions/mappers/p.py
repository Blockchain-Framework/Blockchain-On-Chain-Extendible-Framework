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
        'addresses': ('addresses', "feature"),
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
        'addresses': ('addresses', "feature"),
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