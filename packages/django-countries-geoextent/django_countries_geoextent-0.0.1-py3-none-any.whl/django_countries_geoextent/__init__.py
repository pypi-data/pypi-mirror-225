from django_countries_geoextent.countries import get_country_extent


def get_geo_extent(country) -> list:
    country_extent = get_country_extent(country.alpha3)
    return country_extent
