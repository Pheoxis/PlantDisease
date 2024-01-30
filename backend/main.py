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

@app.get("/ping")
async def ping():
    return "Hello, I am alive"

@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    upload_folder = Path("uploaded_files")
    upload_folder.mkdir(parents=True, exist_ok=True)

    file_path = "uploaded_files/data.jpg"

    with open(file_path,"wb") as buffer:
        while True:
            data = await file.read(1024)
            if not data:
                break
            buffer.write(data)

    bootstrap_project(Path("/home/kedro"))
    with KedroSession.create() as session:
        context: KedroContext = session.load_context()
        result = session.run(pipeline_name="backend")
    varclass = result.get("formatted_prediction").get("class")
    confidence = result.get("formatted_prediction").get("confidence")
    filenamev = file.filename
    return {
        'filename': filenamev,
        'class': varclass,
        'confidence': confidence
    }


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)