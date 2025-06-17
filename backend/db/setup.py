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
    slug TEXT UNIQUE NOT NULL, 
    zip_centre TEXT, 
    zip_suburb TEXT, 
    state TEXT, 
    UNIQUE(name, slug) 
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS numbeo_data (
    id SERIAL PRIMARY KEY,
    city_id INTEGER REFERENCES cities(id),
    item_id INTEGER REFERENCES items(id),
    category TEXT NOT NULL,
    price TEXT NOT NULL,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS items(
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    bls_series_id TEXT UNIQUE,
    unit TEXT
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS bls_data (
    id SERIAL PRIMARY KEY,
    item_id INTEGER REFERENCES items(id),
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    price NUMERIC,
    UNIQUE(item_id, year, month)
);
""")

conn.commit()
cur.close()
conn.close()

print("✅ Tables created successfully.")
