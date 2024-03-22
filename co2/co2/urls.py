from django.urls import path
from co2app.views import main_page, compare_countries, show_on_map

urlpatterns = [
    path('', main_page, name='main_page'),
    path('compare/', compare_countries, name='compare_countries'),
    path('show_on_map/', show_on_map, name='show_on_map'),
]
