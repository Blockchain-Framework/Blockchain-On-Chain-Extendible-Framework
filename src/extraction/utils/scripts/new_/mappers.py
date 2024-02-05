from utils.scripts.new_.model import GeneralTransactionModel
from utils.scripts.new_.model import GeneralUTXOModel
from utils.scripts.new_.helper import calculate_amount_unlocked, calculate_amount_created, getAssetId, getAssetName, getSymbol, getDenomination, getAsset_type, getAmount

# Mapping of function names to actual functions for dynamic invocation
transformation_functions = {
    "calculate_amount_unlocked": calculate_amount_unlocked,
    "calculate_amount_created": calculate_amount_created,
}

utxo_functions = {
    "getAssetId": getAssetId,
    "getAssetName":getAssetName,
    "getSymbol":getSymbol,
    "getDenomination":getDenomination,
    "getAsset_type":getAsset_type,
    "getAmount":getAmount
}


def map_utxo(feature_mapping, utxo, txHash, txType, blockHash):
    transformed_data = {
        'txHash': txHash,
        'txType': txType,
        'blockHash': blockHash
    }
    
    for general_attr, details in feature_mapping.items():
        api_attr, attr_type = details[:2]
        if attr_type == "feature":
            transformed_data[general_attr] = utxo.get(api_attr)
        elif attr_type == "function":
            function_name = details[2]
            if function_name in transformation_functions:
                transformed_data[general_attr] = transformation_functions[function_name](utxo)
    
    GeneralUTXOModel(**transformed_data)
    
def map_transaction(blockchain_feature_mapping,tx):
    transformed_data = {}
    for general_attr, details in blockchain_feature_mapping.items():
        api_attr, attr_type = details[:2]
        
        if attr_type == "feature":
            transformed_data[general_attr] = tx.get(api_attr)
        elif attr_type == "function":
            function_name = details[2]
            if function_name in transformation_functions:
                transformed_data[general_attr] = transformation_functions[function_name](tx)
    
    GeneralTransactionModel(**transformed_data)
