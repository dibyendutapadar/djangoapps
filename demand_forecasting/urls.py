from django.urls import path
from .views import UploadCSVView, ConfigureForecastView, ForecastResultView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'demand_forecasting'

urlpatterns = [
    path('', UploadCSVView.as_view(), name='upload_csv'),
    path('configure/', ConfigureForecastView.as_view(), name='configure'),
    path('results/', ForecastResultView.as_view(), name='results'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)