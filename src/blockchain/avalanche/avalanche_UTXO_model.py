from src.models.general_UTXO_model import GeneralUTXO

class AvalancheUTXO(GeneralUTXO):
    def __init__(self, utxoId, txHash, outputIndex, addresses, amount, assetId, assetName, assetSymbol, assetDenomination, utxoType, consumingTxHash="", consumingTxTimestamp=0, credentials=None):
        super().__init__(utxoId, txHash, outputIndex, addresses, amount, assetId)
        self.txHash = txHash
        self.assetName = assetName
        self.assetSymbol = assetSymbol
        self.assetDenomination = assetDenomination
        self.utxoType = utxoType
        self.consumingTxHash = consumingTxHash
        self.consumingTxTimestamp = consumingTxTimestamp
        self.credentials = credentials if credentials is not None else []


