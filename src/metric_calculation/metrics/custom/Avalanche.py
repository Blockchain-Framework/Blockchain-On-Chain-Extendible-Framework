import pandas as pd
from utils.model.metric import CustomMetric
class Total_stacked_Amount(CustomMetric):
    def __init__(self):
        super().__init__(blockchain='Avalanche', chain='p', name='total_stacked_amount', transaction_type='emitted_utxo', category='Economic Indicators', description='Description')

    def calculate(self, data: pd.DataFrame) ->float:
        
        total_staked = data['amountStaked'].sum()

        if total_staked > 0:
            return total_staked
        else:
            return None
        
class TotalBurnedAmount(CustomMetric):
    def __init__(self):
        super().__init__(blockchain='Avalanche', chain='p', name='total_burned_amount', transaction_type='consumed_utxo', category='Economic Indicators', description='Description')

    def calculate(self, data: pd.DataFrame) ->float:
        
        total_burned = data['amountBurned'].sum()

        if total_burned > 0:
            return total_burned
        else:
            return None
        
class stackingDynamicIndex(CustomMetric):
    def __init__(self):
        super().__init__(blockchain='Avalanche', chain='p', name='staking_dynamics_index', transaction_type='emitted_utxo', category='Economic Indicators', description='Description')

    def calculate(self, data: pd.DataFrame) ->float:
        # Assuming 'amountStaked', 'amountBurned', 'estimatedReward', and 'delegationFeePercent' are columns in the DataFrame
        total_amount_staked = data['amountStaked'].sum()
        total_amount_burned = data['amountBurned'].sum()
        total_estimated_reward = data['estimatedReward'].replace('', '0').astype(float).sum()
        avg_delegation_fee_percent = data['delegationFeePercent'].replace('', '0').astype(float).mean()

        if total_amount_burned == 0:
            return None

        # Calculate SDI using the provided formula
        sdi = ((total_amount_staked * total_estimated_reward) / (total_amount_burned)) * (avg_delegation_fee_percent)

        return sdi
    
class StakingEngagementIndex(CustomMetric):
    def __init__(self):
        super().__init__(blockchain='Avalanche', chain='p', name='staking_engagement_index', transaction_type='emitted_utxo', category='Economic Indicators', description='Description')

    def calculate(self, data: pd.DataFrame) ->float:
        # Assuming 'amountStaked' and 'estimatedReward' are columns in the DataFrame
        total_amount_staked = data['amountStaked'].sum()
        total_estimated_reward = data['estimatedReward'].replace('', '0').astype(float).sum()

        if total_amount_staked == 0:
            return None

        # Calculate SEI using the provided formula
        sei = total_estimated_reward / total_amount_staked if total_amount_staked else 0  # Ensure division by zero is handled

        return sei
    
class InterchainTransactionalCoherance(CustomMetric):
    def __init__(self):
        super().__init__(blockchain='Avalanche', chain='c', name='interchain_transactional_coherence', transaction_type='transaction', category='Economic Indicators', description='Description')

    def calculate(self, data: pd.DataFrame) ->float:
        # Assuming 'amountCreated', 'sourceChain', and 'destinationChain' are columns in the DataFrame
        total_cross_chain_value = data.loc[(data['sourceChain'].notna()) & (data['destinationChain'].notna()), 'amountCreated'].sum()
        total_transaction_value = data['amountCreated'].sum()

        if total_transaction_value == 0:
            return None

        # Calculate ITC using the provided formula
        itc = total_cross_chain_value / total_transaction_value if total_transaction_value else None

        return itc
class InterchainLiquidityRatio(CustomMetric):
    def __init__(self):
        super().__init__(blockchain='Avalanche', chain='c', name='interchain_liquidity_ratio', transaction_type='transaction', category='Economic Indicators', description='Description')

    def calculate(self, data: pd.DataFrame) ->float:
        # Assuming 'amountUnlocked', 'amountCreated', 'sourceChain', and 'destinationChain' are columns in the DataFrame
        total_interchain_value = data.loc[(data['sourceChain'].notna()) & (data['destinationChain'].notna()), ['amountUnlocked', 'amountCreated']].replace('', '0').astype(float).sum().sum()
        total_created_value = data['amountCreated'].replace('', '0').astype(float).sum()

        if total_created_value == 0:
            return None

        # Calculate ILR using the provided formula
        ilr = total_interchain_value / total_created_value if total_created_value else 0  # Ensure division by zero is handled
        return ilr
    
class NetworkEconomyEfficiency(CustomMetric):
    def __init__(self):
        super().__init__(blockchain='Avalanche', chain='x', name='network_economy_efficiency', transaction_type='transaction', category='Economic Indicators', description='Description')

    def calculate(self, data: pd.DataFrame) ->float:
        # Assuming 'amountCreated' and 'amountBurned' are columns in the DataFrame
        total_value_transacted = data['amountCreated'].replace('', '0').astype(float).sum()
        total_amount_burned = data['amountBurned'].replace('', '0').astype(float).sum()

        if total_amount_burned == 0:
            return None

        # Calculate NEE using the provided formula
        nee = total_value_transacted / total_amount_burned if total_amount_burned else None

        return nee
    