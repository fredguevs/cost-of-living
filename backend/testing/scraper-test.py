from bs4 import BeautifulSoup
import requests
import pprint
from collections import OrderedDict

url = f"https://www.numbeo.com/cost-of-living/in/New-York"

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

pprint.pprint(city_details)


