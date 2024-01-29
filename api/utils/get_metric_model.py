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
}
