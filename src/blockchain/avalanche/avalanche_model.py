# avalanche_model.py
from src.models.general_blockchain_model import GeneralBlockchainModel

class Avalanche_X_Model(GeneralBlockchainModel):
    def __init__(self, txHash, blockHash, timestamp, value, txType, memo, chainFormat):
        super().__init__(txHash, blockHash, timestamp, value)  # Initialize parent class
        self.txType = txType
        self.memo = memo
        self.chainFormat = chainFormat