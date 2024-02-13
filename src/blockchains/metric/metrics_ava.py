
from src.utils.model.metric import BaseMetric
import pandas as pd


class TransactionPerSecond(BaseMetric):
    def __init__(self):
        # Initialize the base class with metric-specific details
        super().__init__(
            blockchain="Avalanche",
            chain="x",
            name="trx_per_second",
            transaction_type="transaction"
        )

    def calculate(self, data: pd.DataFrame) -> float:
        count = data.drop_duplicates().shape[0]
        if count > 0:
            return count / 86400
        else:
            return 0
