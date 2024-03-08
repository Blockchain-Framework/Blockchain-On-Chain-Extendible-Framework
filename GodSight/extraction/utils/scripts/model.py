# class TransactionModel:
#     def __init__(self, **kwargs):
#         self.txHash = kwargs.get('txHash')
#         self.blockHash = kwargs.get('blockHash')
#         self.timestamp = kwargs.get('timestamp')
#         self.blockHeight = kwargs.get('blockHeight')
#         self.txType = kwargs.get('txType')
#         self.memo = kwargs.get('memo')
#         self.nodeId = kwargs.get('nodeId')
#         self.chainFormat = kwargs.get('chainFormat')
#
#         # Features for Account - based Blockchains(e.g., Ethereum, Avalanche, BNB Chain)
#         self.gasPrice = kwargs.get('gasPrice')
#         self.amountCreated = kwargs.get('amountCreated')
#
#         # Features for Cross - Chain and Multi-Chain Ecosystems (e.g., Cosmos, Polkadot):
#         self.sourceChain = kwargs.get('sourceChain')
#         self.destinationChain = kwargs.get('destinationChain')
#         self.subnetId = kwargs.get('subnetId')
#
#         # Features for Proof - of - Stake Blockchains(e.g., Cosmos, Polkadot, Solana, Avalanche):
#         self.amountStaked = kwargs.get('amountStaked')
#         self.estimatedReward = kwargs.get('estimatedReward')
#         self.startTimestamp = kwargs.get('startTimestamp')  # (for staking / delegation period)
#         self.endTimestamp = kwargs.get('endTimestamp')  # (for staking / delegation period)
#         self.delegationFeePercent = kwargs.get('delegationFeePercent')
#
#         # Features for Blockchains with Token Burning (e.g., Ethereum, Binance Smart Chain):
#         self.amountBurned = kwargs.get('amountBurned')
#
#         # Smart Contract - related Features:
#         self.contractAddress = kwargs.get('contractAddress')  # ( for contract interactions)
#         self.functionSignature = kwargs.get('functionSignature')  # ( for identifying the called function)
#         self.inputData = kwargs.get('inputData')  # (for function input parameters)
#         self.outputData = kwargs.get('outputData')  # (for function output data)
#
#         # Governance - related Features:
#         self.proposalId = kwargs.get('proposalId')  # (for on - chain governance proposals)
#         self.voteOption = kwargs.get('voteOption')  # (for vote choices)
#         self.votingPower = kwargs.get('votingPower')  # (for weighted voting)
#
#         # Privacy - related Features:
#         self.isPrivate = kwargs.get('proposalId')  # (for identifying private / shielded transactions)
#         self.privacyType = kwargs.get('proposalId')  # (e.g., zk - SNARKs, ring signatures)
#
#         # Fee - related Features:
#         self.feeAmount = kwargs.get('feeAmount')  # (for transaction fees paid)
#         self.feeToken = kwargs.get('feeToken')  # (for the token used to pay fees)
#
#         # Account - relate Features:
#         self.senderAddress = kwargs.get('senderAddress')
#         self.recipientAddress = kwargs.get('recipientAddress')
#
#         # Block Producer - related Features:
#         self.blockProducer = kwargs.get('blockProducer')  # (for identifying the block producer)
#         self.blockProducerReward = kwargs.get('blockProducerReward')  # (for block rewards)
#
#         # Features for UTXO - based Blockchains(e.g., Bitcoin, Litecoin, Dogecoin):
#         self.amountUnlocked = kwargs.get('amountUnlocked')  # (for inputs)
#         self.rewardAddresses = kwargs.get('rewardAddresses')  # (for mining rewards)
#
# class UTXOModel():
#     def __init__(self, **kwargs):
#         self.utxoId = kwargs.get('utxoId')
#         self.txHash = kwargs.get('txHash')
#         self.txType = kwargs.get('txType')
#         self.addresses = kwargs.get('addresses')
#         self.value = kwargs.get('value')
#         self.blockHash = kwargs.get('blockHash')
#         self.assetId = kwargs.get('assetId')
#         self.asset_name = kwargs.get('asset_name')
#         self.asset_symbol = kwargs.get('symbol')
#         self.denomination = kwargs.get('denomination')
#         self.asset_type = kwargs.get('asset_type')
#         self.amount = kwargs.get('amount')
#
# class GeneralModel:
#     def __init__(self, **kwargs):
#         # General Features(Applicable to Most Blockchain Types):
#         self.txHash = kwargs.get('txHash')
#         self.blockHash = kwargs.get('blockHash')
#         self.timestamp = kwargs.get('timestamp')
#         self.blockHeight = kwargs.get('blockHeight')
#         self.txType = kwargs.get('txType')
#         self.memo = kwargs.get('memo')
#         self.nodeId = kwargs.get('nodeId')
#         self.chainFormat = kwargs.get('chainFormat')
#
#         # Features for Account - based Blockchains(e.g., Ethereum, Avalanche, BNB Chain)
#         self.gasPrice = kwargs.get('gasPrice')
#         self.amountCreated = kwargs.get('amountCreated')
#
#         # Features for Cross - Chain and Multi-Chain Ecosystems (e.g., Cosmos, Polkadot):
#         self.sourceChain = kwargs.get('sourceChain')
#         self.destinationChain = kwargs.get('destinationChain')
#         self.subnetId = kwargs.get('subnetId')
#
#         # Features for Proof - of - Stake Blockchains(e.g., Cosmos, Polkadot, Solana, Avalanche):
#         self.amountStaked = kwargs.get('amountStaked')
#         self.estimatedReward = kwargs.get('estimatedReward')
#         self.startTimestamp = kwargs.get('startTimestamp')  # (for staking / delegation period)
#         self.endTimestamp = kwargs.get('endTimestamp')  # (for staking / delegation period)
#         self.delegationFeePercent = kwargs.get('delegationFeePercent')
#
#         # Features for Blockchains with Token Burning (e.g., Ethereum, Binance Smart Chain):
#         self.amountBurned = kwargs.get('amountBurned')
#
#         # Smart Contract - related Features:
#         self.contractAddress = kwargs.get('contractAddress')  # ( for contract interactions)
#         self.functionSignature = kwargs.get('functionSignature')  # ( for identifying the called function)
#         self.inputData = kwargs.get('inputData')  # (for function input parameters)
#         self.outputData = kwargs.get('outputData')  # (for function output data)
#
#         # Governance - related Features:
#         self.proposalId = kwargs.get('proposalId')  # (for on - chain governance proposals)
#         self.voteOption = kwargs.get('voteOption')  # (for vote choices)
#         self.votingPower = kwargs.get('votingPower')  # (for weighted voting)
#
#         # Privacy - related Features:
#         self.isPrivate = kwargs.get('proposalId')  # (for identifying private / shielded transactions)
#         self.privacyType = kwargs.get('proposalId')  # (e.g., zk - SNARKs, ring signatures)
#
#         # Fee - related Features:
#         self.feeAmount = kwargs.get('feeAmount')  # (for transaction fees paid)
#         self.feeToken = kwargs.get('feeToken')  # (for the token used to pay fees)
#
#         # Account - relate Features:
#         self.senderAddress = kwargs.get('senderAddress')
#         self.recipientAddress = kwargs.get('recipientAddress')
#
#         # Block Producer - related Features:
#         self.blockProducer = kwargs.get('blockProducer')  # (for identifying the block producer)
#         self.blockProducerReward = kwargs.get('blockProducerReward')  # (for block rewards)
#
#         # Features for UTXO - based Blockchains(e.g., Bitcoin, Litecoin, Dogecoin):
#         self.amountUnlocked = kwargs.get('amountUnlocked')  # (for inputs)
#         self.rewardAddresses = kwargs.get('rewardAddresses')  # (for mining rewards)
#         self.inputAddress = kwargs.get('inputAddress')
#         self.inputAmount = kwargs.get('inputAmount')
#         self.outputAddress = kwargs.get('outputAddress')
#         self.outputAmount = kwargs.get('outputAmount')
#
#         self.input_utxo_count = kwargs.get('input_utxo_count')
#         self.input_utxo_amount_mean = kwargs.get('input_utxo_amount_mean')
#         self.input_utxo_amount_median = kwargs.get('input_utxo_amount_median')
#         self.input_utxo_amount_min = kwargs.get('input_utxo_amount_min')
#         self.input_utxo_amount_max = kwargs.get('input_utxo_amount_max')
#         self.input_utxo_amount_std_dev = kwargs.get('input_utxo_amount_std_dev')
#
#         self.output_utxo_count = kwargs.get('output_utxo_count')
#         self.output_utxo_amount_mean = kwargs.get('output_utxo_amount_mean')
#         self.output_utxo_amount_median = kwargs.get('output_utxo_amount_median')
#         self.output_utxo_amount_min = kwargs.get('output_utxo_amount_min')
#         self.output_utxo_amount_max = kwargs.get('output_utxo_amount_max')
#         self.output_utxo_amount_std_dev = kwargs.get('output_utxo_amount_std_dev')

from GodSight.extraction.utils.database.services import load_model_fields

def create_model_class(model_name, model_fields):
    field_definitions = '\n'.join([f"    {field_name} = None" for field_name in model_fields.keys()])
    class_definition = f"""
class {model_name}:
{field_definitions}

    def __init__(self, **kwargs):
        for field, value in kwargs.items():
            setattr(self, field, value)
"""
    return type(model_name, (object,), dict(__module__=__name__, __doc__=class_definition))

def get_models(config):
    # Load transaction model fields
    transaction_model_fields = load_model_fields('transaction_model', config)

    # Load utxo model fields
    utxo_model_fields = load_model_fields('utxo_model', config)

    # Create TransactionModel class
    TransactionModel = create_model_class('TransactionModel', transaction_model_fields)

    # Create UTXOModel class
    UTXOModel = create_model_class('UTXOModel', utxo_model_fields)

    return TransactionModel, UTXOModel