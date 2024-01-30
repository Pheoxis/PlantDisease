from PIL import Image
import numpy as np
from io import BytesIO
import tensorflow as tf

def parse_image_data(image_data):
    image_array = np.array(image_data)
    return image_array

def preprocess_image(image_array):
    if image_array.shape[:2] != (256, 256):
        image_array = np.array(Image.fromarray(image_array).resize((256, 256)))

    if len(image_array.shape) == 2:
        image_array = cv2.cvtColor(image_array, cv2.COLOR_GRAY2RGB)

    elif image_array.shape[2] == 4:
        image_array = cv2.cvtColor(image_array, cv2.COLOR_BGRA2RGB)

    assert image_array.shape == (256, 256, 3)

    processed_image = np.reshape(image_array, (256, 256, 3))

    return processed_image

def model_prediction(processed_image):

    model = tf.keras.models.load_model("/home/kedro/Disease_model.h5")
    prediction = model.predict(np.expand_dims(processed_image, axis=0))
    return prediction

def format_prediction(prediction):

    predicted_index = np.argmax(prediction)
    class_names = ["Tomato_Bacterial_spot", "Tomato_Early_blight", "Tomato_Late_blight","Tomato_Leaf_Mold","Tomato_Septoria_leaf_spot", "TomatoTarget_Spot", "TomatoTomato_YellowLeafCurl_Virus", "TomatoTomato_mosaic_virus", "Tomato_healthy"]
    predicted_class = class_names[predicted_index]
    confidence = np.max(prediction)
    print({
        "class": predicted_class.replace('', ' '),
        "confidence": f'{round(float(confidence), 4) * 100}%'
    }   )

    return {
        "class": predicted_class.replace('', ' '),
        "confidence": f'{round(float(confidence), 4) * 100}%'
    }

 
def resize_image(image, size):
    return np.resize(image, size)

