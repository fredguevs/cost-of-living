from flask import Flask
from flask_cors import CORS
from db.connection import close_db

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

# Import route handlers
from api import city  # noqa: E402


@app.teardown_appcontext
def teardown(exception):
    close_db(exception)
