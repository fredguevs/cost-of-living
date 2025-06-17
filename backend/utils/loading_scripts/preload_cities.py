from scraper import get_city_names
from db.model import execute_query, get_cursor, get_db
from api import app  # import your Flask app

# Hardcoded for now
city_zip_map = {
    "New York, NY":         {"center": "10007", "suburb": "11354"},
    "Honolulu, HI":         {"center": "96813", "suburb": "96701"},
    "San Francisco, CA":    {"center": "94103", "suburb": "94608"},
    "Seattle, WA":          {"center": "98101", "suburb": "98052"},
    "San Jose, CA":         {"center": "95113", "suburb": "94401"},
    "Washington, DC":       {"center": "20001", "suburb": "22031"},
    "Boston, MA":           {"center": "02108", "suburb": "02446"},
    "Los Angeles, CA":      {"center": "90012", "suburb": "90210"},
    "San Diego, CA":        {"center": "92101", "suburb": "91910"},
    "Miami, FL":            {"center": "33131", "suburb": "33010"},
    "Philadelphia, PA":     {"center": "19102", "suburb": "19010"},
    "Sacramento, CA":       {"center": "95814", "suburb": "95608"},
    "New Orleans, LA":      {"center": "70112", "suburb": "70001"},
    "Denver, CO":           {"center": "80202", "suburb": "80014"},
    "Chicago, IL":          {"center": "60602", "suburb": "60007"},
    "Atlanta, GA":          {"center": "30303", "suburb": "30060"},
    "Portland, OR":         {"center": "97204", "suburb": "97034"},
    "Pittsburgh, PA":       {"center": "15222", "suburb": "15122"},
    "Minneapolis, MN":      {"center": "55401", "suburb": "55421"},
    "Colorado Springs, CO": {"center": "80903", "suburb": "80132"},
    "Spokane, WA":          {"center": "99201", "suburb": "99006"},
    "Dallas, TX":           {"center": "75201", "suburb": "75001"},
    "Tampa, FL":            {"center": "33602", "suburb": "33647"},
    "Nashville, TN":        {"center": "37203", "suburb": "37027"},
    "Baltimore, MD":        {"center": "21202", "suburb": "21090"},
    "Columbus, OH":         {"center": "43215", "suburb": "43081"},
    "Charlotte, NC":        {"center": "28202", "suburb": "28105"},
    "Phoenix, AZ":          {"center": "85004", "suburb": "85251"},
    "Raleigh, NC":          {"center": "27601", "suburb": "27511"},
    "Saint Louis, MO":      {"center": "63101", "suburb": "63303"},
    "Omaha, NE":            {"center": "68102", "suburb": "68124"},
    "Fort Worth, TX":       {"center": "76102", "suburb": "76092"},
    "Madison, WI":          {"center": "53703", "suburb": "53562"},
    "Las Vegas, NV":        {"center": "89101", "suburb": "89044"},
    "Orlando, FL":          {"center": "32801", "suburb": "32789"},
    "Kansas City, MO":      {"center": "64106", "suburb": "66062"},
    "Indianapolis, IN":     {"center": "46204", "suburb": "46250"},
    "Detroit, MI":          {"center": "48226", "suburb": "48219"},
    "Salt Lake City, UT":   {"center": "84111", "suburb": "84095"},
    "Tucson, AZ":           {"center": "85701", "suburb": "85650"},
    "Austin, TX":           {"center": "78701", "suburb": "78717"},
    "Houston, TX":          {"center": "77002", "suburb": "77070"},
    "Wichita, KS":          {"center": "67202", "suburb": "67220"},
    "Vancouver, WA":        {"center": "98660", "suburb": "98682"},
    "Cleveland, OH":        {"center": "44113", "suburb": "44124"},
    "Jacksonville, FL":     {"center": "32202", "suburb": "32073"},
    "San Antonio, TX":      {"center": "78205", "suburb": "78015"},
    "Albuquerque, NM":      {"center": "87102", "suburb": "87023"},
    "Cincinnati, OH":       {"center": "45202", "suburb": "45244"}
}



def preload_city_names_only(): 
    city_names = get_city_names()
    db = get_db()
    cur = get_cursor()

    for name, slug in list(city_names.items()):  # preload only 50 cities
        parts = name.split(", ")
        city_name = parts[0]
        state = parts[1]

        print(f"Inserting {city_name} {state}...")

        # Avoid duplicate insert
        exists = execute_query(
            "SELECT 1 FROM cities WHERE slug = %s", (slug,), fetchone=True)
        if exists:
            print(f"Skipping {city_name}, already exists.")
            continue

        #TODO: Add ZIP code lookup
        zip_centre = city_zip_map.get(name, {}).get("center")
        zip_suburb = city_zip_map.get(name, {}).get("suburb")

        # Insert into cities table
        cur.execute(
            "INSERT INTO cities (name, state, slug, zip_centre, zip_suburb) VALUES (%s, %s, %s, %s, %s)", (city_name, state, slug, zip_centre, zip_suburb))
        db.commit()

    print("City names preloaded.")


if __name__ == "__main__":
    with app.app_context():
        preload_city_names_only()
