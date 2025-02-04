from confluent_kafka import Consumer, KafkaError

def consume_messages(consumer, topic):
    consumer.subscribe([topic])

    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break

            print('Received message: key={}, value={}'.format(msg.key(), msg.value()))

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

def main_consumer():
    # Configuration du consommateur
    consumer_config = {
        'bootstrap.servers': 'localhost:9092',  # Remplacez par votre configuration Kafka
        'group.id': 'example_group',
        'auto.offset.reset': 'earliest',
    }

    consumer = Consumer(consumer_config)
    topic_name = 'example_topic'  # Remplacez par le nom du topic Kafka que vous utilisez

    try:
        consume_messages(consumer, topic_name)
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

if __name__ == "__main__":
    main_consumer()