from django.db import models

class SensorData(models.Model):
    nitrogen = models.FloatField()
    phosphorus = models.FloatField()
    potassium = models.FloatField()
    pH = models.FloatField()
    electroconductivity = models.FloatField()
    moisture = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

class CropPredictionResult(models.Model):
    crop = models.CharField(max_length=100)
    sensor_data = models.ForeignKey(SensorData, on_delete=models.CASCADE)
    predicted_at = models.DateTimeField(auto_now_add=True)

class ImageUpload(models.Model):
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class DiseasePredictionResult(models.Model):
    disease = models.CharField(max_length=100)
    image = models.ForeignKey(ImageUpload, on_delete=models.CASCADE)
    predicted_at = models.DateTimeField(auto_now_add=True)
