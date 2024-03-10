from flask_sqlalchemy import SQLAlchemy
from ..database.database import db




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

class MetricsData(db.Model):
    __tablename__ = 'metrics_data'
    date = db.Column(db.Date, primary_key=True)
    blockchain = db.Column(db.String(255), primary_key=True)
    subchain = db.Column(db.String(255), primary_key=True)
    metric = db.Column(db.String(255), primary_key=True)
    value = db.Column(db.Float)

    def serialize(self):
        return {
            'date': self.date,
            'blockchain': self.blockchain,
            'subchain': self.subchain,
            'metric': self.metric,
            'value': self.value
        }