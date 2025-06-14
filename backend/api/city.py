from flask import jsonify
from api import app
from scraper import get_city_data, get_city_names
from db.model import execute_query


@app.route("/api/cities", methods=["GET"])
def get_cities():
    city_names = get_city_names()
    city_array = [{"label": name, "value": slug}
                  for name, slug in city_names.items()]
    city_array.sort(key=lambda x: x["label"].lower())
    return jsonify(city_array)


@app.route("/api/city/<slug>", methods=["GET"])
def get_city(slug):
    # Try to fetch city data from DB
    data = execute_query("""
        SELECT category, item_name, price 
        FROM numbeo_data
        JOIN cities ON cities.id = numbeo_data.city_id
        WHERE cities.slug = %s
    """, (slug,), fetchall=True)

    if data:
        # Group data into category -> list of items
        grouped = {}
        for row in data:
            grouped.setdefault(row["category"], []).append({
                "name": row["item_name"],
                "price": row["price"]
            })
        return jsonify(grouped)

    # Fallback: scrape
    scraped = get_city_data(slug)
    if not scraped:
        return jsonify({"error": "City not found"}), 404

    # Insert city into DB if it doesn't exist
    execute_query("""
        INSERT INTO cities (name, slug) 
        VALUES (%s, %s) 
        ON CONFLICT (slug) DO NOTHING
    """, (slug.replace("-", " ").title(), slug))

    # Get city_id
    city = execute_query("""
        SELECT id FROM cities WHERE slug = %s
    """, (slug,), fetchone=True)
    city_id = city["id"]

    # Insert scraped data into numbeo_data
    for category, items in scraped.items():
        for item in items:
            execute_query("""
                INSERT INTO numbeo_data (city_id, category, item_name, price)
                VALUES (%s, %s, %s, %s)
            """, (city_id, category, item["name"], item["price"]))

    return jsonify(scraped)


@app.route("/api/db-test")
def test_db():
    result = execute_query("SELECT 1", fetchone=True)
    return jsonify(result)
