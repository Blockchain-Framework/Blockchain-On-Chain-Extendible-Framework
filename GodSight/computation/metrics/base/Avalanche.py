import sys
from pathlib import Path
import pandas as pd

from utils.model.metric import BaseMetric
from utils.database.database_service import execute_query

class TransactionPerSecond(BaseMetric):
    def __init__(self):
        super().__init__(name = 'trx_per_second', category = "'Economic Indicators'", description = 'Description')
    
    def calculate(self, blockchain: str, subchain: str, date: str) -> float:
        if not subchain or not date:
            raise

        query = f"SELECT COUNT(*) FROM {subchain}_transactions WHERE date = '{date}'"
        results = execute_query(query)
        
        if results is not None and not results.empty:
            count = results.iloc[0]['count']
            if count > 0:
                return count / 86400
            else:
                return 0
        return None         


class TransactionPerDay(BaseMetric):
    def __init__(self):
        super().__init__(name = 'trx_per_day', category = "'Economic Indicators'", description = 'Description')
    
    def calculate(self, blockchain: str, subchain: str, date: str) -> float:
        if not subchain or not date:
            raise

        query = f"SELECT COUNT(*) FROM {subchain}_transactions WHERE date = '{date}'"
        results = execute_query(query)
        
        if results is not None and not results.empty:
            return results.iloc[0]['count']
        return None


class TotalTransactions(BaseMetric):
    def __init__(self):
        super().__init__(name = 'total_transactions', category = "'Economic Indicators'", description = 'Description')
    def calculate(self, blockchain: str, subchain: str, date: str) -> float:
        if not subchain:
            return None

        query = f"""
        SELECT SUM(CAST(amount AS NUMERIC)) as count
        FROM {subchain}_consumed_utxos
        WHERE date = '{date}'
        """
        results = execute_query(query)
        
        if results is not None and not results.empty:
            return results.iloc[0]['count']
        return None
    
class AvarageTransactionAmount(BaseMetric):
    def __init__(self):
        super().__init__(name = 'avarage_transaction_amount', category = "'Economic Indicators'", description = 'Description')
    
    def calculate(self, blockchain: str, subchain: str, date: str) -> float:
        if not subchain or not date:
            return None

        # Query for the sum of transaction amounts and count of transactions
        query = f"""
        SELECT SUM(CAST(amount AS NUMERIC)) as total_amount, COUNT(*) as trx_count
        FROM {subchain}_consumed_utxos
        WHERE date = '{date}'
        """
        results = execute_query(query)

        if results is not None and not results.empty:
            total_amount = results.iloc[0]['total_amount']
            trx_count = results.iloc[0]['trx_count']

            if trx_count > 0:
                avg_amount = total_amount / trx_count
                # add_data_to_database('avg_trx_amount', date, blockchain, subchain, avg_amount)
                return avg_amount
            else:
                return 0
        # add_data_to_database('avg_trx_amount', date, blockchain, subchain, None)
        return None
    
    
class AverageTransactionPerHour(BaseMetric):
    def __init__(self):
        super().__init__(name = 'avg_trxs_per_hour', category = "'Economic Indicators'", description = 'Description')
         
    def calculate(self, blockchain: str, subchain: str, date: str) -> float:
        if not subchain or not date:
            return None

        # Query for the count of transactions
        query = f"""
        SELECT COUNT(*) as trx_count
        FROM {subchain}_transactions
        WHERE date = '{date}'
        """
        results = execute_query(query)

        if results is not None and not results.empty:
            trx_count = results.iloc[0]['trx_count']
            if trx_count > 0:
                return trx_count / 24
            else:
                return 0
        return None
    
class TotalBlocks(BaseMetric):
    def __init__(self):
        super().__init__(name = 'total_blocks', category = "'Economic Indicators'", description = 'Description')
          
    def calculate(self, blockchain: str, subchain: str, date: str) -> float:
        if not subchain:
            return None

        query =  f"SELECT COUNT(DISTINCT \"blockHash\") FROM {subchain}_transactions"
        results = execute_query(query)
        
        if results is not None and not results.empty:
            return results.iloc[0]['count']
        return None    
    
class TransactionPerBlock(BaseMetric):
    def __init__(self):
        super().__init__(name = 'trx_per_block', category = "'Economic Indicators'", description = 'Description')
          
    def calculate(self, blockchain: str, subchain: str, date: str) -> float:
        if not subchain or not date:
            return None

        # Query for the count of transactions
        query = f"""
        SELECT AVG(tx_count) as avg_tx_per_block
        FROM (
            SELECT \"blockHash\", COUNT(*) as tx_count
            FROM {subchain}_transactions
            WHERE date = '{date}'
            GROUP BY \"blockHash\"
        ) as block_transactions
        """
        results = execute_query(query)

        if results is not None and not results.empty:
            trx_count = results.iloc[0]['avg_tx_per_block']
        else:
            return None
        
