from src.models.general_UTXO_model import GeneralUTXO

class AvalancheUTXO(GeneralUTXO):
    def __init__(self, utxoId, txHash, blockHash, addresses, assetId, asset_name, symbol, denomination, asset_type, amount):
        super().__init__(utxoId, txHash, addresses, None)
        self.blockHash = blockHash
        self.assetId = assetId
        self.asset_name = asset_name
        self.asset_symbol = symbol
        self.denomination = denomination
        self.asset_type = asset_type
        self.amount = amount
