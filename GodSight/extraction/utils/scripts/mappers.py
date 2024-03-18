from extraction.utils.database.services import fetch_feature_mappings
from extraction.utils.scripts.model import get_models

# Mapping of function names to actual functions for dynamic invocation
def data_mapper(mapper_config, raw_trxs, raw_emitted_utxos, raw_consumed_utxos, config):
    trxs, emitted_utxos, consumed_utxos = [], [], []
    transaction_feature_mapping, emit_utxo_mapping, consume_utxo_mapping, functions= mapper_config
    print(3)
    TransactionModel, UTXOModel = get_models(config)
    print(4)
    trxs.extend([
        map_transaction(TransactionModel, transaction_feature_mapping, trx, functions).__dict__ for trx in raw_trxs
    ])
    
    emitted_utxos.extend([
        map_utxo(UTXOModel, emit_utxo_mapping, e_utxo, functions).__dict__ for e_utxo in raw_emitted_utxos
    ])
    
    consumed_utxos.extend([
        map_utxo(UTXOModel, consume_utxo_mapping, c_utxo, functions).__dict__ for c_utxo in raw_consumed_utxos
    ])

    print(5)
    
    return trxs, emitted_utxos, consumed_utxos

def map_utxo(UTXOModel, feature_mapping, utxo, functions):
    transformed_data = {}

    print('ooooooooo')
    
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


def transform_data(blockchain, sub_chain, transactions, emitted_utxos, consumed_utxos, functions, config):
    # Fetch feature mappings from the database
    feature_mappings = fetch_feature_mappings(config, blockchain, sub_chain)

    # Define a helper function for applying transformations
    def apply_transformation(data, mappings):
        transformed = []
        for item in data:
            transformed_item = {}
            for mapping in mappings:
                source_field = mapping['sourceField']
                target_field = mapping['targetField']
                if mapping['type'] == 'feature':
                    transformed_item[source_field] = item.get(target_field, None)
                elif mapping['type'] == 'function':
                    # Assuming you have a way to dynamically call the function based on 'info'
                    func_name = mapping['info']
                    if func_name in functions:
                        transformed_item[source_field] = functions[func_name](item)
                    else:
                        # Handle the case where the function does not exist
                        transformed_item[target_field] = None
            transformed.append(transformed_item)
        return transformed

    # Apply transformations
    transformed_transactions = apply_transformation(transactions, feature_mappings['transaction_mappings'])
    transformed_emitted_utxos = apply_transformation(emitted_utxos, feature_mappings['emitted_mappings'])
    transformed_consumed_utxos = apply_transformation(consumed_utxos, feature_mappings['consumed_mappings'])

    return transformed_transactions, transformed_emitted_utxos, transformed_consumed_utxos