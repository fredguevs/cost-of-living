from flask import jsonify
from api import app
from db.model import execute_query


@app.route("/api/rentcast/<path:city_slug>/<path:item_name>", methods=["GET"])
def get_rentcast_data(city_slug, item_name):
    # look up item_id
    item_row = execute_query(
        "SELECT id FROM items WHERE name = %s",
        (item_name,),
        fetchone=True
    )
    if not item_row:
        return jsonify({"error": f"No Rentcast item '{item_name}'."}), 404
    item_id = item_row["id"]

    # look up city_id
    city_row = execute_query(
     "SELECT id FROM cities WHERE slug = %s",
      (city_slug,), fetchone=True
    )
    if not city_row:
        return jsonify({"error": f"No Rentcast city '{city_name}'."}), 404
    city_id = city_row["id"]

    # query the correct table/column
    rows = execute_query(
        """
        SELECT year, month, average_rent AS price
        FROM rentcast_prices
        WHERE city_id = %s AND item_id = %s
        ORDER BY year, month
        """,
        (city_id, item_id),
        fetchall=True
    )

    result = [
        {
            "date": f"{r['year']}-{str(r['month']).zfill(2)}",
            "price": float(r["price"]),
        }
        for r in rows
    ]
    return jsonify(result)
