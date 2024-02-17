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

        query = f"SELECT COUNT(*) FROM {subchain}_transactions"
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
    
class AverageTransactionPerBlock(BaseMetric):
    def __init__(self):
        super().__init__(name = 'avg_tx_per_block', category = "'Economic Indicators'", description = 'Description')
          
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



if __name__ == "__main__":
    active_senders = ActiveSenders('Avalanche', 'x', 'active_senders', 'transaction', 'Economic Indicators', 'Description')
    s = active_senders.calculate('Avalanche', 'x', '2022-01-01')
    