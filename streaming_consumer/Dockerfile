FROM bitnami/spark:3.3.1

WORKDIR /app

ENV TOPIC="message_data"

COPY data_consumer.py /app/data_consumer.py
COPY requirements.txt /app/requirements.txt

USER root 

# Install Python 3.11 and related tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.9 \
    python3.9-venv \
    python3.9-distutils \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["/opt/bitnami/spark/bin/spark-submit"]
CMD []

