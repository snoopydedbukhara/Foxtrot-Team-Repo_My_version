from django.db import models


class CountryName(models.Model):
    country_code = models.CharField(primary_key=True, max_length=5)
    country_name = models.CharField(max_length=200)

    def __str__(self):
        return self.country_name


class CO2Value(models.Model):
    country_code = models.ForeignKey(CountryName, on_delete=models.CASCADE)
    years = models.PositiveIntegerField()
    value = models.FloatField()

    def __str__(self):
        return f"{self.country_code} - {self.years}: {self.value}"

