# from rest_framework import serializers
# from .models import SensorData, CropPredictionResult, ImageUpload, DiseasePredictionResult

# class SensorDataSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SensorData
#         fields = '__all__'

# class CropPredictionResultSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CropPredictionResult
#         fields = '__all__'

# class ImageUploadSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ImageUpload
#         fields = '__all__'

# class DiseasePredictionResultSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DiseasePredictionResult
#         fields = '__all__'


from rest_framework import serializers
from .models import SensorData, CropPredictionResult, ImageUpload, DiseasePredictionResult

class SensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorData
        fields = '__all__'

class CropPredictionResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = CropPredictionResult
        fields = '__all__'

class ImageUploadSerializer(serializers.Serializer):
    image_url = serializers.URLField()


class DiseasePredictionResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiseasePredictionResult
        fields = '__all__'
