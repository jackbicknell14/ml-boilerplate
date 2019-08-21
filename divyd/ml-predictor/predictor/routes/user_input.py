from flask import request, jsonify
from predictor import app

from predictor.models.user_input import *

# Create a user_input
@app.route('/user_input', methods=['POST'])
def add_user_input():
	customer_id = request.json['customer_id']
	category = request.json['category']
	if 'upload_time' in request.json:
		upload_time = request.json['upload_time']
	else:
		upload_time = None
	weekday = request.json['weekday']
	day_of_month = request.json['day_of_month']

	new_user_input = UserInput(customer_id, category, weekday, day_of_month, upload_time)

	db.session.add(new_user_input)
	db.session.commit()

	return user_input_schema.jsonify(new_user_input)


# Get all user_inputs
@app.route('/user_input', methods=['GET'])
def get_user_inputs():
	all_user_inputs = UserInput.query.all()
	result = user_inputs_schema.dump(all_user_inputs)
	return jsonify(result)


# Get single user_input
@app.route('/user_input/<id>', methods=['GET'])
def get_user_input(id):
	product = UserInput.query.get(id)
	return user_input_schema.jsonify(product)



# Update a user_input
@app.route('/user_input/<id>', methods=['PUT'])
def update_user_input(id):
	user_input = UserInput.query.get(id)
	customer_id = request.json['customer_id']
	category = request.json['category']
	weekday = request.json['weekday']
	day_of_month = request.json['day_of_month']

	user_input.customer_id = customer_id
	user_input.category = category
	user_input.weekday = weekday
	user_input.day_of_month = day_of_month

	db.session.commit()

	return user_input_schema.jsonify(user_input)

# Delete a user_input
@app.route('/user_input/<id>', methods=['DELETE'])
def delete_user_input(id):
	user_input = UserInput.query.get(id)
	db.session.delete(user_input)
	db.session.commit()

	return user_input_schema.jsonify(user_input)
