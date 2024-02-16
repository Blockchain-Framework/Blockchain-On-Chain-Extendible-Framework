import pandas as pd
from utils.model.metric import CustomMetric


class TransactionPerSecond(CustomMetric):

    def __init__(self):
        super().__init__(blockchain='Avalanche', chain='x', name=
        'trx_per_second', transaction_type='transaction', category=
                         'Economic Indicators', description='Description')

    def calculate(self, data: pd.DataFrame) -> float:
        count = data.shape[0]
        if count > 0:
            return count / 86400
        else:
            return 0


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


