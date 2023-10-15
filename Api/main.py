from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
import asyncio



async def my_coroutine():
    app = FastAPI()

    Model = tf.keras.models.load_model(r"C:\Users\Kamil\Desktop\PROGRAMMING\Rok4\ASI\JupyterASI\PlantDisease\saved_models1")

    Class_names = ["Tomato_Bacterial_spot", "Tomato_Early_blight", "Tomato_Late_blight","Tomato_Leaf_Mold",
                    "Tomato_Septoria_leaf_spot","Tomato__Target_Spot","Tomato__Tomato_YellowLeaf__Curl_Virus","Tomato__Tomato_mosaic_virus","Tomato_healthy"]

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
        confidence = np.max(prediction[0])

        return {
            'class': predicted_class,
            'confidence': float(confidence)
        }

    if __name__ == "__main__":
        uvicorn.run(app, host='localhost', port=8000)


loop = asyncio.get_event_loop()
loop.run_until_complete(my_coroutine())