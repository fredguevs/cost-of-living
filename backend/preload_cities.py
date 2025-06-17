from scraper import get_city_names
from db.model import execute_query, get_cursor, get_db
from api import app  # import your Flask app


def preload_city_names_only(): 
    city_names = get_city_names()
    db = get_db()
    cur = get_cursor()

    for name, slug in list(city_names.items())[:50]:  # preload only 50 cities
        print(f"Inserting {name}...")

        # Avoid duplicate insert
        exists = execute_query(
            "SELECT 1 FROM cities WHERE slug = %s", (slug,), fetchone=True)
        if exists:
            print(f"Skipping {name}, already exists.")
            continue

        #TODO: Add ZIP code lookup

        #TODO : Add state extraction from name

        # Insert into cities table
        cur.execute(
            "INSERT INTO cities (name, slug) VALUES (%s, %s)", (name, slug))
        db.commit()

    print("City names preloaded.")


if __name__ == "__main__":
    with app.app_context():
        preload_city_names_only()
