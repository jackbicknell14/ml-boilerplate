from flask import request, jsonify
from models.persistent_models import *

### Models routes
# Init schema
model_schema = PersistentModelSchema(strict=True)
models_schema = PersistentModelSchema(many=True, strict=True)


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



# Update a model
@app.route('/model/<id>', methods=['PUT'])
def update_model(id):
	product = PersistentModel.query.get(id)

	name = request.json['name']
	params = request.json['params']
	in_use = request.json['in_use']

	model.name = name
	model.params = params
	model.in_use = in_use

	db.session.commit()

	return model_schema.jsonify(model)

# Delete a model
@app.route('/model/<id>', methods=['DELETE'])
def delete_product(id):
	model = PersistentModel.query.get(id)
	db.session.delete(model)
	db.session.commit()

	return model_schema.jsonify(model)
