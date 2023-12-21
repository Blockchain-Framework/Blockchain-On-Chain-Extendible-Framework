from flask_sqlalchemy import SQLAlchemy
from app import db

class DailyTransactionCount(db.Model):
    __tablename__ = 'daily_transaction_count'
    date = db.Column(db.String, primary_key=True)
    chain_name = db.Column(db.String)
    count = db.Column(db.Integer)

    def serialize(self):
        return {
            'date': self.date,
            'chain_name': self.chain_name,
            'value': self.count
        }

class AverageTransactionsPerBlock(db.Model):
    __tablename__ = 'average_transactions_per_block'
    date = db.Column(db.String, primary_key=True)
    chain_name = db.Column(db.String)
    avg_transactions_per_block = db.Column(db.Float)

    def serialize(self):
        return {
            'date': self.date,
            'chain_name': self.chain_name,
            'value': self.avg_transactions_per_block
        }

class TotalStakedAmount(db.Model):
    __tablename__ = 'total_staked_amount'
    date = db.Column(db.String, primary_key=True)
    chain_name = db.Column(db.String)
    total_staked_amount = db.Column(db.Float)

    def serialize(self):
        return {
            'date': self.date,
            'chain_name': self.chain_name,
            'value': self.total_staked_amount
        }

class TotalBurnedAmount(db.Model):
    __tablename__ = 'total_burned_amount'
    date = db.Column(db.String, primary_key=True)
    chain_name = db.Column(db.String)
    total_burned_amount = db.Column(db.Float)

    def serialize(self):
        return {
            'date': self.date,
            'chain_name': self.chain_name,
            'value': self.total_burned_amount
        }

class AverageTransactionValue(db.Model):
    __tablename__ = 'average_transaction_value'
    date = db.Column(db.String, primary_key=True)
    chain_name = db.Column(db.String)
    average_transaction_value = db.Column(db.Float)

    def serialize(self):
        return {
            'date': self.date,
            'chain_name': self.chain_name,
            'value': self.average_transaction_value
        }

class LargeTransactionMonitoring(db.Model):
    __tablename__ = 'large_transaction_monitoring'
    date = db.Column(db.String, primary_key=True)
    chain_name = db.Column(db.String)
    large_transaction_count = db.Column(db.Integer)

    def serialize(self):
        return {
            'date': self.date,
            'chain_name': self.chain_name,
            'value': self.large_transaction_count
        }

class CrossChainWhaleActivity(db.Model):
    __tablename__ = 'cross_chain_whale_activity'
    date = db.Column(db.String, primary_key=True)
    chain_name = db.Column(db.String)
    cross_chain_large_transaction_count = db.Column(db.Integer)

    def serialize(self):
        return {
            'date': self.date,
            'chain_name': self.chain_name,
            'value': self.cross_chain_large_transaction_count
        }
