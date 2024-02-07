
# workflow_manager.py
import os
import logging
from dotenv import load_dotenv

from utils.scripts.extraction import extract_avalanche_data, calculate_amount_unlocked, calculate_amount_created, getAssetId, getAssetName, getSymbol, getDenomination, getAsset_type, getAmount

from utils.scripts.mappers import data_mapper
from utils.scripts.helper import store_data

load_dotenv()

# Ensure the correct paths are included for imports
# sys.path.insert(0, os.environ.get("ROOT_DIRECTORY_LOCAL_PATH"))

class DataExtractionWorkflowManager:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.db_connection_string = os.environ.get("DATABASE_CONNECTION")

    
if __name__ == "__main__":
    # date = "2024-01-27"
    # manager = DataExtractionWorkflowManager()
    # manager.run_workflow(date)
    
     x_feature_mapping =  {
            'txHash' : ('txHash',"feature"),
            'blockHash':('blockHash',"feature"),
            'blockHeight': ('blockHeight',"feature"),
            'timestamp':('timestamp',"feature"),
            'memo':('memo',"feature"),
            'chainFormat':('chainFormat','feature'),
            'txType':('txType',"feature"),
            'amountUnlocked': ('amount_unlocked',"function","calculate_amount_unlocked"),
            'amountCreated': ('amount_created',"function", "calculate_amount_created")
        }
    
     x_emit_utxo_mapping = {
        'addresses': ('addresses',"feature"),
        'utxoId': ('utxoId',"feature"),
        'txHash':('txHash',"feature"),
        'txType':('txType',"feature"),
        'assetId': ('assetId',"function", 'getAssetId'),
        'asset_name': ('asset_name',"function", 'getAssetName'),
        'symbol': ('symbol',"function", 'getSymbol'),
        'denomination': ('denomination',"function", 'getDenomination'),
        'asset_type': ('asset_type',"function", 'getAsset_type'),
        'amount': ('amount',"function", 'getAmount')
    }
    
     x_consume_utxo_mapping = {
        'addresses': ('addresses',"feature"),
        'utxoId': ('utxoId',"feature"),
        'txHash':('txHash',"feature"),
        'txType':('txType',"feature"),
        'blockHash':('blockHash',"feature"),
        'assetId': ('assetId',"function", 'getAssetId'),
        'asset_name': ('asset_name',"function", 'getAssetName'),
        'symbol': ('symbol',"function", 'getSymbol'),
        'denomination': ('denomination',"function", 'getDenomination'),
        'asset_type': ('asset_type',"function", 'getAsset_type'),
        'amount': ('amount',"function", 'getAmount')
    }
    
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
        
     day = "2024-02-05"

     trxs, emitted_utxos, consumed_utxos = extract_avalanche_data(day)
    
     config = [
        x_feature_mapping,
        x_emit_utxo_mapping,
        x_consume_utxo_mapping,
        transformation_functions,
        utxo_functions
    ]
     trxs, emitted_utxos, consumed_utxos = data_mapper(config, trxs, emitted_utxos, consumed_utxos)
    
     store_data('x', day, trxs, emitted_utxos, consumed_utxos)