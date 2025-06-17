from scraper import get_items
from db.model import execute_query, get_cursor, get_db
from api import app  # import your Flask app


def preload_item_names():
    """Preload item names into the database from Numbeo"""
    print("Starting preload...")
    items = get_items()
    db = get_db()
    cur = get_cursor()

    for item_name in items:
        # Insert item name, skip if it already exists
        cur.execute("""
            INSERT INTO items (name) 
            VALUES (%s) 
            ON CONFLICT (name) DO NOTHING
        """, (item_name,))

    db.commit()
    print("Item names preloaded.")


if __name__ == "__main__":
    with app.app_context():
        preload_item_names()
