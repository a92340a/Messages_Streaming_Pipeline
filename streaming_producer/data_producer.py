import os
import json
import gcsfs
import csv
import time
import logging
from typing import Optional
from confluent_kafka import Producer, Message


logging.basicConfig(level=logging.INFO)


BOOTSTRAP_SERVERS = os.getenv("BOOTSTRAP_SERVERS", "kafka-service:9092")
TOPIC = os.getenv("TOPIC", "message_data")
FILE_PATH = os.getenv("FILE_PATH")


def read_data(file_path: str):
    """
    Reads a CSV file from either local or GCS and yields each row as a dictionary.
    """
    if file_path.startswith("gs://"):
        fs = gcsfs.GCSFileSystem()
        with fs.open(file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            count = 0
            for row in reader:
                count += 1
                logging.info(f"count: {count}")
                time.sleep(1)
                yield row
    else:
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            count = 0
            for row in reader:
                count += 1
                logging.info(f"count: {count}")
                time.sleep(1)
                yield row


def delivery_report(err: Optional[Exception], msg: Message) -> None:
    """
    Called once for each message produced to indicate delivery result. Triggered by poll() or flush().
    """
    if err is not None:
        logging.error(f"Message delivery failed: {err}")
    else:
        logging.info(f"Message delivered to topic: {msg.topic()}, partition: {msg.partition()}, offset: {msg.offset()}")


def kafka_producer(bootstrap_servers: str, topic: str, file_path: str) -> None:
    """
    Converts each row from source data, and sends it as a message to a Kafka topic.

    Args:
        bootstrap_servers (str): Kafka broker addresses (e.g., "localhost:9092").
        topic (str): The Kafka topic to produce messages to.
        file_path (str): Path to the CSV file containing the data to be sent.

    Returns:
        None
    """
    producer = Producer({"bootstrap.servers": bootstrap_servers})

    try:
        for row in read_data(file_path):
            json_row = json.dumps(row)
            producer.produce(topic, value=json_row, callback=delivery_report)
            producer.flush()

    except KeyboardInterrupt:
        pass

    finally:
        producer.flush()


if __name__ == "__main__":
    if not FILE_PATH:
        logging.error("No configuration about source file path")
        exit(1)

    kafka_producer(BOOTSTRAP_SERVERS, TOPIC, FILE_PATH)
