from flask_sqlalchemy import SQLAlchemy
from database import db

class DailyTransactionCount(db.Model):
    __tablename__ = 'daily_transaction_count'
    date = db.Column(db.DateTime, primary_key=True)
    chain_name = db.Column(db.String)
    value = db.Column(db.Integer)
    
    def serialize(self):
        return {
            'date': self.date,
            'chain_name': self.chain_name,
            'value': self.value
        }

class AverageTransactionsPerBlock(db.Model):
    __tablename__ = 'average_transactions_per_block'
    date = db.Column(db.DateTime, primary_key=True)
    chain_name = db.Column(db.String)
    value = db.Column(db.Float)

    def serialize(self):
        return {
            'date': self.date,
            'chain_name': self.chain_name,
            'value': self.value
        }

class TotalStakedAmount(db.Model):
    __tablename__ = 'total_staked_amount'
    date = db.Column(db.DateTime, primary_key=True)
    chain_name = db.Column(db.String)
    value = db.Column(db.Float)

    def serialize(self):
        return {
            'date': self.date,
            'chain_name': self.chain_name,
            'value': self.value
        }

class TotalBurnedAmount(db.Model):
    __tablename__ = 'total_burned_amount'
    date = db.Column(db.DateTime, primary_key=True)
    chain_name = db.Column(db.String)
    value = db.Column(db.Float)

    def serialize(self):
        return {
            'date': self.date,
            'chain_name': self.chain_name,
            'value': self.value
        }

class AverageTransactionValue(db.Model):
    __tablename__ = 'average_transaction_value'
    date = db.Column(db.DateTime, primary_key=True)
    chain_name = db.Column(db.String)
    value = db.Column(db.Float)

    def serialize(self):
        return {
            'date': self.date,
            'chain_name': self.chain_name,
            'value': self.value
        }

class LargeTransactionMonitoring(db.Model):
    __tablename__ = 'large_transaction_monitoring'
    date = db.Column(db.DateTime,primary_key=True)
    chain_name = db.Column(db.String)
    value = db.Column(db.Integer)

    def serialize(self):
        return {
            'date': self.date,
            'chain_name': self.chain_name,
            'value': self.value
        }

class CrossChainWhaleActivity(db.Model):
    __tablename__ = 'cross_chain_whale_activity'
    date = db.Column(db.DateTime, primary_key=True)
    chain_name = db.Column(db.String)
    value = db.Column(db.Integer)

    def serialize(self):
        return {
            'date': self.date,
            'blockchain': self.chain_name,
            'sub_chain':self.sub_chain_name,
            'value': self.value
        }

class WhaleAddressActivity(db.Model):
    __tablename__ = 'whale_address_activity'
    date = db.Column(db.DateTime, primary_key=True)
    chain_name = db.Column(db.String)
    value = db.Column(db.Integer)

    def serialize(self):
        return {
            'date': self.date,
            'chain_name': self.chain_name,
            'value': self.value
        }
    
class AvgUtxoValue(db.Model):
    __tablename__ = 'avg_utxo_value'
    date = db.Column(db.DateTime,primary_key=True)
    chain_name = db.Column(db.String)
    value = db.Column(db.Integer)

    def serialize(self):
        return {
            'date': self.date,
            'chain_name': self.chain_name,
            'value': self.value
        }
    
class MedianTransactionValue(db.Model):
    __tablename__ = 'median_trx_value'
    date = db.Column(db.DateTime, primary_key=True)
    chain_name = db.Column(db.String)
    value = db.Column(db.Integer)

    def serialize(self):
        return {
            'date': self.date,
            'chain_name': self.chain_name,
            'value': self.value
        }
    
class CumulativeNumberOfTransactions(db.Model):
    __tablename__ = 'cumulative_number_of_trx'
    date = db.Column(db.DateTime, primary_key=True)
    chain_name = db.Column(db.String)
    value = db.Column(db.Integer)

    def serialize(self):
        return {
            'date': self.date,
            'chain_name': self.chain_name,
            'value': self.value
        }
    
class ActiveAddresses(db.Model):
    __tablename__ = 'active_addresses'
    date = db.Column(db.DateTime, primary_key=True)
    chain_name = db.Column(db.String)
    value = db.Column(db.Integer)

    def serialize(self):
        return {
            'date': self.date,
            'chain_name': self.chain_name,
            'value': self.value
        }
    
class TransactionsPerSecond(db.Model):
    __tablename__ = 'trx_per_second'
    date = db.Column(db.DateTime, primary_key=True)
    chain_name = db.Column(db.String)
    value = db.Column(db.Integer)

    def serialize(self):
        return {
            'date': self.date,
            'chain_name': self.chain_name,
            'value': self.value
        }
