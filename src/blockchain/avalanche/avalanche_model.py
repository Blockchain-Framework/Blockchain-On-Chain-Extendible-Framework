# avalanche_model.py
from src.models.general_blockchain_model import GeneralBlockchainModel

class Avalanche_X_Model(GeneralBlockchainModel):
    def __init__(self, txHash, blockHash, blockHeight, timestamp, value, txType, memo, chainFormat):
        super().__init__(txHash, blockHash, timestamp, value)  # Initialize parent class
        self.txType = txType
        self.memo = memo
        self.chainFormat = chainFormat
        self.blockHeight = blockHeight
        
class Avalanche_C_Model(GeneralBlockchainModel):
    def __init__(self, txHash, blockHash, blockHeight, txType, timestamp, sourceChain, destinationChain, memo, total_input_value, total_output_value):
        super().__init__(txHash, blockHash, timestamp, None)  # value is None as it may need special calculation
        self.blockHeight = blockHeight
        self.txType = txType
        self.sourceChain = sourceChain
        self.destinationChain = destinationChain
        self.memo = memo
        total_input_value = total_input_value
        total_output_value = total_output_value
  
class Avalanche_P_Model(GeneralBlockchainModel):
    def __init__(self, txHash, blockHash, timestamp, value, txType, memo, chainFormat):
        super().__init__(txHash, blockHash, timestamp, value)  # Initialize parent class
        self.txType = txType
        self.memo = memo
        self.chainFormat = chainFormat