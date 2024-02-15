import pandas as pd
from ...utils.model.metric import CustomMetric

class TransactionPerSecond(CustomMetric):

    def __init__(self):
        super().__init__(blockchain='Avalanche', chain='x', name=
            'trx_per_second', transaction_type='transaction', category=
            'Economic Indicators', description='Description')

    def calculate(self, data: pd.DataFrame) ->float:
        count = data.shape[0]
        if count > 0:
            return count / 86400
        else:
            return 0


class TotalTransactions(CustomMetric):
    def __init__(self):
        super().__init__(
            blockchain='Avalanche', 
            chain='x', 
            name='total_trxs', 
            transaction_type='transaction', 
            category='Economic Indicators', 
            description='Calculate the total number of transactions for a given subchain and date.'
        )

    def calculate(self, data: pd.DataFrame) -> float:
        """
        Calculate the total number of transactions using the provided data.

        :param data: A pandas DataFrame containing the blockchain data relevant to this metric.
        :return: The total number of transactions.
        """
        if data is not None and not data.empty:
            count = data.shape[0]
            return count
        return 0

class AverageTransactionAmount(CustomMetric):
    def __init__(self):
        super().__init__(
            blockchain='Avalanche',
            chain='x',
            name='avg_trx_amount',
            transaction_type='consumed_utxo',  # Assuming this metric is specific to consumed UTXOs
            category='Economic Indicators',
            description='Calculate the average transaction amount for a specified date.'
        )

    def calculate(self, data: pd.DataFrame) -> float:
        """
        Calculate the average transaction amount using the provided data.

        :param data: A pandas DataFrame containing the transaction amounts and count.
        :return: The average transaction amount.
        """
        if data is not None and not data.empty:
            total_amount = data['amount'].sum()
            trx_count = len(data)
            if trx_count > 0:
                return total_amount / trx_count
            else:
                logging.info("No transactions found for the given data.")
                return 0
        return 0

