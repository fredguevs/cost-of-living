from scraper import get_city_names

city_names = get_city_names()

for name, slug in list(city_names.items()):  # preload only 50 cities
    parts = name.split(", ")
    city = parts[0]
    state = parts[1]
    print(f"Inserting {city} {state}...")
