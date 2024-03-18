import pandas as pd

from computation.config.config import Config


class BaseMetric:
    def __init__(self, name, category, description):
        self.name = name
        self.category = category
        self.description = description

    def calculate(self, blockchain: str, subchain: str, date: str, config : Config) -> float:
        """
        Override this method to define the metric calculation.

        :param data: A pandas DataFrame containing the blockchain data relevant to this metric.
        :return: The calculated metric value.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")


class CustomMetric:
    def __init__(self, blockchain, chain, name, display_name, transaction_type, category, description):
        self.blockchain = blockchain
        self.chain = chain
        self.name = name
        self.display_name = display_name
        self.transaction_type = transaction_type  # Options: "transaction", "emitted_utxo", "consumed_utxo"
        self.category = category
        self.description = description

    def calculate(self, data: pd.DataFrame) -> float:
        """
        Override this method to define the metric calculation.

        :param data: A pandas DataFrame containing the blockchain data relevant to this metric.
        :return: The calculated metric value.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")
