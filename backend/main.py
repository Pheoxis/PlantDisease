from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Model = tf.keras.models.load_model("./Disease_model.h5")

CLASS_NAMES = ["Tomato_Bacterial_spot", "Tomato_Early_blight", "Tomato_Late_blight","Tomato_Leaf_Mold",                     
               "Tomato_Septoria_leaf_spot", "TomatoTarget_Spot", "TomatoTomato_YellowLeafCurl_Virus", "TomatoTomato_mosaic_virus", "Tomato_healthy"]


@app.get("/ping")
async def ping():
    return "Hello, I am alive"

def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image

@app.post("/predict")
async def predict(
    file: UploadFile = File(...)
):
    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, 0)

    prediction = Model.predict(img_batch)

    predicted_class = CLASS_NAMES[np.argmax(prediction[0])]
    confidence = np.max(prediction)

    return {
        "class": predicted_class.replace('_', ' '),
        "confidence": f'{round(float(confidence), 4) * 100}%'
    }

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)