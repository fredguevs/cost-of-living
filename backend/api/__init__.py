from flask import Flask
from flask_cors import CORS
from db.connection import close_db

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Route handlers
from api import city  
from api import bls
from api import rentcast


@app.teardown_appcontext
def teardown(exception):
    close_db(exception)
