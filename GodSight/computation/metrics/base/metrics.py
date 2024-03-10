import sys
from pathlib import Path
import pandas as pd

from GodSight.computation.utils.model.metric import BaseMetric
from GodSight.computation.utils.database.database_service import execute_query
from GodSight.computation.config.config import Config

class TransactionPerSecond(BaseMetric):
    def __init__(self):
        super().__init__(name = 'trx_per_second', category = "'Economic Indicators'", description = 'Description')
    
    def calculate(self, blockchain: str, subchain: str, date: str, config : Config) -> float:
        if not subchain or not date:
            raise

        query = f"SELECT COUNT(*) FROM transaction_data WHERE date = '{date}' AND blockchain = '{blockchain}' AND sub_chain = '{subchain}'"
        results = execute_query(query, config)
        if results is not None and not results.empty:
            count = results.iloc[0]['count']
            if count > 0:
                return count / 86400
            else:
                return 0
        return 0


class TransactionPerDay(BaseMetric):
    def __init__(self):
        super().__init__(name = 'trx_per_day', category = "'Economic Indicators'", description = 'Description')

    def calculate(self, blockchain: str, subchain: str, date: str, config : Config) -> float:
        if not subchain or not date:
            raise

        query = f"SELECT COUNT(*) FROM transaction_data WHERE date = '{date}' AND blockchain = '{blockchain}' AND sub_chain = '{subchain}'"
        results = execute_query(query, config)
        
        if results is not None and not results.empty:
            return results.iloc[0]['count']
        return 0


class TotalTransactions(BaseMetric):
    def __init__(self):
        super().__init__(name = 'total_transactions', category = "'Economic Indicators'", description = 'Description')
    def calculate(self, blockchain: str, subchain: str, date: str, config : Config) -> float:
        if not subchain:
            return 0

        query = f"""
        SELECT SUM(CAST(amount AS NUMERIC)) as count
        FROM consumed_utxo_data
        WHERE date = '{date}' AND blockchain = '{blockchain}' AND sub_chain = '{subchain}'
        """
        results = execute_query(query, config)
        
        if results is not None and not results.empty:
            return results.iloc[0]['count']
        return 0
    
class AvarageTransactionAmount(BaseMetric):
    def __init__(self):
        super().__init__(name = 'average_transaction_amount', category = "'Economic Indicators'", description = 'Description')
    
    def calculate(self, blockchain: str, subchain: str, date: str, config : Config) -> float:
        if not subchain or not date:
            return 0

        # Query for the sum of transaction amounts and count of transactions
        query = f"""
        SELECT SUM(CAST(amount AS NUMERIC)) as total_amount, COUNT(*) as trx_count
        FROM consumed_utxo_data
        WHERE date = '{date}' AND blockchain = '{blockchain}' AND sub_chain = '{subchain}'
        """
        results = execute_query(query, config)

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
        return 0
    
    
class AverageTransactionPerHour(BaseMetric):
    def __init__(self):
        super().__init__(name = 'avg_trxs_per_hour', category = "'Economic Indicators'", description = 'Description')
         
    def calculate(self, blockchain: str, subchain: str, date: str, config : Config) -> float:
        if not subchain or not date:
            return 0

        # Query for the count of transactions
        query = f"""
        SELECT COUNT(*) as trx_count
        FROM transaction_data
        WHERE date = '{date}' AND blockchain = '{blockchain}' AND sub_chain = '{subchain}'
        """
        results = execute_query(query, config)

        if results is not None and not results.empty:
            trx_count = results.iloc[0]['trx_count']
            if trx_count > 0:
                return trx_count / 24
            else:
                return 0
        return 0
    
class TotalBlocks(BaseMetric):
    def __init__(self):
        super().__init__(name = 'total_blocks', category = "'Economic Indicators'", description = 'Description')
          
    def calculate(self, blockchain: str, subchain: str, date: str, config : Config) -> float:
        if not subchain:
            return 0

        query =  f"SELECT COUNT(DISTINCT \"block_hash\") FROM transaction_data WHERE date = '{date}' AND blockchain = '{blockchain}' AND sub_chain = '{subchain}'"
        results = execute_query(query, config)
        
        if results is not None and not results.empty:
            return results.iloc[0]['count']
        return 0
    
class TransactionPerBlock(BaseMetric):
    def __init__(self):
        super().__init__(name = 'trx_per_block', category = "'Economic Indicators'", description = 'Description')
          
    def calculate(self, blockchain: str, subchain: str, date: str, config : Config) -> float:
        if not subchain or not date:
            return 0

        # Query for the count of transactions
        query = f"""
        SELECT AVG(tx_count) as avg_tx_per_block
        FROM (
            SELECT \"block_hash\", COUNT(*) as tx_count
            FROM transaction_data
            WHERE date = '{date}' AND blockchain = '{blockchain}' AND sub_chain = '{subchain}'
            GROUP BY \"block_hash\"
        ) as block_transactions
        """
        results = execute_query(query, config)

        if results is not None and not results.empty:
            trx_count = results.iloc[0]['avg_tx_per_block']
            return trx_count
        else:
            return 0
        
