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

from routes import *
from models.persistent_models import *
from models.predictions import *
from models.user_input import *
