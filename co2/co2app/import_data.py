import pandas as pd
from co2app.models import CountryName, CO2Value
from django.db import transaction


def clean_tables():
    with transaction.atomic():
        CO2Value.objects.all().delete()
        CountryName.objects.all().delete()


def import_country_data(file_path):
    df = pd.read_excel(file_path)
    for index, row in df.iterrows():
        country_code = row.pop('Country Code')  # Extract the value of 'Country Code' from the row
        if not CountryName.objects.filter(country_code=country_code).exists():
            CountryName.objects.create(
                country_code=country_code,
                country_name=row['Country Name']
            )


def import_co2_data(file_path):
    df = pd.read_excel(file_path)
    for index, row in df.iterrows():
        country_obj = CountryName.objects.get(country_code=row['Country Code'])
        for year in range(1990, 2021):
            value = row[str(year)]
            if pd.notna(value):
                CO2Value.objects.create(
                    country_code=country_obj,
                    years=year,
                    value=value
                )
