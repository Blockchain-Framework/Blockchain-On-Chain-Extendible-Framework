from flask_sqlalchemy import SQLAlchemy
from ..database.database import db


class MetricBase(db.Model):
    __abstract__ = True  # This makes MetricBase an abstract class
    date = db.Column(db.DateTime, primary_key=True)
    blockchain = db.Column(db.String, primary_key=True)
    subchain = db.Column(db.String, primary_key=True)
    value = db.Column(db.Float)

    def serialize(self):
        return {
            'date': self.date,
            'blockchain': self.blockchain,
            'subchain': self.subchain,
            'value': self.value
        }


class Metric(db.Model):
    __tablename__ = 'metric_table'
    metric_name = db.Column(db.String, primary_key=True)
    description = db.Column(db.String)
    display_name = db.Column(db.String)

    def serialize(self):
        return {
            'metric_name': self.metric_name,
            'description': self.description,
            'display_name': self.display_name
        }


class TransactionsPerDay(MetricBase):
    __tablename__ = 'trx_per_day'


class TotalTransactions(MetricBase):
    __tablename__ = 'total_transactions'


class AverageTransactionAmount(MetricBase):
    __tablename__ = 'average_transaction_amount'


class AvgTrxsPerHour(MetricBase):
    __tablename__ = 'avg_trxs_per_hour'


class TotalBlocks(MetricBase):
    __tablename__ = 'total_blocks'


class TrxPerBlock(MetricBase):
    __tablename__ = 'trx_per_block'


class ActiveAddresses(MetricBase):
    __tablename__ = 'active_addresses'


class ActiveSenders(MetricBase):
    __tablename__ = 'active_senders'


class SumEmittedUtxoAmount(MetricBase):
    __tablename__ = 'sum_emitted_utxo_amount'


class AvgEmittedUtxoAmount(MetricBase):
    __tablename__ = 'avg_emitted_utxo_amount'


class MedianEmittedUtxoAmount(MetricBase):
    __tablename__ = 'median_emitted_utxo_amount'


class SumConsumedUtxoAmount(MetricBase):
    __tablename__ = 'sum_consumed_utxo_amount'


class AvgConsumedUtxoAmount(MetricBase):
    __tablename__ = 'avg_consumed_utxo_amount'


class MedianConsumedUtxoAmount(MetricBase):
    __tablename__ = 'median_consumed_utxo_amount'


class LargeTrx(MetricBase):
    __tablename__ = 'large_trx'


class WhaleAddressActivity(MetricBase):
    __tablename__ = 'whale_address_activity'
