import requests
import json
from config import RENTCAST_API_KEY
from db.model import get_db, get_cursor, execute_query
from api import app
from datetime import datetime


def fetch_and_store_rentcast_data():
  db = get_db()
  cur = get_cursor()

  months_so_far = datetime.now()
  num_months = months_so_far.month + 12

  cur.execute("""
      SELECT name, state, zip_centre, zip_suburb FROM cities;
  """)


  cities = cur.fetchall()


  for city in cities:
    center_zip = city["zip_centre"]
    # suburb_zip = city["zip_suburb"] because of limited api access, we'll just use the center zip code

    cur.execute("SELECT id FROM cities WHERE zip_centre = %s",
                (center_zip,))
    city_id = cur.fetchone()["id"]

    url = f'https://api.rentcast.io/v1/markets?zipCode={center_zip}&dataType=Rental&historyRange={num_months}'

    response = requests.get(
      url,
      headers={
        "X-Api-Key": RENTCAST_API_KEY,
        "accept": "application/json"
      }
    )

    

    if response.status_code == 200:
      print(f"Success for ZIP {center_zip}")
      data = response.json()

      for date in data["rentalData"]["history"]:
        
        year, month = map(int, date.split("-"))
        data_by_bedrooms = data["rentalData"]["history"][date]["dataByBedrooms"]

    # Parse the date

        # get the city_id from the database
        

        for bedroom in data_by_bedrooms:
          average_rent = bedroom["averageRent"]
          if average_rent is None:
            continue

          if bedroom["bedrooms"] == 1:
            # `id | 48
            # name | Apartment(1 bedroom) in City Centre
            cur.execute("""
              INSERT INTO rentcast_prices (city_id, item_id, average_rent, month, year)
              VALUES (%s, %s, %s, %s, %s)
              ON CONFLICT (city_id, item_id, month, year) DO UPDATE
              SET average_rent = EXCLUDED.average_rent
            """, (city_id, 48, average_rent, month, year))
          elif bedroom["bedrooms"] == 3:
            # id | 50
            # name | Apartment(3 bedrooms) in City Centre
            cur.execute("""
              INSERT INTO rentcast_prices (city_id, item_id, average_rent, month, year)
              VALUES (%s, %s, %s, %s, %s)
              ON CONFLICT (city_id, item_id, month, year) DO UPDATE
              SET average_rent = EXCLUDED.average_rent
            """, (city_id, 50, average_rent, month, year))

        db.commit()

    else:
      raise Exception(f"Non-success status code: {response.status_code}")




if __name__ == "__main__":
    with app.app_context():
        fetch_and_store_rentcast_data()
