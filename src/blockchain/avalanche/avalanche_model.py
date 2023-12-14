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
        super().__init__(txHash, blockHash, timestamp, None) 
        self.blockHeight = blockHeight
        self.txType = txType
        self.sourceChain = sourceChain
        self.destinationChain = destinationChain
        self.memo = memo
        self.total_input_value = total_input_value
        self.total_output_value = total_output_value

class Avalanche_P_Model(GeneralBlockchainModel):
    def __init__(self, txHash, txType, blockTimestamp, blockNumber, blockHash, memo, nodeId, subnetId, amountStaked, amountBurned):
        super().__init__(txHash, blockHash, blockTimestamp, None)  # P-Chain might not have a direct 'value' field
        self.txType = txType
        self.blockNumber = blockNumber
        self.memo = memo
        self.nodeId = nodeId
        self.subnetId = subnetId
        self.amountStaked = amountStaked
        self.amountBurned = amountBurned
        # Add other fields as necessary

