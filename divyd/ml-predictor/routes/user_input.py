from flask import request, jsonify
from models.user_input import *

# Init schema
user_input_schema = UserInputSchema(strict=True)
user_inputs_schema = UserInputSchema(many=True, strict=True)


# Create a model
@app.route('/user_input', methods=['POST'])
def add_model():
	name = request.json['name']
	params = request.json['params']
	print(request.json)
	if 'upload_time' in request.json:
		upload_time = request.json['upload_time']
	else:
		upload_time = None
	in_use = request.json['in_use']

	new_model = PersistentModel(name, params, upload_time, in_use)

	db.session.add(new_model)
	db.session.commit()

	return model_schema.jsonify(new_model)


# Get all models
@app.route('/user_input', methods=['GET'])
def get_models():
	all_models = PersistentModel.query.all()
	result = models_schema.dump(all_models)
	return jsonify(result.data)


# Get single product
@app.route('/user_input/<id>', methods=['GET'])
def get_product(id):
	product = PersistentModel.query.get(id)
	return model_schema.jsonify(product)
