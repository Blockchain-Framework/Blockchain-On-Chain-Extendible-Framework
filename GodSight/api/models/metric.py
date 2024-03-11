from ..database.database import db
from datetime import datetime



# class Metric(db.Model):
#     __tablename__ = 'metric_table'
#     metric_name = db.Column(db.String, primary_key=True)
#     description = db.Column(db.String)
#     display_name = db.Column(db.String)
#
#     def serialize(self):
#         return {
#             'metric_name': self.metric_name,
#             'description': self.description,
#             'display_name': self.display_name
#         }

class Metric(db.Model):
    __tablename__ = 'metric_table'
    metric_name = db.Column(db.String(255), primary_key=True)
    display_name = db.Column(db.String(255))
    description = db.Column(db.Text)
    category = db.Column(db.String(255))
    type = db.Column(db.String(255))
    grouping_type = db.Column(db.String(255))
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def serialize(self):
        return {
            'metric_name': self.metric_name,
            'display_name': self.display_name,
            'description': self.description,
            'category': self.category,
            'type': self.type,
            'grouping_type': self.grouping_type,
            'create_date': self.create_date.isoformat(),
            'update_date': self.update_date.isoformat(),
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



