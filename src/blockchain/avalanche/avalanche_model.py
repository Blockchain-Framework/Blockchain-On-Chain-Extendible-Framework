# avalanche_model.py
from .general_blockchain_model import GeneralBlockchainModel

class Avalanche_X_Model(GeneralBlockchainModel):
    def __init__(self, txHash, blockHash, timestamp, value, txType, memo, chainFormat):
        self.memo = memo
        self.chainFormat = chainFormat
        self.txType = txType
