# Django Countries GeoExtent

This package adds a `geo_extent` attribute to
the `django-countries` [Country](https://github.com/SmileyChris/django-countries#the-country-object) object.

The `geo_extent` attribute represents the geographic extent of a country, as extracted
from [GADM 4.1](https://gadm.org/download_world.html) boundaries data.

## Installation

```
pip install django-countries-geoextent
```

## Usage

Once installed, use the [Django Country](https://github.com/SmileyChris/django-countries#the-country-object) as
described in the [docs](https://github.com/SmileyChris/django-countries).

A new attribute named `geo_extent` will be added to a Country object instance, that represents the geographic extent of
the country, as obtained from [GADM 4.1](https://gadm.org/download_world.html) boundaries data.

If a country is not found, the `geo_extent` attribute will be `None`