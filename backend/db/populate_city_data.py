from scraper import get_city_data
from db.model import execute

city_slug = "Ann-Arbor-MI-United-States"
city_id = execute("SELECT id FROM cities WHERE slug=%s;",
                  (city_slug,), fetchone=True)['id']
city_data = get_city_data(city_slug)

for category, items in city_data.items():
    for item in items:
        execute("""
            INSERT INTO numbeo_data (city_id, category, item_name, price)
            VALUES (%s, %s, %s, %s);
        """, (city_id, category, item['name'], item['price']))

print("City data inserted.")
