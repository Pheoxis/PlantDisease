FROM tensorflow/tensorflow:2.14.0-jupyter

WORKDIR /app
COPY . .

RUN pip install --no-cache -r Api/requirements.txt
CMD ["python3", "Api/main-tf-serving.py"]
