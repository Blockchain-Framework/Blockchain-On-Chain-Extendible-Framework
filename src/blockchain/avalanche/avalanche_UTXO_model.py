from src.models.general_UTXO_model import GeneralUTXO

class AvalancheUTXO(GeneralUTXO):
    def __init__(self, utxoId, txHash, outputIndex, addresses, amount, assetId, assetName, assetSymbol, assetDenomination):
        super().__init__(utxoId, txHash, outputIndex, addresses, amount, assetId)
        self.assetName = assetName
        self.assetSymbol = assetSymbol
        self.assetDenomination = assetDenomination
