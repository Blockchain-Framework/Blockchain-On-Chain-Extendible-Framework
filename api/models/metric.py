from flask_sqlalchemy import SQLAlchemy
from database import db

class DailyTransactionCount(db.Model):
    __tablename__ = 'daily_transaction_count'
    date = db.Column(db.String, primary_key=True)
    blockchain_name = db.Column(db.String)
    chain_name = db.Column(db.String)
    count = db.Column(db.Integer)

    def serialize(self):
        return {
            'date': self.date,
            'blockchain_name': self.blockchain_name,
            'chain_name': self.chain_name,
            'value': self.count
        }

class AverageTransactionsPerBlock(db.Model):
    __tablename__ = 'average_transactions_per_block'
    date = db.Column(db.String, primary_key=True)
    blockchain_name = db.Column(db.String)
    chain_name = db.Column(db.String)
    avg_transactions_per_block = db.Column(db.Float)

    def serialize(self):
        return {
            'date': self.date,
            'blockchain_name': self.blockchain_name,
            'chain_name': self.chain_name,
            'value': self.avg_transactions_per_block
        }

class TotalStakedAmount(db.Model):
    __tablename__ = 'total_staked_amount'
    date = db.Column(db.String, primary_key=True)
    blockchain_name = db.Column(db.String)
    chain_name = db.Column(db.String)
    total_staked_amount = db.Column(db.Float)

    def serialize(self):
        return {
            'date': self.date,
            'blockchain_name': self.blockchain_name,
            'chain_name': self.chain_name,
            'value': self.total_staked_amount
        }

class TotalBurnedAmount(db.Model):
    __tablename__ = 'total_burned_amount'
    date = db.Column(db.String, primary_key=True)
    blockchain_name = db.Column(db.String)
    chain_name = db.Column(db.String)
    total_burned_amount = db.Column(db.Float)

    def serialize(self):
        return {
            'date': self.date,
            'blockchain_name': self.blockchain_name,
            'chain_name': self.chain_name,
            'value': self.total_burned_amount
        }

class AverageTransactionValue(db.Model):
    __tablename__ = 'average_transaction_value'
    date = db.Column(db.String, primary_key=True)
    blockchain_name = db.Column(db.String)
    chain_name = db.Column(db.String)
    average_transaction_value = db.Column(db.Float)

    def serialize(self):
        return {
            'date': self.date,
            'blockchain_name': self.blockchain_name,
            'chain_name': self.chain_name,
            'value': self.average_transaction_value
        }

class LargeTransactionMonitoring(db.Model):
    __tablename__ = 'large_transaction_monitoring'
    date = db.Column(db.String, primary_key=True)
    blockchain_name = db.Column(db.String)
    chain_name = db.Column(db.String)
    large_transaction_count = db.Column(db.Integer)

    def serialize(self):
        return {
            'date': self.date,
            'blockchain_name': self.blockchain_name,
            'chain_name': self.chain_name,
            'value': self.large_transaction_count
        }

class CrossChainWhaleActivity(db.Model):
    __tablename__ = 'cross_chain_whale_activity'
    date = db.Column(db.String, primary_key=True)
    blockchain_name = db.Column(db.String)
    chain_name = db.Column(db.String)
    cross_chain_large_transaction_count = db.Column(db.Integer)

    def serialize(self):
        return {
            'date': self.date,
            'blockchain_name': self.blockchain_name,
            'chain_name': self.chain_name,
            'value': self.cross_chain_large_transaction_count
        }

class WhaleAddressActivity(db.Model):
    __tablename__ = 'whale_address_activity'
    date = db.Column(db.String, primary_key=True)
    blockchain_name = db.Column(db.String)
    chain_name = db.Column(db.String)
    whale_address_activity_count = db.Column(db.Integer)

    def serialize(self):
        return {
            'date': self.date,
            'blockchain_name': self.blockchain_name,
            'chain_name': self.chain_name,
            'value': self.whale_address_activity_count
        }
    
class AvgUtxoValue(db.Model):
    __tablename__ = 'avg_utxo_value'
    date = db.Column(db.String, primary_key=True)
    blockchain_name = db.Column(db.String)
    chain_name = db.Column(db.String)
    avg_utxo_value_count = db.Column(db.Integer)

    def serialize(self):
        return {
            'date': self.date,
            'blockchain_name': self.blockchain_name,
            'chain_name': self.chain_name,
            'value': self.avg_utxo_value_count
        }
    
class MedianTransactionValue(db.Model):
    __tablename__ = 'median_trx_value'
    date = db.Column(db.String, primary_key=True)
    blockchain_name = db.Column(db.String)
    chain_name = db.Column(db.String)
    median_trx_value_count = db.Column(db.Integer)

    def serialize(self):
        return {
            'date': self.date,
            'blockchain_name': self.blockchain_name,
            'chain_name': self.chain_name,
            'value': self.median_trx_value_count
        }
    
class CumulativeNumberOfTransactions(db.Model):
    __tablename__ = 'cumulative_number_of_trx'
    date = db.Column(db.String, primary_key=True)
    blockchain_name = db.Column(db.String)
    chain_name = db.Column(db.String)
    cumulative_number_of_trx = db.Column(db.Integer)

    def serialize(self):
        return {
            'date': self.date,
            'blockchain_name': self.blockchain_name,
            'chain_name': self.chain_name,
            'value': self.cumulative_number_of_trx
        }
    
class ActiveAddresses(db.Model):
    __tablename__ = 'active_addresses'
    date = db.Column(db.String, primary_key=True)
    blockchain_name = db.Column(db.String)
    chain_name = db.Column(db.String)
    active_addresses = db.Column(db.Integer)

    def serialize(self):
        return {
            'date': self.date,
            'blockchain_name': self.blockchain_name,
            'chain_name': self.chain_name,
            'value': self.active_addresses
        }
    
class TransactionsPerSecond(db.Model):
    __tablename__ = 'trx_per_second'
    date = db.Column(db.String, primary_key=True)
    blockchain_name = db.Column(db.String)
    chain_name = db.Column(db.String)
    trx_per_second = db.Column(db.Integer)

    def serialize(self):
        return {
            'date': self.date,
            'blockchain_name': self.blockchain_name,
            'chain_name': self.chain_name,
            'value': self.trx_per_second
        }
