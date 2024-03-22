# views.py
from django.shortcuts import render
from co2app.models import CountryName, CO2Value
import plotly.graph_objs as go


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

        # Generate the graph HTML
        graph_html = generate_graph(co2_data_country1, co2_data_country2, country1.country_name, country2.country_name)

        return render(request, 'compare_countries.html', {
            'countries': CountryName.objects.all(),
            'country1_name': country1.country_name,
            'country2_name': country2.country_name,
            'co2_data_country1': co2_data_country1,
            'co2_data_country2': co2_data_country2,
            'all_years': all_years,
            'start_year': start_year,
            'end_year': end_year,
            'graph_html': graph_html  # Pass the graph HTML to the template
        })
    else:
        countries = CountryName.objects.all()
        all_years = list(range(1990, 2021))  # Adjust this range as per your data
        return render(request, 'compare_countries.html', {'countries': countries, 'all_years': all_years})


def show_on_map(request):
    # Add functionality to show countries on a map
    return render(request, 'show_on_map.html')


def generate_graph(data_country1, data_country2, country1_name, country2_name):
    try:
        years_country1 = [row[0] for row in data_country1]  # Extract years for country 1
        values_country1 = [row[1] for row in data_country1]  # Extract values for country 1

        years_country2 = [row[0] for row in data_country2]  # Extract years for country 2
        values_country2 = [row[1] for row in data_country2]  # Extract values for country 2

        # Create traces for country 1 and country 2
        trace_country1 = go.Scatter(x=years_country1, y=values_country1, mode='lines+markers', name=country1_name)
        trace_country2 = go.Scatter(x=years_country2, y=values_country2, mode='lines+markers', name=country2_name)

        # Set layout for the graph
        layout = go.Layout(title='CO2 Values Comparison',
                           xaxis=dict(title='Year'),
                           yaxis=dict(title='CO2 Value'))

        fig = go.Figure(data=[trace_country1, trace_country2], layout=layout)  # Create figure object
        return fig.to_html(full_html=False)  # Return HTML representation of the graph

    except Exception as e:  # Catch any exceptions
        return f"Error generating graph: {e}"  # Return error message if graph generation fails
