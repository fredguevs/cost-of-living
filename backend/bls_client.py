# fetch_bls_data.py
import requests
import json
from config import BLS_API_KEY
from db.model import get_db, get_cursor, execute_query
from api import app

BLS_API_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"


def fetch_and_store_bls_data(start_year="2020", end_year="2025"):
    db = get_db()
    cur = get_cursor()

    # Get all items with a BLS series ID
    items = execute_query(
        "SELECT id, bls_series_id FROM items WHERE bls_series_id IS NOT NULL", fetchall=True)

    for item in items:
        item_id = item["id"]
        series_id = item["bls_series_id"]
        print(f"Fetching BLS data for series {series_id}")

        payload = {
            "seriesid": [series_id],
            "startyear": start_year,
            "endyear": end_year,
            "registrationkey": BLS_API_KEY
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(
            BLS_API_URL, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            data = response.json()
            try:
                series = data["Results"]["series"][0]["data"]
            except (KeyError, IndexError):
                print(f"No data found for {series_id}")
                continue

            for entry in series:
                year = int(entry["year"])
                month = int(entry["period"][1:])  # "M01" -> 1
                price = float(entry["value"])

                cur.execute("""
                    INSERT INTO bls_data (item_id, year, month, price) 
                    VALUES (%s, %s, %s, %s) 
                    ON CONFLICT (item_id, year, month)
                    DO UPDATE 
                    SET price = EXCLUDED.price
                """, (item_id, year, month, price))
        else:
            print(
                f"Error fetching data for {series_id}: {response.status_code} {response.text}")

    db.commit()
    print("Finished fetching and storing BLS data.")


if __name__ == "__main__":
    with app.app_context():
        fetch_and_store_bls_data()
