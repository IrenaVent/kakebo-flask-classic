from flask import Flask  

# aquí se crea aplicación flask
app = Flask(__name__)

# tiene que estar situado depués de hacer la app
from balance import views
