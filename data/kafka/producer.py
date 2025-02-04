from confluent_kafka import Producer
import time

def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

def produce_messages(producer, topic, num_messages=10):
    for i in range(num_messages):
        key = 'key{}'.format(i)
        value = 'message{}'.format(i)
        producer.produce(topic, key=key, value=value, callback=delivery_report)

    producer.flush()

def main_producer():
    # Configuration du producteur
    producer_config = {
        'bootstrap.servers': 'localhost:9092',  # Remplacez par votre configuration Kafka
        'acks': 'all',
    }

    producer = Producer(producer_config)
    topic_name = 'example_topic'  # Remplacez par le nom du topic Kafka que vous utilisez

    try:
        produce_messages(producer, topic_name)
    except KeyboardInterrupt:
        pass
    finally:
        producer.flush()
        producer.close()

if __name__ == "__main__":
    main_producer()