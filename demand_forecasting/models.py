from django.db import models

class ForecastingRequest(models.Model):
    csv_file = models.FileField(upload_to='csvs/')
    date_column = models.CharField(max_length=100)
    date_format = models.CharField(max_length=50)
    demand_column = models.CharField(max_length=100)
    forecast_days = models.IntegerField()
    train_test_split = models.FloatField()

    def __str__(self):
        return f"Forecasting Request {self.id}"