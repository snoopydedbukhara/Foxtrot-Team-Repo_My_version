from django.core.management.base import BaseCommand
from co2app.import_data import import_country_data, import_co2_data, clean_tables

class Command(BaseCommand):
    help = 'Imports country and CO2 data from Excel files'

    def handle(self, *args, **kwargs):
        # Displaying success messages with paths
        self.stdout.write(self.style.SUCCESS(f'Importing country data...'))

        # Clean tables
        clean_tables()

        # Importing country data
        import_country_data('co2app/data/country_name.xls')

        # Success message
        self.stdout.write(self.style.SUCCESS('Country data imported successfully'))

        # Displaying success messages with paths
        self.stdout.write(self.style.SUCCESS(f'Importing CO2 data...'))

        # Importing CO2 data
        import_co2_data('co2app/data/value.xls')

        # Success message
        self.stdout.write(self.style.SUCCESS('CO2 data imported successfully'))
