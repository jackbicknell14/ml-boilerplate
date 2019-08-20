import datetime
from predictor import db, ma

# Product class/model
class PersistentModel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), unique=True)
	params = db.Column(db.String(200))
	upload_time = db.Column(db.DateTime, default=datetime.datetime.utcnow())
	in_use = db.Column(db.Boolean)

	def __init__(self, name, params, upload_time, in_use):
		self.name = name
		self.params = params
		self.upload_time = upload_time
		self.in_use = in_use

# Product schema
class PersistentModelSchema(ma.Schema):
	class Meta:
		fields = ('id', 'name', 'params', 'upload_time', 'in_use')
