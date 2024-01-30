import os
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from kedro.framework.session import KedroSession
from kedro.framework.startup import bootstrap_project
from kedro.io import DataCatalog
from pathlib import Path
import uvicorn
import time
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from PIL import Image
import tensorflow as tf
from io import BytesIO
import os

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
model_path = os.path.join("Disease_model.h5")
Model = tf.keras.models.load_model(model_path)
Class_names = ["Tomato_Bacterial_spot", "Tomato_Early_blight", "Tomato_Late_blight","Tomato_Leaf_Mold",
                "Tomato_Septoria_leaf_spot","Tomato__Target_Spot","Tomato__Tomato_YellowLeaf__Curl_Virus","Tomato__Tomato_mosaic_virus","Tomato_healthy"]
@app.get("/ping")
async def ping():
    return "Hello, I am alive"
def read_file_as_image(data) -> np.ndarray:
    image = Image.open(BytesIO(data))
    image = image.convert('RGB')
    image = image.resize((256, 256))
    image = np.array(image)
    return image
@app.post("/predict")
async def predict(file: UploadFile = File(...)):



    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, 0)
    prediction = Model.predict(img_batch)
    predicted_class = Class_names[np.argmax(prediction[0])]
    confidence = np.max(prediction[0])
    print(prediction, predicted_class, confidence)
    return {
        'filename': file.filename,
        'class': predicted_class,
        'confidence': float(confidence)
    }

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)

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