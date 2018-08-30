from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
marshmallow_app = Marshmallow(app)
db.metadata.clear()
