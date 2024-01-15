# avalanche_model.py
from src.models.general_blockchain_model import GeneralBlockchainModel
from src.blockchain.avalanche.avalanche_UTXO_model import AvalancheUTXO
class Avalanche_X_Model(GeneralBlockchainModel):
    def __init__(self, txHash, blockHash, blockHeight, txType, timestamp , memo, chainFormat,  amountUnlocked, amountCreated):
        super().__init__(txHash, blockHash, timestamp, None)
        self.blockHeight = blockHeight
        self.txType = txType
        self.memo = memo
        self.chainFormat = chainFormat
        self.amountUnlocked = amountUnlocked
        self.amountCreated = amountCreated
        
class Avalanche_C_Model(GeneralBlockchainModel):
    def __init__(self, txHash, blockHash, blockHeight, txType, timestamp, sourceChain, destinationChain, memo,  amountUnlocked, amountCreated):
        super().__init__(txHash, blockHash, timestamp, None)
        self.blockHeight = blockHeight
        self.txType = txType
        self.sourceChain = sourceChain
        self.destinationChain = destinationChain
        self.memo = memo
        self.amountUnlocked = amountUnlocked
        self.amountCreated = amountCreated

class EVMInput:
    def __init__(self, asset, fromAddress, credentials):
        self.asset = Asset(**asset)
        self.fromAddress = fromAddress
        self.credentials = credentials

class Asset:
    def __init__(self, assetId, name, symbol, denomination, type, amount):
        self.assetId = assetId
        self.name = name
        self.symbol = symbol
        self.denomination = denomination
        self.type = type
        self.amount = amount

class Avalanche_P_Model(GeneralBlockchainModel):
    def __init__(self, txHash, txType, blockTimestamp, blockNumber, blockHash, memo, nodeId, active_adreesess, subnetId, amountStaked, amountBurned, active_senders, consumedUtxos=[], emittedUtxos=[]):
        super().__init__(txHash, blockHash, blockTimestamp, None)
        self.txType = txType
        self.blockNumber = blockNumber
        self.memo = memo
        self.nodeId = nodeId
        self.subnetId = subnetId
        self.amountStaked = amountStaked
        self.amountBurned = amountBurned
        # self.consumedUtxos = [AvalancheUTXO(**utxo) for utxo in consumedUtxos]
        # self.emittedUtxos = [AvalancheUTXO(**utxo) for utxo in emittedUtxos]
        self.active_senders = active_senders
        self.active_adreesess = active_adreesess



