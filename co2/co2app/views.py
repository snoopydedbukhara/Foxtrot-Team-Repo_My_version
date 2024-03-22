# views.py
from django.shortcuts import render
from co2app.models import CountryName, CO2Value


def main_page(request):
    return render(request, 'index.html')


def compare_countries(request):
    if request.method == 'POST':
        country1_code = request.POST.get('country1')
        country2_code = request.POST.get('country2')
        start_year = int(request.POST.get('start_year', 1990))  # Default to 1990 if not provided
        end_year = int(request.POST.get('end_year', 2020))  # Default to 2020 if not provided

        country1 = CountryName.objects.get(country_code=country1_code)
        country2 = CountryName.objects.get(country_code=country2_code)

        co2_data_country1 = CO2Value.objects.filter(country_code=country1, years__range=(start_year, end_year)).order_by('years').values_list('years', 'value')
        co2_data_country2 = CO2Value.objects.filter(country_code=country2, years__range=(start_year, end_year)).order_by('years').values_list('years', 'value')

        all_years = list(range(1990, 2021))  # Adjust this range as per your data

        return render(request, 'compare_countries.html', {
            'countries': CountryName.objects.all(),
            'country1_name': country1.country_name,
            'country2_name': country2.country_name,
            'co2_data_country1': co2_data_country1,
            'co2_data_country2': co2_data_country2,
            'all_years': all_years,
            'start_year': start_year,
            'end_year': end_year,
        })
    else:
        countries = CountryName.objects.all()
        all_years = list(range(1990, 2021))  # Adjust this range as per your data
        return render(request, 'compare_countries.html', {'countries': countries, 'all_years': all_years})


def show_on_map(request):
    # Add functionality to show countries on a map
    return render(request, 'show_on_map.html')
