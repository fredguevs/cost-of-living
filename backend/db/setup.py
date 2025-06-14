# db/setup.py
import psycopg2

conn = psycopg2.connect(
    dbname="cost_of_living",
    user="frederick",
    password="",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS cities (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS numbeo_data (
    id SERIAL PRIMARY KEY,
    city_id INTEGER REFERENCES cities(id),
    category TEXT NOT NULL,
    item_name TEXT NOT NULL,
    price TEXT NOT NULL,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

conn.commit()
cur.close()
conn.close()

print("✅ Tables created successfully.")
