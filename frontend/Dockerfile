FROM python:3.10.12-alpine3.18

WORKDIR /app
COPY . .
COPY requirements.txt requirements.txt

RUN pip install --no-cache -r requirements.txt
CMD ["python3", "main.py"]