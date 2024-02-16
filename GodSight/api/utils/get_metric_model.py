<<<<<<< HEAD
from models.metric import (DailyTransactionCount, AverageTransactionsPerBlock, TotalStakedAmount,
                           TotalBurnedAmount, AverageTransactionValue, LargeTransactionMonitoring,
                           CrossChainWhaleActivity, WhaleAddressActivity, AvgUtxoValue, MedianTransactionValue,
                           CumulativeNumberOfTransactions, ActiveAddresses, TransactionsPerSecond)

metric_route_map = {
    'daily_transaction_count': DailyTransactionCount,
    'average_transactions_per_block': AverageTransactionsPerBlock,
    'total_staked_amount': TotalStakedAmount,
    'total_burned_amount': TotalBurnedAmount,
    'average_transaction_value': AverageTransactionValue,
    'large_transaction_monitoring': LargeTransactionMonitoring,
    'cross_chain_whale_activity': CrossChainWhaleActivity,
    'whale_address_activity': WhaleAddressActivity,
    'avg_utxo_value': AvgUtxoValue,
    'median_trx_value': MedianTransactionValue,
    'cumulative_number_of_trx': CumulativeNumberOfTransactions,
    'active_addresses': ActiveAddresses,
    'trx_per_second': TransactionsPerSecond
=======
from models.metric import (TransactionsPerSecond,
                           TransactionsPerDay,
                            TotalTransactions,
                            AverageTransactionAmount,
                            AverageTransactionsPerHour,
                            TotalBlocks,
                            AverageTransactionsPerBlock,
                            ActiveAddresses,
                            ActiveSenders,
                            CumulativeNumberOfTransactions,
                            SumEmittedUtxoAmount,
                            AvgEmmitedUtxoAmount,
                            MedianEmmitedUtxoValue,
                            SumConsumedUtxoAmount,
                            AvgConsumedUtxoAmount,
                            MedianConsumedUtxoAmount,
                            LargeTransactionMonitoring,
                            WhaleAddressActivity,
                            TotalStakedAmount,
                            TotalBurnedAmount)

metric_route_map = {
    'trx_per_second': TransactionsPerSecond,
    'trx_per_day': TransactionsPerDay,  # Assuming a placeholder class name
    'total_trxs': TotalTransactions,
    'avg_trx_amount': AverageTransactionAmount,
    'avg_trxs_per_hour': AverageTransactionsPerHour,  # Placeholder
    'total_blocks': TotalBlocks,  # Placeholder
    'avg_tx_per_block': AverageTransactionsPerBlock,
    'active_addresses': ActiveAddresses,
    'active_senders': ActiveSenders,  # Placeholder
    'cumulative_number_of_trx': CumulativeNumberOfTransactions,
    'sum_emitted_utxo_amount': SumEmittedUtxoAmount,  # Placeholder
    'avg_emmited_utxo_amount': AvgEmmitedUtxoAmount,  # Assuming similar to avg_utxo_value
    'median_emmited_utxo_amount': MedianEmmitedUtxoValue,  # Placeholder, assuming similarity
    'sum_consumed_utxo_amount': SumConsumedUtxoAmount,  # Placeholder
    'avg_consumed_utxo_amount': AvgConsumedUtxoAmount,  # Placeholder
    'median_consumed_utxo_amount': MedianConsumedUtxoAmount,  # Placeholder
    'large_trx': LargeTransactionMonitoring,
    'whale_address_activity': WhaleAddressActivity,
    'total_staked_amount': TotalStakedAmount,
    'total_burned_amount': TotalBurnedAmount
>>>>>>> feature/dual-workflow
}