class ActiveAddresses(BaseMetric):
    def __init__(self):
        super().__init__(name = 'active_addresses', category = "'Economic Indicators'", description = 'Description')
            
    def calculate(self, blockchain: str, subchain: str, date: str) -> float:
        if not subchain or not date:
            return None

        query = f"""
        SELECT COUNT(DISTINCT addresses) FROM (
            SELECT addresses FROM {subchain}_emitted_utxos WHERE date = '{date}'
            UNION
            SELECT addresses FROM {subchain}_consumed_utxos WHERE date = '{date}'
        ) AS active_addresses
        """
        results = execute_query(query)
        
        if results is not None and not results.empty:
            active_addrs_count = results.iloc[0]['count']
            return active_addrs_count
        else:
            return 0

        
class ActiveSenders(BaseMetric):
    def __init__(self):
        super().__init__(name = 'active_senders', category = "'Economic Indicators'", description = 'Description')
            
    def calculate(self, blockchain: str, subchain: str, date: str) -> float:
        if not subchain or not date:
            return None

        query = f"""
        SELECT COUNT(DISTINCT addresses) FROM {subchain}_emitted_utxos WHERE date = '{date}'
        """ 
        results = execute_query(query)
        
        if results is not None and not results.empty:
            active_senders_count = results.iloc[0]['count']
            return active_senders_count
        
        else:
            return 0

# class CummulativeNumberOfTransactions(BaseMetric):
#     def __init__(self):
#         super().__init__(name = 'cumulative_number_of_trx', category = "'Economic Indicators'", description = 'Description')
            
#     def calculate(self, blockchain: str, subchain: str, date: str) -> float:
#         if not subchain or not date:
#             return None

#         query = f"SELECT COUNT(*) FROM {subchain}_transactions WHERE date <= '{date}'"
#         results = execute_query(query)
        
#         if results is not None and not results.empty:
#             cumulative_trx_count = results.iloc[0]['count']
#             return cumulative_trx_count
#         else:
#             return 0

class SumEmittedUtxoAmount(BaseMetric):
    def __init__(self):
        super().__init__(name = 'active_senders', category = "'Economic Indicators'", description = 'Description')
            
    def calculate(self, blockchain: str, subchain: str, date: str) -> float:
        if not subchain or not date:
            return None

        query = f"SELECT SUM(CAST(amount AS NUMERIC)) FROM {subchain}_emitted_utxos WHERE date = '{date}'"
        results = execute_query(query)
        
        if results is not None and not results.empty:
            emitted_utxo_sum = results.iloc[0]['sum']
            return emitted_utxo_sum
        else:
            return None
        
class AverageEmittedUtxoAmount(BaseMetric):
    def __init__(self):
        super().__init__(name = 'avg_emmited_utxo_amount', category = "'Economic Indicators'", description = 'Description')
            
    def calculate(self, blockchain: str, subchain: str, date: str) -> float:
        if not subchain or not date:
            return None

        query = f"SELECT AVG(CAST(amount AS NUMERIC)) FROM {subchain}_emitted_utxos WHERE date = '{date}'"
        results = execute_query(query)
        
        if results is not None and not results.empty:
            avg_utxo_amount = results.iloc[0]['avg']
            return avg_utxo_amount
        else:
            return None
class MedianEmittedUtxoAmount(BaseMetric):
    def __init__(self):
        super().__init__(name = 'active_senders', category = "'Economic Indicators'", description = 'Description')
            
    def calculate(self, blockchain: str, subchain: str, date: str) -> float:
        if not subchain or not date:
            return None

        query = f"""
        SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY CAST(amount AS NUMERIC)) 
        FROM {subchain}_emitted_utxos 
        WHERE date = '{date}'
        """
        results = execute_query(query)
        
        if results is not None and not results.empty:
            median_utxo_amount = results.iloc[0]['percentile_cont']
            return median_utxo_amount
        else:
            return None
class SumConsumedUtxoAmount(BaseMetric):
    def __init__(self):
        super().__init__(name = 'sum_consumed_utxo_amount', category = "'Economic Indicators'", description = 'Description')
            
    def calculate(self, blockchain: str, subchain: str, date: str) -> float:
        if not subchain or not date:
            return None

        # Assuming 'consumed_table' refers to a table where UTXOs are consumed in the subchain transactions
        query = f"SELECT SUM(CAST(amount AS NUMERIC)) FROM {subchain}_consumed_utxos WHERE date = '{date}'"
        results = execute_query(query)
        
        if results is not None and not results.empty:
            consumed_utxo_sum = results.iloc[0]['sum']
            return consumed_utxo_sum
        else:
            return None
