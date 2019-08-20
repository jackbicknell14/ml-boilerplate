import datetime
from predictor import db, ma

# User input class/model
class UserInput(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	customer_id = db.Column(db.Integer)
	category = db.Column(db.String(200))
	weekday = db.Column(db.String(100))
	day_of_month = db.Column(db.Integer)

	def __init__(self, customer_id, category, upload_time, in_use):
		self.customer_id = customer_id
		self.category = category
		self.weekday = weekday
		self.day_of_month = day_of_month

# User input schema
class UserInputSchema(ma.Schema):
	class Meta:
		fields = ('id', 'customer_id', 'category', 'weekday', 'day_of_month')
