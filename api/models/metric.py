from flask_sqlalchemy import SQLAlchemy
from database import db

class MetricBase(db.Model):
    __abstract__ = True  # This makes MetricBase an abstract class
    date = db.Column(db.DateTime, primary_key=True)
    blockchain = db.Column(db.String, primary_key=True)
    subchain = db.Column(db.String, primary_key=True)
<<<<<<< HEAD
    value = db.Column(db.Float)  # Use Float if it's the most common type or adjust as needed
=======
    value = db.Column(db.Float) 
>>>>>>> feature/dual-workflow

    def serialize(self):
        return {
            'date': self.date,
            'blockchain': self.blockchain,
            'subchain': self.subchain,
            'value': self.value
        }

<<<<<<< HEAD
class DailyTransactionCount(MetricBase):
    __tablename__ = 'daily_transaction_count'

class AverageTransactionsPerBlock(MetricBase):
    __tablename__ = 'average_transactions_per_block'

class TotalStakedAmount(MetricBase):
    __tablename__ = 'total_staked_amount'

class TotalBurnedAmount(MetricBase):
    __tablename__ = 'total_burned_amount'

class AverageTransactionValue(MetricBase):
    __tablename__ = 'average_transaction_value'

class LargeTransactionMonitoring(MetricBase):
    __tablename__ = 'large_transaction_monitoring'
    

class CrossChainWhaleActivity(MetricBase):
    __tablename__ = 'cross_chain_whale_activity'
    
class WhaleAddressActivity(MetricBase):
    __tablename__ = 'whale_address_activity'
    
class AvgUtxoValue(MetricBase):
    __tablename__ = 'avg_utxo_value'
    
class MedianTransactionValue(MetricBase):
    __tablename__ = 'median_trx_value'
    
class CumulativeNumberOfTransactions(MetricBase):
    __tablename__ = 'cumulative_number_of_trx'
    
class ActiveAddresses(MetricBase):
    __tablename__ = 'active_addresses' 
    
class TransactionsPerSecond(MetricBase):
    __tablename__ = 'trx_per_second'
=======
class TransactionsPerDay(MetricBase):  
    __tablename__ = 'trx_per_day'

class TransactionsPerSecond(MetricBase):
    __tablename__ = 'trx_per_second'

class TotalTransactions(MetricBase): 
    __tablename__ = 'total_trxs'
    
class AverageTransactionAmount(MetricBase):  
    __tablename__ = 'avg_trx_amount'
    
class CumulativeNumberOfTransactions(MetricBase):  
    __tablename__ = 'cumulative_number_of_trx'

class AverageTransactionsPerHour(MetricBase):
    __tablename__ = 'avg_trxs_per_hour'
    
class TotalBlocks(MetricBase):
    __tablename__ = 'total_blocks'
    
class AverageTransactionsPerBlock(MetricBase):  
    __tablename__ = 'avg_tx_per_block'
    
class ActiveAddresses(MetricBase):  
    __tablename__ = 'active_addresses'
    
class ActiveSenders(MetricBase):
    __tablename__ = 'active_senders'
    
class SumEmittedUtxoAmount(MetricBase):
    __tablename__ = 'sum_emitted_utxo_amount'

class AvgEmmitedUtxoAmount(MetricBase):  
    __tablename__ = 'avg_emmited_utxo_amount'

class MedianEmmitedUtxoValue(MetricBase): 
    __tablename__ = 'median_emmited_utxo_amount'

class SumConsumedUtxoAmount(MetricBase):
    __tablename__ = 'sum_consumed_utxo_amount'

class AvgConsumedUtxoAmount(MetricBase):
    __tablename__ = 'avg_consumed_utxo_amount'

class MedianConsumedUtxoAmount(MetricBase):
    __tablename__ = 'median_consumed_utxo_amount'

class LargeTransactionMonitoring(MetricBase):  
    __tablename__ = 'large_trx'
    
class WhaleAddressActivity(MetricBase):  
    __tablename__ = 'whale_address_activity'

class TotalStakedAmount(MetricBase):  
    __tablename__ = 'total_staked_amount'
    
class TotalBurnedAmount(MetricBase): 
    __tablename__ = 'total_burned_amount'
>>>>>>> feature/dual-workflow
