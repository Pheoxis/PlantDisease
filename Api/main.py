from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from PIL import Image
import tensorflow as tf
from io import BytesIO
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
model_path = os.path.join("saved_models1", "1")
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
async def predict(
        file: UploadFile = File(...)
):
    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, 0)
    prediction = Model.predict(img_batch)
    predicted_class = Class_names[np.argmax(prediction[0])]
    confidence = np.max(prediction[0])
    return {
        'filename': file.filename,
        'class': predicted_class,
        'confidence': float(confidence)
    }
if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)