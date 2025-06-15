from db.model import get_db, get_cursor, execute_query
from api import app
from difflib import get_close_matches

bls_series_map = {
    # Food & Groceries
    "Milk (regular), (1 gallon)": "APU0000709111",
    "Loaf of Fresh White Bread (1 lb)": "APU0000701111",
    "Rice (white), (1 lb)": "APU0000702111",
    "Eggs (regular) (12)": "APU0000709112",
    "Local Cheese (1 lb)": "APU0000710111",
    "Chicken Fillets (1 lb)": "APU0000706111",
    "Beef Round (1 lb) (or Equivalent Back Leg Red Meat)": "APU0000703112",
    "Apples (1 lb)": "APU0000711112",
    "Banana (1 lb)": "APU0000711111",
    "Oranges (1 lb)": "APU0000711311",
    "Potato (1 lb)": "APU0000710211",
    "Tomato (1 lb)": "APU0000712111",
    "Cappuccino (regular)": "APU0000720111",  # Closest match to ground coffee
    "Coffee (regular)": "APU0000720111",  # In case you renamed it manually
    "Sugar (1 lb)": "APU0000721111",
    "Onion (1 lb)": "APU0000712404",
    "Lettuce (1 head)": "APU0000712211",
    "Bottle of Wine (Mid-Range)": "APU0000720311",

    # Utilities / Energy
    "Electricity": "APU000072610",
    "Natural Gas": "APU000072611",
    "Gasoline (1 gallon)": "APU000074714",

    # Items without known BLS matches
    "Meal, Inexpensive Restaurant": None,
    "Meal for 2 People, Mid-range Restaurant, Three-course": None,
    "McMeal at McDonalds (or Equivalent Combo Meal)": None,
    "Domestic Beer (1 pint draught)": None,
    "Imported Beer (12 oz small bottle)": None,
    "Coke/Pepsi (12 oz small bottle)": None,
    "Water (12 oz small bottle)": None,

    "Water (1.5 liter bottle)": None,
    "Domestic Beer (0.5 liter bottle)": None,
    "Cigarettes 20 Pack (Marlboro)": None,
    "One-way Ticket (Local Transport)": None,
    "Monthly Pass (Regular Price)": None,
    "Taxi Start (Normal Tariff)": None,
    "Taxi 1 mile (Normal Tariff)": None,
    "Taxi 1hour Waiting (Normal Tariff)": None,
    "Volkswagen Golf 1.4 90 KW Trendline (Or Equivalent New Car)": None,
    "Toyota Corolla Sedan 1.6l 97kW Comfort (Or Equivalent New Car)": None,
    "Basic (Electricity, Heating, Cooling, Water, Garbage) for 915 sq ft Apartment": None,
    "Mobile Phone Monthly Plan with Calls and 10GB+ Data": None,
    "Internet (60 Mbps or More, Unlimited Data, Cable/ADSL)": None,
    "Fitness Club, Monthly Fee for 1 Adult": None,
    "Tennis Court Rent (1 Hour on Weekend)": None,
    "Cinema, International Release, 1 Seat": None,
    "Preschool (or Kindergarten), Full Day, Private, Monthly for 1 Child": None,
    "International Primary School, Yearly for 1 Child": None,
    "1 Pair of Jeans (Levis 501 Or Similar)": None,
    "1 Summer Dress in a Chain Store (Zara, H&M, ...)": None,
    "1 Pair of Nike Running Shoes (Mid-Range)": None,
    "1 Pair of Men Leather Business Shoes": None,
    "Apartment (1 bedroom) in City Centre": None,
    "Apartment (1 bedroom) Outside of Centre": None,
    "Apartment (3 bedrooms) in City Centre": None,
    "Apartment (3 bedrooms) Outside of Centre": None,
    "Price per Square Feet to Buy Apartment in City Centre": None,
    "Price per Square Feet to Buy Apartment Outside of Centre": None,
    "Average Monthly Net Salary (After Tax)": None,
    "Mortgage Interest Rate in Percentages (%), Yearly, for 20 Years Fixed-Rate": None,
}



def update_bls_ids_fuzzy():
    """Adds BLS series ids to items table."""
    db = get_db()
    cur = get_cursor()

    # Get all current item names
    items = execute_query("SELECT id, name FROM items", fetchall=True)

    updated = 0
    for item in items:
        item_id, name = item["id"], item["name"]

        # Find best match in BLS series map using fuzzy matching
        match = get_close_matches(
            name, bls_series_map.keys(), n=1, cutoff=0.95)

        if match:
            matched_name = match[0]
            series_id = bls_series_map[matched_name]
            print(f"Matched '{name}' -> '{matched_name}'")

            cur.execute("""
                UPDATE items
                SET bls_series_id = %s
                WHERE id = %s
            """, (series_id, item_id))
            updated += 1
        else:
            print(f"No match for '{name}'")

    db.commit()
    print(f"Updated {updated} items with BLS series IDs.")


if __name__ == "__main__":
    with app.app_context():
        update_bls_ids_fuzzy()
