from bs4 import BeautifulSoup
import requests
import pprint

def get_city_data(city_name):
    """
    Fetches the cost of living data for a given city from Numbeo.
    
    Args:
        city_name (str): The name of the city to fetch data for.
        
    Returns:
        dict: A dictionary containing the cost of living data for the city.
    """
    url = f"https://www.numbeo.com/cost-of-living/in/{city_name}"

    result = requests.get(url).text
    doc = BeautifulSoup(result, "html.parser")

    table = doc.find("table", class_="data_wide_table new_bar_table")

    city_details = {}

    for tr in table.find_all("tr"):
        tds = tr.find_all("td")
        if len(tds) >= 2:
            item = tds[0].text.strip()
            price = tds[1].text.replace("\xa0", "").strip()
            city_details[item] = price

    return city_details


def get_city_names():
    """
    Fetches the list of city names from Numbeo.
    
    Returns:
        list: A list of city names.
    """
    from bs4 import BeautifulSoup


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
