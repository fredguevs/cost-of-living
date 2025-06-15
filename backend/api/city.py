from flask import jsonify
from api import app
from scraper import get_city_data, get_city_names
from db.model import execute_query


@app.route("/api/cities", methods=["GET"])
def get_cities():
    data = execute_query(
        "SELECT name, slug FROM cities ORDER BY name ASC", fetchall=True)
    city_array = [{"label": row["name"], "value": row["slug"]} for row in data]
    return jsonify(city_array)


@app.route("/api/city/<slug>", methods=["GET"])
def get_city(slug):
    # Try to fetch city data from DB
    data = execute_query("""
        SELECT numbeo_data.category, items.name AS item_name, numbeo_data.price
        FROM numbeo_data
        JOIN cities ON cities.id = numbeo_data.city_id
        JOIN items ON items.id = numbeo_data.item_id
        WHERE cities.slug = %s
    """, (slug,), fetchall=True)

    if data:
        # Group data into category -> list of items
        grouped = {}
        for row in data:
            if row["category"] not in grouped:
                grouped[row["category"]] = []
            grouped[row["category"]].append({
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
            item_row = execute_query("""
                SELECT id FROM items WHERE name = %s
            """, (item["name"],), fetchone=True)


            item_id = item_row["id"] if item_row else None

            execute_query("""
                INSERT INTO numbeo_data (city_id, category, item_id, price)
                VALUES (%s, %s, %s, %s)
            """, (city_id, category, item_id, item["price"]))

    return jsonify(scraped)