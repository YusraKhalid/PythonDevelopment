from flask import Flask

app = Flask(__name__)
app.secret_key = 'jkghkdhgklfgh5kflgjkfhj8ty89jf'
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Blog.db'

from flicker import models
from flicker import views
