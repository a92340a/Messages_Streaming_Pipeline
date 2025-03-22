FROM python:3.11-slim

WORKDIR /app

ENV TOPIC="message_data"

COPY data_producer.py /app/data_producer.py
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "data_producer.py"]
