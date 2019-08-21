from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

import os

# Init app
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

from .routes.persistent_models import *
from .routes.predictions import *
from .routes.user_input import *

from .models.persistent_models import PersistentModel
from .models.predictions import Prediction
from .models.user_input import UserInput

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'PersistentModel': PersistentModel, 'UserInput': UserInput, 'Prediction': Prediction}