class ActiveAddresses(BaseMetric):
    def __init__(self):
        super().__init__(name = 'active_addresses', category = "'Economic Indicators'", description = 'Description')
            
    def calculate(self, blockchain: str, subchain: str, date: str, config : Config) -> float:
        if not subchain or not date:
            return 0

        query = f"""
        SELECT COUNT(DISTINCT addresses) FROM (
            SELECT addresses FROM emitted_utxo_data WHERE date = '{date}' AND blockchain = '{blockchain}' AND sub_chain = '{subchain}'
            UNION
            SELECT addresses FROM consumed_utxo_data WHERE date = '{date}' AND blockchain = '{blockchain}' AND sub_chain = '{subchain}'
        ) AS active_addresses
        """
        results = execute_query(query, config)
        
        if results is not None and not results.empty:
            active_addrs_count = results.iloc[0]['count']
            return active_addrs_count
        else:
            return 0

        
class ActiveSenders(BaseMetric):
    def __init__(self):
        super().__init__(name = 'active_senders', category = "'Economic Indicators'", description = 'Description')
            
    def calculate(self, blockchain: str, subchain: str, date: str, config : Config) -> float:
        if not subchain or not date:
            return 0

        query = f"""
        SELECT COUNT(DISTINCT addresses) FROM emitted_utxo_data WHERE date = '{date}' AND blockchain = '{blockchain}' AND sub_chain = '{subchain}'
        """ 
        results = execute_query(query, config)
        
        if results is not None and not results.empty:
            active_senders_count = results.iloc[0]['count']
            return active_senders_count
        
        else:
            return 0

# class CummulativeNumberOfTransactions(BaseMetric):
#     def __init__(self):
#         super().__init__(name = 'cumulative_number_of_trx', category = "'Economic Indicators'", description = 'Description')
            
#     def calculate(self, blockchain: str, subchain: str, date: str, config : Config) -> float:
#         if not subchain or not date:
#             return 0

#         query = f"SELECT COUNT(*) FROM {subchain}_transactions WHERE date <= '{date}'"
#         results = execute_query(query, config)
        
#         if results is not None and not results.empty:
#             cumulative_trx_count = results.iloc[0]['count']
#             return cumulative_trx_count
#         else:
#             return 0

class SumEmittedUtxoAmount(BaseMetric):
    def __init__(self):
        super().__init__(name = 'sum_emitted_utxo_amount', category = "'Economic Indicators'", description = 'Description')
            
    def calculate(self, blockchain: str, subchain: str, date: str, config : Config) -> float:
        if not subchain or not date:
            return 0

        query = f"SELECT SUM(CAST(amount AS NUMERIC)) FROM emitted_utxo_data WHERE date = '{date}' AND blockchain = '{blockchain}' AND sub_chain = '{subchain}'"
        results = execute_query(query, config)
        
        if results is not None and not results.empty:
            emitted_utxo_sum = results.iloc[0]['sum']
            return emitted_utxo_sum
        else:
            return 0
        
class AverageEmittedUtxoAmount(BaseMetric):
    def __init__(self):
        super().__init__(name = 'avg_emitted_utxo_amount', category = "'Economic Indicators'", description = 'Description')
            
    def calculate(self, blockchain: str, subchain: str, date: str, config : Config) -> float:
        if not subchain or not date:
            return 0

        query = f"SELECT AVG(CAST(amount AS NUMERIC)) FROM emitted_utxo_data WHERE date = '{date}' AND blockchain = '{blockchain}' AND sub_chain = '{subchain}'"
        results = execute_query(query, config)
        
        if results is not None and not results.empty:
            avg_utxo_amount = results.iloc[0]['avg']
            return avg_utxo_amount
        else:
            return 0
class MedianEmittedUtxoAmount(BaseMetric):
    def __init__(self):
        super().__init__(name = 'median_emitted_utxo_amount', category = "'Economic Indicators'", description = 'Description')
            
    def calculate(self, blockchain: str, subchain: str, date: str, config : Config) -> float:
        if not subchain or not date:
            return 0

        query = f"""
        SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY CAST(amount AS NUMERIC)) 
        FROM emitted_utxo_data 
        WHERE date = '{date}' AND blockchain = '{blockchain}' AND sub_chain = '{subchain}'
        """
        results = execute_query(query, config)
        
        if results is not None and not results.empty:
            median_utxo_amount = results.iloc[0]['percentile_cont']
            return median_utxo_amount
        else:
            return 0
class SumConsumedUtxoAmount(BaseMetric):
    def __init__(self):
        super().__init__(name = 'sum_consumed_utxo_amount', category = "'Economic Indicators'", description = 'Description')
            
    def calculate(self, blockchain: str, subchain: str, date: str, config : Config) -> float:
        if not subchain or not date:
            return 0

        # Assuming 'consumed_table' refers to a table where UTXOs are consumed in the subchain transactions
        query = f"SELECT SUM(CAST(amount AS NUMERIC)) FROM consumed_utxo_data WHERE date = '{date}' AND blockchain = '{blockchain}' AND sub_chain = '{subchain}'"
        results = execute_query(query, config)
        
        if results is not None and not results.empty:
            consumed_utxo_sum = results.iloc[0]['sum']
            return consumed_utxo_sum
        else:
            return 0
