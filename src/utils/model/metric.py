import pandas as pd


class BaseMetric:
    def __init__(self, blockchain, chain, name, transaction_type):
        self.blockchain = blockchain
        self.chain = chain
        self.name = name
        self.transaction_type = transaction_type  # Options: "transaction", "emitted_utxo", "consumed_utxo"

    def calculate(self, data: pd.DataFrame) -> float:
        """
        Override this method to define the metric calculation.

        :param data: A pandas DataFrame containing the blockchain data relevant to this metric.
        :return: The calculated metric value.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")
