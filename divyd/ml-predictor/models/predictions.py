import datetime
from predictor import db, ma
from .persistent_models import PersistentModel

# Result input class/model
class Prediction(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	model_id = db.Column(db.Integer, db.ForeignKey('persistent_model.id'), nullable=False)
	customer_id = db.Column(db.Integer)
	prediction = db.Column(db.Float(200))

	def __init__(self, model_id, customer_id, prediction):
		self.model_id = model_id
		self.customer_id = customer_id
		self.prediction = prediction

# Result input schema
class PredictionSchema(ma.Schema):
	class Meta:
		fields = ('id', 'model_id', 'customer_id', 'prediction')

# Init schema
prediction_schema = PredictionSchema(strict=True)
predictions_schema = PredictionSchema(many=True, strict=True)
