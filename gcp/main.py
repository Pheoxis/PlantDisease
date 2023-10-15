from google.cloud import storage
import tensorflow as tf
from PIL import Image
import numpy as np

model = None
interpreter = None
input_index = None
output_index = None


Class_names = ["Tomato_Bacterial_spot", "Tomato_Early_blight", "Tomato_Late_blight","Tomato_Leaf_Mold",
                    "Tomato_Septoria_leaf_spot","Tomato__Target_Spot","Tomato__Tomato_YellowLeaf__Curl_Virus","Tomato__Tomato_mosaic_virus","Tomato_healthy"]

Bucket_name = "tomato_disease_bucket"


def download_blob(bucket_name, source_blob_name, destination_file_name):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)

def predict(request):
    global model 
    if model is None:
        download_blob(
            Bucket_name,
            "Models/Disease_model.h5",
            "/tmp/Disease_model.h5"
        )

        model = tf.keras.models.load_model("/tmp/Disease_model.h5",compile = False)
    
    image = request.files["file"]

    image = np.array(Image.open(image).convert("RGB"))#.resize((256,256))

    #image = image/255

    img_array = tf.expand_dims(image, 0)
    predictions = model.predict(img_array)

    predicted_class = Class_names[np.argmax(predictions[0])]
    confidence = round(100 * (np.max(predictions[0])),2)

    return{
            'class' : predicted_class,
            'confidence': float(confidence)
        }