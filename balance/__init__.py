from flask import Flask  

# aquí se crea aplicación flask
app = Flask(__name__, instance_relative_config=True)
app.config.from_object("config")

# tiene que estar situado depués de hacer la app
from balance.views import *
