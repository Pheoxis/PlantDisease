from google.cloud import storage
import tensorflow as tf
from PIL import Image
import numpy as np

Bucket_name = "tomato_disease_bucket"

Class_names = ["Tomato__Target_Spot", "Tomato__Tomato_mosaic_virus", "Tomato__Tomato_YellowLeaf__Curl_Virus","Tomato_Bacterial_spot",
                    "Tomato_Early_blight","Tomato_healthy","Tomato_Late_blight","Tomato_Leaf_Mold","Tomato_Septoria_leaf_spot"]

model = None

def download_blob(bucket_name, source_blob_name, destination, destination_file_name):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

def predict(request):
    global model 
    if model is not None:
        download_blob(
            Bucket_name,
            "Models/Disease_model.h5",
         "/trying/Disease_model.h5"
        )

        model = tf.keras.load_model("/trying/Disease_model.h5")
    
    image = request.filers["file"]

    image = np.array(Image.open(image).convert("RGB").resize((128,128)))
    image = image/127
    image_array = tf.expand_dims(image,0)


    predictions = model.predict(image_array)

    predictions = Class_names[np.argmax(predictions[0])]
    confidence = round(100 * (np.max(predictions[0]),2))

    return{
            'class' : predictions,
            'confidence': float(confidence)
        }