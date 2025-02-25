from confluent_kafka import Consumer, KafkaError
import logging
from config import BOOTSTRAP_SERVERS, TOPIC

logging.basicConfig(level=logging.INFO)


def consume_data(bootstrap_servers, topic):
    conf = {"bootstrap.servers": bootstrap_servers, "group.id": "ashraf-supply-chain", "auto.offset.reset": "earliest"}
    consumer = Consumer(conf)
    consumer.subscribe([topic])

    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition
                    continue
                else:
                    logging.error(msg.error())
                    break
            else:
                logging.info("Received message: {}".format(msg.value().decode("utf-8")))

    except KeyboardInterrupt:
        pass

    finally:
        consumer.close()


if __name__ == "__main__":
    bootstrap_servers = BOOTSTRAP_SERVERS
    topic = TOPIC

    consume_data(bootstrap_servers, topic)
