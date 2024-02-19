
from utils.model.metric import CustomMetric
import pandas as pd


class NetworkEconomyEfficiency(CustomMetric):

    def __init__(self):
        super().__init__(blockchain='Avalanche', chain='x', name=
            'network_economy_efficiency', transaction_type='transaction',
            category='Economic Indicators', description='Description',
            display_name='Network Economy Efficiency')

    def calculate(self, data: pd.DataFrame) ->float:
        total_value_transacted = data['amountCreated'].replace('', '0').astype(
            float).sum()
        total_amount_burned = data['amountBurned'].replace('', '0').astype(
            float).sum()
        if total_amount_burned == 0:
            return None
        nee = (total_value_transacted / total_amount_burned if
            total_amount_burned else None)
        return nee
