import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COUNTRIES_LIST = os.path.join(BASE_DIR, "countries.json")

with open(COUNTRIES_LIST, 'r') as f:
    COUNTRIES = json.load(f)


def get_country_extent(alpha3_code):
    country = COUNTRIES.get(alpha3_code)

    if not country:
        return None

    return country.get("bbox")
