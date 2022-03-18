from django.db import models

# Create your models here.
class Output(models.Model):
    geographical_description = models.TextField()
    geographical_level = models.CharField(max_length=7)
    ons_code = models.CharField(max_length = 10)
    measure_group_description = models.TextField()
    disaggregation_level = models.TextField()
    measure_value = models.FloatField()
    imd_average_rank = models.FloatField(null=True)
    annual_pay_mean = models.IntegerField(null=True)
    population = models.IntegerField(null=True)
    year = models.IntegerField(default=2021)

    def __str__(self):
        return f'Geographical Description: {self.geographical_description}, Geographical Level: {self.geographical_level}, ONS Code: {self.ons_code}, Measure Group Description: {self.measure_group_description}, Disaggregation Level: {self.disaggregation_level}, Measure Value: {self.measure_value}, IMD Average Rank: {self.imd_average_rank}, Annual Pay Mean: {self.imd_average_rank}, Population: {self.population}'