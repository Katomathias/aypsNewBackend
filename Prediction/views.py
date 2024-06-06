# Prediction/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .utils import predict_crop, predict_disease
from .serializers import SensorDataSerializer, ImageUploadSerializer

# class SensorDataView(APIView):
#     def post(self, request):
#         serializer = SensorDataSerializer(data=request.data)
#         if serializer.is_valid():
#             npk_values = [
#                 serializer.validated_data['nitrogen'],
#                 serializer.validated_data['phosphorus'],
#                 serializer.validated_data['potassium'],
#                 serializer.validated_data['ph'],
#                 serializer.validated_data['electroconductivity'],
#                 serializer.validated_data['moisture']
#             ]
#             prediction = predict_crop(npk_values)
#             return Response({'prediction': prediction.tolist()})  # Ensure the prediction is JSON serializable
#         return Response(serializer.errors, status=400)


# class SensorDataView(APIView):
#     # parser_classes = (MultiPartParser, FormParser)
#     parser_classes = (JSONParser,)

#     def post(self, request):
#         serializer = SensorDataSerializer(data=request.data)
#         if serializer.is_valid():
#             npk_values = [
#                 serializer.validated_data['nitrogen'],
#                 serializer.validated_data['phosphorus'],
#                 serializer.validated_data['potassium'],
#                 serializer.validated_data['ph'],
#                 serializer.validated_data['electroconductivity'],
#                 serializer.validated_data['moisture']
#             ]
#             prediction = predict_crop(npk_values)
#             return Response({'prediction': prediction})  # Return crop prediction
#         return Response(serializer.errors, status=400)
class SensorDataView(APIView):
    parser_classes = (JSONParser,)

    def post(self, request):
        serializer = SensorDataSerializer(data=request.data)
        if serializer.is_valid():
            sensor_data = serializer.validated_data
            prediction = predict_crop(sensor_data)
            return Response({'prediction': prediction}, status=200)
        return Response(serializer.errors, status=400)

    def get(self, request):
        # Here you can implement logic to display captured data
        # For demonstration purposes, let's print prediction and sensor data
        prediction_message = "No prediction available"
        sensor_data_message = "No sensor data available"

        # Assuming you have stored sensor data in the request.session
        if 'sensor_data' in request.session:
            sensor_data = request.session['sensor_data']
            npk_values = [
                sensor_data['nitrogen'],
                sensor_data['phosphorus'],
                sensor_data['potassium'],
                sensor_data['ph'],
                sensor_data['electroconductivity'],
                sensor_data['moisture']
            ]
            prediction = predict_crop(npk_values)
            prediction_message = f"Prediction: {prediction}"
            sensor_data_message = f"Sensor Data: {sensor_data}"

        return Response({'prediction_message': prediction_message, 'sensor_data_message': sensor_data_message})


class ImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.validated_data['image']
            model_type = serializer.validated_data['model_type']
            prediction = predict_disease(image.temporary_file_path(), model_type)
            return Response({'prediction': prediction.tolist()})  # Ensure the prediction is JSON serializable
        return Response(serializer.errors, status=400)
