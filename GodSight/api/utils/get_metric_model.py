
from ..models.metric import Metric

from ..models.metric import (
                           TransactionsPerDay,
                            TotalTransactions,
                            AverageTransactionAmount,
                            TransactionsPerDay,
                            TotalBlocks,
                            AvgTrxsPerHour,
                            ActiveAddresses,
                            ActiveSenders,
                            TrxPerBlock,
                            SumEmittedUtxoAmount,
                            AvgEmittedUtxoAmount,
                            MedianEmittedUtxoAmount,
                            SumConsumedUtxoAmount,
                            AvgConsumedUtxoAmount,
                            MedianConsumedUtxoAmount,
                            LargeTrx,
                            WhaleAddressActivity
                            )

metric_route_map = {
    'trx_per_day': TransactionsPerDay,
    'total_transactions': TotalTransactions,
    'average_transaction_amount': AverageTransactionAmount,
    'avg_trxs_per_hour': AvgTrxsPerHour,
    'total_blocks': TotalBlocks,
    'trx_per_block': TrxPerBlock,
    'active_addresses': ActiveAddresses,
    'active_senders': ActiveSenders,
    'sum_emitted_utxo_amount': SumEmittedUtxoAmount,
    'avg_emitted_utxo_amount': AvgEmittedUtxoAmount,
    'median_emitted_utxo_amount': MedianEmittedUtxoAmount,
    'sum_consumed_utxo_amount': SumConsumedUtxoAmount,
    'avg_consumed_utxo_amount': AvgConsumedUtxoAmount,
    'median_consumed_utxo_amount': MedianConsumedUtxoAmount,
    'large_trx': LargeTrx,
    'whale_address_activity': WhaleAddressActivity,
}

