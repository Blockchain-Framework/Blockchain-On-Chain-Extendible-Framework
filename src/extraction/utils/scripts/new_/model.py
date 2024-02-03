class GeneralTransactionModel:
    def __init__(self, **kwargs):
        self.txHash = kwargs.get('txHash')
        self.blockHash = kwargs.get('blockHash')
        self.timestamp = kwargs.get('timestamp')
        self.blockHeight = kwargs.get('blockHeight')
        self.txType = kwargs.get('txType')
        self.memo = kwargs.get('memo')
        self.chainFormat = kwargs.get('chainFormat')
        self.amountUnlocked = kwargs.get('amountUnlocked')
        self.amountCreated = kwargs.get('amountCreated')
        self.sourceChain = kwargs.get('sourceChain')
        self.destinationChain = kwargs.get('destinationChain')
        self.rewardAddresses = kwargs.get('rewardAddresses')
        self.estimatedReward = kwargs.get('estimatedReward')
        self.startTimestamp = kwargs.get('startTimestamp')
        self.endTimestamp = kwargs.get('endTimestamp')
        self.delegationFeePercent = kwargs.get('delegationFeePercent')
        self.nodeId = kwargs.get('nodeId')
        self.subnetId = kwargs.get('subnetId')
        self.value = kwargs.get('value')
        self.amountStaked = kwargs.get('amountStaked')
        self.amountBurned = kwargs.get('amountBurned')
    

class GeneralUTXOModel():
    def __init__(self, utxoId, txHash, blockHash, txType, addresses, value, assetId, asset_name, symbol, denomination, asset_type, amount):
        self.utxoId = utxoId
        self.txHash = txHash
        self.txType = txType
        self.addresses = addresses 
        self.value = value
        self.blockHash = blockHash
        self.assetId = assetId
        self.asset_name = asset_name
        self.asset_symbol = symbol
        self.denomination = denomination
        self.asset_type = asset_type
        self.amount = amount