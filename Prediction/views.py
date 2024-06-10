# Prediction/views.py


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .utils import predict_crop, predict_disease
from .serializers import SensorDataSerializer, ImageUploadSerializer
from django.http import JsonResponse
from.utils import load_maize_model, predict_disease

import logging
logger = logging.getLogger(__name__)


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


# class ImageUploadView(APIView):
#     parser_classes = (MultiPartParser, FormParser)

#     def post(self, request):
#         serializer = ImageUploadSerializer(data=request.data)
#         if serializer.is_valid():
#             try:
#                 image = serializer.validated_data['image']
#             except KeyError:
#                 return Response({'error': 'Image field is required'}, status=400)
            
#             prediction = predict_disease(image.read())
#             return Response({'prediction': prediction.tolist()})  # Ensure the prediction is JSON serializable
#         return Response(serializer.errors, status=400)


class ImageUploadView(APIView):
    parser_classes = (JSONParser,)

    def post(self, request):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            try:
                image_url = serializer.validated_data['image_url']  # Extract the image URL
            except KeyError:
                return Response({'error': 'Image URL is required'}, status=400)
            
            # Load the maize model interpreter
            maize_interpreter = load_maize_model()
            
            # Call predict_disease and directly use its return value since it's a string
            prediction = predict_disease(image_url, maize_interpreter)
            return Response({'prediction': prediction})  # Directly return the prediction string
        return Response(serializer.errors, status=400)
    
     
    def upload_image(request):
        image_url = request.POST.get('image_url')
        try:
            maize_interpreter = load_maize_model()
            prediction = predict_disease(maize_interpreter, image_url)
            return JsonResponse({'prediction': prediction}, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


