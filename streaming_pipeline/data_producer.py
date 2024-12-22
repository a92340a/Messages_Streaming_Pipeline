import time
import json
import csv
import logging
from typing import Optional
from confluent_kafka import Producer, Message
from config import BOOTSTRAP_SERVERS, TOPIC

logging.basicConfig(level=logging.INFO)


def read_data(file_path: str):
    """
    Reads a CSV file and yields each row as a dictionary.

    Args:
        file_path (str): The path to the CSV file.

    Yields:
        Dict[str, str]: A dictionary representing a row of the CSV file,
            where the keys are column headers and the values are strings.
    """
    count = 0
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
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
    bootstrap_servers = BOOTSTRAP_SERVERS
    topic = TOPIC
    file_path = "./data/messages.csv"

    kafka_producer(bootstrap_servers, topic, file_path)
