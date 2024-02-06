from utils.scripts.new_.model import GeneralTransactionModel
from utils.scripts.new_.model import GeneralUTXOModel

# Mapping of function names to actual functions for dynamic invocation


def data_mapper(config, raw_trxs, raw_emitted_utxos, raw_consumed_utxos):
    trxs, emitted_utxos, consumed_utxos = [], [], []
    transaction_feature_mapping, emit_utxo_mapping, consume_utxo_mapping, transformation_functions, utxo_functions= config
    
    # Iterating through each transaction in the day
    # for trx in raw_trxs:
    #     trxs, emitted_utxos, consumed_utxos = data_mapper_for_trx(trx, trxs, emitted_utxos, consumed_utxos, transaction_feature_mapping, emit_utxo_mapping, consume_utxo_mapping, emitted_utxos_keys, consumed_utxos_keys)
    trxs.extend([
        map_transaction(transaction_feature_mapping, trx, transformation_functions).__dict__ for trx in raw_trxs
    ])
    
    emitted_utxos.extend([
        map_utxo(emit_utxo_mapping, e_utxo, utxo_functions).__dict__ for e_utxo in raw_emitted_utxos
    ])
    
    consumed_utxos.extend([
        map_utxo(consume_utxo_mapping, c_utxo, utxo_functions).__dict__ for c_utxo in raw_consumed_utxos
    ])
    
    return trxs, emitted_utxos, consumed_utxos
    
# def data_mapper_for_trx(tx, trxs, emitted_utxos, consumed_utxos, transaction_feature_mapping, emit_utxo_mapping, consume_utxo_mapping):
#     txHash = tx.get(transaction_feature_mapping['txHash'][0],'')
#     blockHash = tx.get(transaction_feature_mapping['blockHash'][0],'')
#     txType= tx.get(transaction_feature_mapping['txType'][0],'')
    
#     mapped_transaction = map_transaction(transaction_feature_mapping, tx)
#     trxs.append(mapped_transaction.__dict__)
    
#     for key in emitted_utxos_keys:
#         if key in tx:
#             emitted_utxos.extend([
#                 map_utxo(emit_utxo_mapping, e_utxo, txHash, txType, blockHash).__dict__ for e_utxo in tx.get(key, [])
#             ])
#             break  # Stop after finding the first matching key
    
#     # Map consumed UTXOs
#     for key in consumed_utxos_keys:
#         if key in tx:
#             consumed_utxos.extend([
#                 map_utxo(consume_utxo_mapping, c_utxo, txHash, txType, blockHash).__dict__ for c_utxo in tx.get(key, [])
#             ])
#             break  # Stop after finding the first matching key
    
#     return trxs, emitted_utxos, consumed_utxos

def map_utxo(feature_mapping, utxo,functions):
    # print(utxo)
    # print()
    transformed_data = {}
    
    for general_attr, details in feature_mapping.items():
        api_attr, attr_type = details[:2]
        if attr_type == "feature":
            transformed_data[general_attr] = utxo.get(api_attr)
        elif attr_type == "function":
            function_name = details[2]
            if function_name in functions:
                transformed_data[general_attr] = functions[function_name](utxo)
    
    return GeneralUTXOModel(**transformed_data)
    
def map_transaction(blockchain_feature_mapping,tx,functions):
    transformed_data = {}
    for general_attr, details in blockchain_feature_mapping.items():
        api_attr, attr_type = details[:2]
        
        if attr_type == "feature":
            transformed_data[general_attr] = tx.get(api_attr)
        elif attr_type == "function":
            function_name = details[2]
            if function_name in functions:
                transformed_data[general_attr] = functions[function_name](tx)
    
    return GeneralTransactionModel(**transformed_data)
