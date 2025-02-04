
import requests
from bs4 import BeautifulSoup
import pandas as pd
from confluent_kafka import Producer
import json

def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

def scrape_jobs():
    URL = "https://realpython.github.io/fake-jobs/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    job_elements = soup.find_all("div", class_="card-content")
   
    jobs = []
    for job in job_elements:
        title = job.find("h2").text.strip()
        company = job.find("h3").text.strip()
        location = job.find("p", class_="location").text.strip()
        jobs.append({"title": title, "company": company, "location": location})
   
    return jobs

def produce_messages(producer, topic, jobs):
    for job in jobs:
        key = job["title"]
        value = json.dumps(job)
        producer.produce(topic, key=key, value=value, callback=delivery_report)
   
    producer.flush()

def main_producer():
    producer_config = {
        'bootstrap.servers': 'localhost:9092',  # Remplacez par votre configuration Kafka
        'acks': 'all',
    }

    producer = Producer(producer_config)
    topic_name = 'jobs_topic'  # Remplacez par le nom du topic Kafka que vous utilisez

    jobs = scrape_jobs()
   
    try:
        produce_messages(producer, topic_name, jobs)
    except KeyboardInterrupt:
        pass
    finally:
        producer.flush()

if __name__ == "__main__":
    main_producer()