model = {
    'trx_mapping': {
        'txHash': "feature",
        'blockHash': "feature",
        'blockHeight': "feature",
        'timestamp': "feature",
        'memo': "feature",
        'chainFormat': 'feature',
        'txType': "feature",
        'amountUnlocked': "function",
        'amountCreated': "function"
    },
    'emit_utxo_mapping': {
        'addresses': "feature",
        'utxoId': "feature",
        'txHash': "feature",
        'txType': "feature",
        'assetId': "function",
        'asset_name': "function",
        'symbol': "function",
        'denomination': "function",
        'asset_type': "function",
        'amount': "function"
    },
    'consume_utxo_mapping': {
        'addresses': "feature",
        'utxoId': "feature",
        'txHash': "feature",
        'txType': "feature",
        'blockHash': "feature",
        'assetId': "function",
        'asset_name': "function",
        'symbol': "function",
        'denomination': "function",
        'asset_type': "function",
        'amount': "function"
    }
}
