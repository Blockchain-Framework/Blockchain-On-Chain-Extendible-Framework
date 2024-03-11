from ..database.database import db
from datetime import datetime

# models.py
# class Blockchain(db.Model):
#     __tablename__ = 'blockchain_table'
#     id = db.Column(db.Integer, primary_key=True)
#     blockchain = db.Column(db.String(255), nullable=False)
#     sub_chain = db.Column(db.String(255), nullable=True)
#     start_date = db.Column(db.Date, nullable=False)
#     # ... other fields ...
#
#     metrics = db.relationship('ChainMetric', back_populates='blockchain')

class Blockchain(db.Model):
    __tablename__ = 'blockchain_table'
    id = db.Column(db.Integer, primary_key=True)
    blockchain = db.Column(db.String(255), primary_key=True)
    sub_chain = db.Column(db.String(255), primary_key=True)
    original = db.Column(db.Boolean, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    metrics = db.relationship('ChainMetric', back_populates='blockchain')

    def serialize(self):
        return {
            'id': str(self.id),
            'blockchain': self.blockchain,
            'sub_chain': self.sub_chain,
            'original': self.original,
            'start_date': self.start_date.isoformat(),
            'description': self.description,
            'create_date': self.create_date.isoformat(),
            'update_date': self.update_date.isoformat(),
        }
class ChainMetric(db.Model):
    __tablename__ = 'chain_metric'
    blockchain_id = db.Column(db.Integer, db.ForeignKey('blockchain_table.id'), primary_key=True)
    metric_name = db.Column(db.String(255), primary_key=True)
    blockchain = db.relationship('Blockchain', back_populates='metrics')
