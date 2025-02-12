import json
from gnews import GNews
from tqdm import tqdm
from kafka import KafkaProducer
from kafka_utils import create_kafka_topic
import os

# Kafka Configuration
KAFKA_BROKER = os.environ.get("KAFKA_BROKER", "kafka:9092")
TOPIC_NAME = os.environ.get("KAFKA_TOPIC", "crypto_news")

def get_kafka_producer():
    create_kafka_topic(KAFKA_BROKER, TOPIC_NAME)
    return KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

def main():
    try:
        producer = get_kafka_producer()
        print("PRODUCER TOPIC OBTAINED")
        news_reader = GNews(period = "1d", max_results = 100, exclude_websites = ['bloomberg.com'])
        gnews = news_reader.get_news('crypto')
        print("RECEIVED NEWS")
        for news in gnews:        
            producer.send(TOPIC_NAME, news)
            print(f"Published to Kafka: {news['title']}")
        producer.flush()
    except Exception as e:
        print("Main function didn't run due to: ", e)

if __name__ == "__main__":
    main()