class AverageConsumedUtxoAmount(BaseMetric):
    def __init__(self):
        super().__init__(name = 'avg_consumed_utxo_amount', category = "'Economic Indicators'", description = 'Description')
            
    def calculate(self, blockchain: str, subchain: str, date: str, config : Config) -> float:
        if not subchain or not date:
            return 0

        # Assuming 'table' refers to a table that tracks consumed UTXOs in the subchain transactions
        query = f"SELECT AVG(CAST(amount AS NUMERIC)) FROM consumed_utxo_data WHERE date = '{date}' AND blockchain = '{blockchain}' AND sub_chain = '{subchain}'"
        results = execute_query(query, config)
        
        if results is not None and not results.empty:
            avg_consumed_utxo = results.iloc[0]['avg']
            return avg_consumed_utxo
        else:
            return 0

class MedianConsumedUtxoAmount(BaseMetric):
    def __init__(self):
        super().__init__(name = 'median_consumed_utxo_amount', category = "'Economic Indicators'", description = 'Description')
            
    def calculate(self, blockchain: str, subchain: str, date: str, config : Config) -> float:
        if not subchain or not date:
            return 0

        # Assuming 'table' refers to a table that tracks consumed UTXOs in the subchain transactions
        query = f"""
        SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY CAST(amount AS NUMERIC)) 
        FROM consumed_utxo_data
        WHERE date = '{date}' AND blockchain = '{blockchain}' AND sub_chain = '{subchain}'
        """
        results = execute_query(query, config)
        
        if results is not None and not results.empty:
            median_consumed_utxo = results.iloc[0]['percentile_cont']
            return median_consumed_utxo
        else:
            return 0
class LargeTransactions(BaseMetric):
    def __init__(self):
        super().__init__(name = 'large_trx', category = "'Economic Indicators'", description = 'Description')
            
    def calculate(self, blockchain: str, subchain: str, date: str, config : Config) -> float:
        threshold = 1000000  # Threshold for a large transaction

        if not subchain or not date or threshold is None:
            return 0

        # Assuming that emitted_table and consumed_table are both part of the same subchain transactions
        query = f"""
        WITH emitted AS (
            SELECT \"tx_hash\", SUM(CAST(amount AS NUMERIC)) as total_emitted
            FROM emitted_utxo_data
            WHERE date = '{date}' AND blockchain = '{blockchain}' AND sub_chain = '{subchain}'
            GROUP BY \"tx_hash\"
            HAVING SUM(CAST(amount AS NUMERIC)) > {threshold}
        ),
        consumed AS (
            SELECT \"tx_hash\", SUM(CAST(amount AS NUMERIC)) as total_consumed
            FROM consumed_utxo_data
            WHERE date = '{date}' AND blockchain = '{blockchain}' AND sub_chain = '{subchain}'
            GROUP BY \"tx_hash\"
            HAVING SUM(CAST(amount AS NUMERIC)) > {threshold}
        )
        SELECT COUNT(DISTINCT \"tx_hash\") as large_transactions_count
        FROM (
            SELECT \"tx_hash\" FROM emitted
            UNION
            SELECT \"tx_hash\" FROM consumed
        ) as combined
        """
        results = execute_query(query, config)
        
        if results is not None and not results.empty:
            large_trx_count = results.iloc[0]['large_transactions_count']
            return large_trx_count
        else:
            return 0
class WhaleAddreessActivity(BaseMetric):
    def __init__(self):
        super().__init__(name = 'whale_address_activity', category = "'Economic Indicators'", description = 'Description')
            
    def calculate(self, blockchain: str, subchain: str, date: str, config : Config) -> float:
        threshold = 8000000000000  # Threshold for whale transactions
    
        if not subchain or not date or threshold is None:
            return 0

        # Assuming that emitted_table and consumed_table are both part of the same subchain transactions
        query = f"""
        WITH whale_emitted AS (
            SELECT \"tx_hash\"
            FROM emitted_utxo_data
            WHERE date = '{date}' AND blockchain = '{blockchain}' AND sub_chain = '{subchain}'
            GROUP BY \"tx_hash\"
            HAVING SUM(CAST(amount AS NUMERIC)) > {threshold}
        ),
        whale_consumed AS (
            SELECT \"tx_hash\"
            FROM consumed_utxo_data
            WHERE date = '{date}' AND blockchain = '{blockchain}' AND sub_chain = '{subchain}'
            GROUP BY \"tx_hash\"
            HAVING SUM(CAST(amount AS NUMERIC)) > {threshold}
        )
        SELECT COUNT(DISTINCT \"tx_hash\") as whale_transactions_count
        FROM (
            SELECT \"tx_hash\" FROM whale_emitted
            UNION
            SELECT \"tx_hash\" FROM whale_consumed
        ) as combined_whale_transactions
        """
        results = execute_query(query, config)
        
        if results is not None and not results.empty:
            whale_trx_count = results.iloc[0]['whale_transactions_count']
            return whale_trx_count
        else:
            return 0

    
