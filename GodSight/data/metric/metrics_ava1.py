import pandas as pd
from GodSight.utils.model.metric import CustomMetric


class Total_stacked_Amount(CustomMetric):

    def __init__(self):
        super().__init__(blockchain='Avalanche', chain='p', name=
        'total_stacked_amount', transaction_type='transaction',
                         category='Economic Indicators', description='Description',
                         display_name='Total Stacked Amount')

    def calculate(self, data: pd.DataFrame) -> float:
        total_staked = data['amount_staked'].sum()
        if total_staked > 0:
            return total_staked
        else:
            return None


class TotalBurnedAmount(CustomMetric):

    def __init__(self):
        super().__init__(blockchain='Avalanche', chain='p', name=
        'total_burned_amount', transaction_type='transaction',
                         category='Economic Indicators', description='Description',
                         display_name='Total Burned Amount')

    def calculate(self, data: pd.DataFrame) -> float:
        total_burned = data['amount_burned'].sum()
        if total_burned > 0:
            return total_burned
        else:
            return None


class stackingDynamicIndex(CustomMetric):

    def __init__(self):
        super().__init__(blockchain='Avalanche', chain='p', name=
        'staking_dynamics_index', transaction_type='transaction',
                         category='Economic Indicators', description='Description',
                         display_name='Staking Dynamics Index')

    def calculate(self, data: pd.DataFrame) -> float:
        total_amount_staked = data['amount_staked'].sum()
        total_amount_burned = data['amount_burned'].sum()
        total_estimated_reward = data['estimated_reward'].replace('', '0'
                                                                 ).astype(float).sum()
        avg_delegation_fee_percent = data['delegation_fee_percent'].replace('',
                                                                          '0').astype(float).mean()
        if total_amount_burned == 0:
            return None
        sdi = (total_amount_staked * total_estimated_reward /
               total_amount_burned * avg_delegation_fee_percent)
        return sdi


class StakingEngagementIndex(CustomMetric):

    def __init__(self):
        super().__init__(blockchain='Avalanche', chain='p', name=
        'staking_engagement_index', transaction_type='transaction',
                         category='Economic Indicators', description='Description',
                         display_name='Staking Engagement Index')

    def calculate(self, data: pd.DataFrame) -> float:
        total_amount_staked = data['amount_staked'].sum()
        total_estimated_reward = data['estimated_reward'].replace('', '0'
                                                                 ).astype(float).sum()
        if total_amount_staked == 0:
            return None
        sei = (total_estimated_reward / total_amount_staked if
               total_amount_staked else 0)
        return sei




