class GeneralUTXO:
    def __init__(self, utxoId, txHash, outputIndex, addresses, amount, assetId=None):
        self.utxoId = utxoId
        self.txHash = txHash
        self.outputIndex = outputIndex
        self.addresses = addresses  # List of addresses associated with the UTXO
        self.amount = amount  # Amount of the asset
        self.assetId = assetId  # Optional, for blockchains that use multiple asset types