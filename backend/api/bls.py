from flask import jsonify
from api import app
from db.model import execute_query


@app.route("/api/bls/<item_name>", methods=["GET"])
def get_bls_data(item_name):
    item_row = execute_query("""
        SELECT id FROM items WHERE name = %s
    """, (item_name,), fetchone=True)

    if item_row is None:
        return jsonify({"error": f"No BLS data found for item '{item_name}'."}), 404

    item_id = item_row["id"]

    data = execute_query("""
        SELECT year, month, price
        FROM bls_data
        WHERE item_id = %s
        ORDER BY year, month
    """, (item_id,), fetchall=True)

    result = [
        {
            "date": f"{row['year']}-{str(row['month']).zfill(2)}",
            "price": float(row["price"])
        }
        for row in data
    ]
    return jsonify(result)
