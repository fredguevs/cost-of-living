from bs4 import BeautifulSoup
import requests
import pprint
from collections import OrderedDict


def get_city_data(city_name):
    """Fetches the cost of living data for a given city from Numbeo."""
    
    url = f"https://www.numbeo.com/cost-of-living/in/{city_name}"

    result = requests.get(url).text
    doc = BeautifulSoup(result, "html.parser")

    table = doc.find("table", class_="data_wide_table new_bar_table")
    city_details = OrderedDict()
    category = ""
    

    for tr in table.find_all("tr"):
        if tr.find("th"):
            category = tr.find("th").text.strip()
            city_details[category] = []
        else:
            tds = tr.find_all("td")
            if len(tds) >= 2:
                item = tds[0].text.strip()
                price = tds[1].text.replace("\xa0", "").strip()
                city_details[category].append({
                    "name": item,
                    "price": price
                })
        
    return city_details


def get_city_names():
    """Fetches the list of city names from Numbeo."""

    url = "https://www.numbeo.com/cost-of-living/country_result.jsp?country=United+States"
    result = requests.get(url).text
    doc = BeautifulSoup(result, "html.parser")

    table = doc.find("table", id="t2")
    tbody = table.find("tbody")
    rows = tbody.find_all("tr")

    # Hold city names and links for each city
    links = {}

    for tr in rows:
        # Find the link for each city
        link = tr.find("a", class_="discreet_link")
        # e.g., /cost-of-living/in/Ann-Arbor-MI-United-States
        full_href = link.get("href")
        slug = full_href.split("/in/")[1]  # take just the slug
        links[link.string] = slug

    return links

def get_items():
    """Fetches the list of items from Numbeo."""
    
    url = f"https://www.numbeo.com/cost-of-living/in/New-York"


    result = requests.get(url).text
    doc = BeautifulSoup(result, "html.parser")

    table = doc.find("table", class_="data_wide_table new_bar_table")

    items = []

    for tr in table.find_all("tr"):
        # Find the item name
        tds = tr.find_all("td")
        if len(tds) >= 2:
            # The first td contains the item name
            item_name = tds[0].text.strip()
            items.append(item_name)

    return items

