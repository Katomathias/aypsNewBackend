# Prediction/urls.py
from django.urls import path
from .views import SensorDataView, ImageUploadView

urlpatterns = [
    path('api/sensor-data/', SensorDataView.as_view(), name='sensor-data'),
    path('api/upload-image/', ImageUploadView.as_view(), name='upload-image'),
]