class AverageConsumedUtxoAmount(BaseMetric):
    def __init__(self):
        super().__init__(name = 'avg_consumed_utxo_amount', category = "'Economic Indicators'", description = 'Description')
            
    def calculate(self, blockchain: str, subchain: str, date: str) -> float:
        if not subchain or not date:
            return None

        # Assuming 'table' refers to a table that tracks consumed UTXOs in the subchain transactions
        query = f"SELECT AVG(CAST(amount AS NUMERIC)) FROM {subchain}_consumed_utxos WHERE date = '{date}'"
        results = execute_query(query)
        
        if results is not None and not results.empty:
            avg_consumed_utxo = results.iloc[0]['avg']
            return avg_consumed_utxo
        else:
            return None

class MedianConsumedUtxoAmount(BaseMetric):
    def __init__(self):
        super().__init__(name = 'median_consumed_utxo_amount', category = "'Economic Indicators'", description = 'Description')
            
    def calculate(self, blockchain: str, subchain: str, date: str) -> float:
        if not subchain or not date:
            return None

        # Assuming 'table' refers to a table that tracks consumed UTXOs in the subchain transactions
        query = f"""
        SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY CAST(amount AS NUMERIC)) 
        FROM {subchain}_consumed_utxos 
        WHERE date = '{date}'
        """
        results = execute_query(query)
        
        if results is not None and not results.empty:
            median_consumed_utxo = results.iloc[0]['percentile_cont']
            return median_consumed_utxo
        else:
            return None
class LargeTransactions(BaseMetric):
    def __init__(self):
        super().__init__(name = 'large_trx', category = "'Economic Indicators'", description = 'Description')
            
    def calculate(self, blockchain: str, subchain: str, date: str) -> float:
        threshold = 1000000  # Threshold for a large transaction

        if not subchain or not date or threshold is None:
            return None

        # Assuming that emitted_table and consumed_table are both part of the same subchain transactions
        query = f"""
        WITH emitted AS (
            SELECT \"txHash\", SUM(CAST(amount AS NUMERIC)) as total_emitted
            FROM {subchain}_emitted_utxos
            WHERE date = '{date}'
            GROUP BY \"txHash\"
            HAVING SUM(CAST(amount AS NUMERIC)) > {threshold}
        ),
        consumed AS (
            SELECT \"txHash\", SUM(CAST(amount AS NUMERIC)) as total_consumed
            FROM {subchain}_consumed_utxos
            WHERE date = '{date}'
            GROUP BY \"txHash\"
            HAVING SUM(CAST(amount AS NUMERIC)) > {threshold}
        )
        SELECT COUNT(DISTINCT \"txHash\") as large_transactions_count
        FROM (
            SELECT \"txHash\" FROM emitted
            UNION
            SELECT \"txHash\" FROM consumed
        ) as combined
        """
        results = execute_query(query)
        
        if results is not None and not results.empty:
            large_trx_count = results.iloc[0]['large_transactions_count']
            return large_trx_count
        else:
            return None
class WhaleAddreessActivity(BaseMetric):
    def __init__(self):
        super().__init__(name = 'whale_address_activity', category = "'Economic Indicators'", description = 'Description')
            
    def calculate(self, blockchain: str, subchain: str, date: str) -> float:
        threshold = 8000000000000  # Threshold for whale transactions
    
        if not subchain or not date or threshold is None:
            return None

        # Assuming that emitted_table and consumed_table are both part of the same subchain transactions
        query = f"""
        WITH whale_emitted AS (
            SELECT \"txHash\"
            FROM {subchain}_emitted_utxos
            WHERE date = '{date}'
            GROUP BY \"txHash\"
            HAVING SUM(CAST(amount AS NUMERIC)) > {threshold}
        ),
        whale_consumed AS (
            SELECT \"txHash\"
            FROM {subchain}_consumed_utxos
            WHERE date = '{date}'
            GROUP BY \"txHash\"
            HAVING SUM(CAST(amount AS NUMERIC)) > {threshold}
        )
        SELECT COUNT(DISTINCT \"txHash\") as whale_transactions_count
        FROM (
            SELECT \"txHash\" FROM whale_emitted
            UNION
            SELECT \"txHash\" FROM whale_consumed
        ) as combined_whale_transactions
        """
        results = execute_query(query)
        
        if results is not None and not results.empty:
            whale_trx_count = results.iloc[0]['whale_transactions_count']
            return whale_trx_count
        else:
            return None

if __name__ == "__main__":
    active_senders = ActiveSenders('Avalanche', 'x', 'active_senders', 'transaction', 'Economic Indicators', 'Description')
    s = active_senders.calculate('Avalanche', 'x', '2022-01-01')
    
