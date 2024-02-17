from flask_sqlalchemy import SQLAlchemy
from ..database.database import db


# models.py
class Blockchain(db.Model):
    __tablename__ = 'blockchain_table'
    id = db.Column(db.Integer, primary_key=True)
    blockchain = db.Column(db.String(255), nullable=False)
    sub_chain = db.Column(db.String(255), nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    # ... other fields ...

    metrics = db.relationship('ChainMetric', back_populates='blockchain')


class ChainMetric(db.Model):
    __tablename__ = 'chain_metric'
    blockchain_id = db.Column(db.Integer, db.ForeignKey('blockchain_table.id'), primary_key=True)
    metric_name = db.Column(db.String(255), primary_key=True)
    # ... other fields ...

    blockchain = db.relationship('Blockchain', back_populates='metrics')
