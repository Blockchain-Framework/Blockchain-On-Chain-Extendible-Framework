from GodSight.extraction.utils.scripts.model import get_models

# Mapping of function names to actual functions for dynamic invocation
def data_mapper(config, raw_trxs, raw_emitted_utxos, raw_consumed_utxos):
    trxs, emitted_utxos, consumed_utxos = [], [], []
    transaction_feature_mapping, emit_utxo_mapping, consume_utxo_mapping, functions= config
    TransactionModel, UTXOModel = get_models(config)
    trxs.extend([
        map_transaction(TransactionModel, transaction_feature_mapping, trx, functions).__dict__ for trx in raw_trxs
    ])
    
    emitted_utxos.extend([
        map_utxo(UTXOModel, emit_utxo_mapping, e_utxo, functions).__dict__ for e_utxo in raw_emitted_utxos
    ])
    
    consumed_utxos.extend([
        map_utxo(UTXOModel, consume_utxo_mapping, c_utxo, functions).__dict__ for c_utxo in raw_consumed_utxos
    ])
    
    return trxs, emitted_utxos, consumed_utxos

def map_utxo(UTXOModel, feature_mapping, utxo, functions):
    transformed_data = {}
    
    for general_attr, details in feature_mapping.items():
        api_attr, attr_type = details[:2]
        if attr_type == "feature":
            transformed_data[general_attr] = utxo.get(api_attr)
        elif attr_type == "function":
            function_name = details[2]
            if function_name in functions:
                transformed_data[general_attr] = functions[function_name](utxo)
    
    return UTXOModel(**transformed_data)
    
def map_transaction(TransactionModel, blockchain_feature_mapping,tx,functions):
    transformed_data = {}
    for general_attr, details in blockchain_feature_mapping.items():
        api_attr, attr_type = details[:2]
        
        if attr_type == "feature":
            transformed_data[general_attr] = tx.get(api_attr)
        elif attr_type == "function":
            function_name = details[2]
            if function_name in functions:
                transformed_data[general_attr] = functions[function_name](tx)

    return TransactionModel(**transformed_data)