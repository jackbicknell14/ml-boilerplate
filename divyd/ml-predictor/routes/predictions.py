from flask import request, jsonify
from models.predictions import *

### Predictions routes


# Create a model
@app.route('/model', methods=['POST'])
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
@app.route('/model', methods=['GET'])
def get_models():
	all_models = PersistentModel.query.all()
	result = models_schema.dump(all_models)
	return jsonify(result.data)


# Get single product
@app.route('/model/<id>', methods=['GET'])
def get_product(id):
	product = PersistentModel.query.get(id)
	return model_schema.jsonify(product)
