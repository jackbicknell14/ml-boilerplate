import datetime
from predictor import db, ma

# Result input class/model
class Prediction(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	model_id = db.Column(db.Integer, db.ForeignKey('persistent_model.id'), nullable=False)
	customer_id = db.Column(db.Integer)
	prediction = db.Column(db.Text)
	prediction_time = db.Column(db.DateTime, default=datetime.datetime.utcnow())


	def __init__(self, model_id, customer_id, prediction, prediction_time):
		self.model_id = model_id
		self.customer_id = customer_id
		self.prediction = prediction
		self.prediction_time = prediction_time

# Result input schema
class PredictionSchema(ma.Schema):
	class Meta:
		fields = ('id', 'model_id', 'customer_id', 'prediction', 'prediction_time')

prediction_schema = PredictionSchema()
predictions_schema = PredictionSchema(many=True)
