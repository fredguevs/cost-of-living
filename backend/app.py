import flask
from flask_cors import CORS
import scraper

app = flask.Flask(__name__)

CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

@app.route("/api/city/<city_name>", methods=["GET"])
def get_city(city_name):
    get_city_data = scraper.get_city_data(city_name)
    return get_city_data

@app.route("/api/cities", methods=["GET"])
def get_cities():
    city_names = scraper.get_city_names()
    city_array = [{"label": name, "value": slug}
                  for name, slug in city_names.items()]
    city_array.sort(key=lambda x: x["label"].lower())
    return flask.jsonify(city_array)

if __name__ == "__main__":
    app.run(debug=True)
