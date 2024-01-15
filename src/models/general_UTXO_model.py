class GeneralUTXO:
    def __init__(self, utxoId, txHash, addresses, value):
        self.utxoId = utxoId
        self.txHash = txHash
        self.addresses = addresses  # List of addresses associated with the UTXO
        self.value = value
        