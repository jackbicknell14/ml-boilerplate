import datetime
from predictor import db, ma

# Product class/model
class PersistentModel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), unique=True)
	params = db.Column(db.String(200))
	upload_time = db.Column(db.DateTime, default=datetime.datetime.utcnow())
	in_use = db.Column(db.Boolean)
	predictions = db.relationship('Prediction', backref='author', lazy='dynamic')

	def __init__(self, name, params, upload_time, in_use, predictions):
		self.name = name
		self.params = params
		self.upload_time = upload_time
		self.in_use = in_use
		self.predictions = predictions

# Product schema
class PersistentModelSchema(ma.Schema):
	class Meta:
		fields = ('id', 'name', 'params', 'upload_time', 'in_use')

# Init schema
model_schema = PersistentModelSchema(strict=True)
models_schema = PersistentModelSchema(many=True, strict=True)