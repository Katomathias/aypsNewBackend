import tensorflow as tf
import numpy as np
from PIL import Image

# Load your TensorFlow Lite model
tomato_model_path = "./models/tomatomodel.tflite"
tomato_interpreter = tf.lite.Interpreter(model_path=tomato_model_path)
tomato_interpreter.allocate_tensors()

maize_model_path = "./models/maizemodel.tflite"
maize_interpreter = tf.lite.Interpreter(model_path=maize_model_path)
maize_interpreter.allocate_tensors()
# Function to preprocess the input image
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




# Function to perform inference
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
    diseases = ['Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus', 'Tomato___Late_blight', 'Tomato___Septoria_leaf_spot', 'Tomato___Target_Spot', 'Tomato___Early_blight', 'Tomato___healthy', 'Tomato___Bacterial_spot', 'Tomato___Leaf_Mold', 'Tomato___Spider_mites Two-spotted_spider_mite','Corn_(maize)___Common_rust_', 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___healthy', 'Corn_(maize)___Northern_Leaf_Blight']
    return diseases[disease_index]



# def predict_disease(image_path, model_interpreter):
#     input_data = preprocess_image(image_path)

#     # Get input and output details
#     input_details = model_interpreter.get_input_details()
#     output_details = model_interpreter.get_output_details()

#     print("Expected input shape:", input_details[0]['shape'])
#     print("Actual input shape:", input_data.shape)

#     # Set input tensor
#     model_interpreter.set_tensor(input_details[0]['index'], input_data)
#     # Run inference
#     model_interpreter.invoke()
#     # Get output tensor
#     output_data = model_interpreter.get_tensor(output_details[0]['index'])

#     # Post-process output and return prediction
#     disease_index = np.argmax(output_data)
#     diseases = ['Corn_(maize)___Common_rust_', 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___healthy', 'Corn_(maize)___Northern_Leaf_Blight']
#     return diseases[disease_index]

# Example usage:
image_path = "./models/tomato.png"
tomato_prediction = predict_disease(image_path, tomato_interpreter)
print("Tomato disease prediction:", tomato_prediction)
# image_path = "./models/download.png"
# input_data = preprocess_image(image_path)
# print("Preprocessed image shape:", input_data.shape)