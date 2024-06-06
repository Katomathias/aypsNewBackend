import tensorflow as tf
import numpy as np
from PIL import Image

# Load TFLite models
maize_model_path = "Prediction/models/maizemodel.tflite"
maize_interpreter = tf.lite.Interpreter(model_path=maize_model_path)
maize_interpreter.allocate_tensors()

crop_model_path = "Prediction/models/crop_recommendation_model.tflite"
crop_interpreter = tf.lite.Interpreter(model_path=crop_model_path)           
crop_interpreter.allocate_tensors()


def preprocess_image(image_path, target_size=(256, 256)):
    # Open and resize the image
    image = Image.open(image_path).convert("RGB")  # Convert image to RGB mode
    image = image.resize(target_size)
    # Convert the image to numpy array, normalize, and reorder dimensions
    image = np.array(image, dtype=np.float32) / 255.0
    # Ensure the image has the correct shape
    image = np.transpose(image, (2, 0, 1))  # Reorder dimensions to match [channels, height, width]
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    return image


def predict_crop(sensor_data):                                               
    input_details = crop_interpreter.get_input_details()
    output_details = crop_interpreter.get_output_details()

    # Assuming your input tensor shape is [1, 6] based on the input_signature
    input_shape = input_details[0]['shape']
    
    # Initialize input_data
    input_data = np.array([
        sensor_data['nitrogen'],
        sensor_data['phosphorus'],
        sensor_data['potassium'],
        sensor_data['pH'],
        sensor_data['electroconductivity'],
        sensor_data['moisture']
    ], dtype=np.float32)

    # Check if the shape of input_data matches the expected input shape
    if input_data.shape != input_shape:
        raise ValueError("Input tensor shape doesn't match the expected shape.")

    # Reshape input_data if necessary
    input_data = input_data.reshape(input_shape)

    crop_interpreter.set_tensor(input_details[0]['index'], input_data)
    crop_interpreter.invoke()
    output_data = crop_interpreter.get_tensor(output_details[0]['index'])

    crop_index = np.argmax(output_data)
    crops = ["Cassava","Vanilla","Coffee","Cotton" ,"Tea","Tobacco","Groundnuts","Yams","Maize (corn)","Beans","Irish Potato","Matooke","Sweet Banana","Sugarcane"]
    return crops[crop_index]


def predict_disease(image_path, model_interpreter):
    input_data = preprocess_image(image_path)

    # Get input and output details
    input_details = model_interpreter.get_input_details()
    output_details = model_interpreter.get_output_details()

    # Set input tensor
    model_interpreter.set_tensor(input_details[0]['index'], input_data)
    # Run inference
    model_interpreter.invoke()
    # Get output tensor
    output_data = model_interpreter.get_tensor(output_details[0]['index'])

    # Post-process output and return prediction
    disease_index = np.argmax(output_data)
    diseases = ['Corn_(maize)___Common_rust_', 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___healthy', 'Corn_(maize)___Northern_Leaf_Blight']
    return diseases[disease_index]

# # Predict disease for maize
# image_path = "./models/download.png"
# maize_prediction = predict_disease(image_path, maize_interpreter)
# print("Maize disease prediction:", maize_prediction)

# # Predict crop
# sensor_data = {
#     'nitrogen': 130,
#     'phosphorus': 45,
#     'potassium': 120,
#     'pH': 5.7,
#     'electroconductivity': 1.1,
#     'moisture': 80
# }
# crop_prediction = predict_crop(sensor_data)
# print("Predicted crop:", crop_prediction)
