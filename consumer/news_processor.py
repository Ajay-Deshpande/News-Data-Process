import os
import json
from kafka import KafkaConsumer
from pymongo import MongoClient

from transformers import pipeline

def get_entity_list(news, NER):
    prev_end = -1
    lst = []
    for i in NER(news):
        if i['start'] == prev_end and i['entity'].startswith('I'):
            lst[-1] += i['word']
        else:
            lst.append(i['word'])
            prev_end = i['end']
    return lst

# Kafka Configuration
KAFKA_BROKER = os.environ.get("KAFKA_BROKER", "kafka:9092")
TOPIC_NAME = os.environ.get("KAFKA_TOPIC", "crypto_news")

# MongoDB Configuration
MONGO_URI = os.environ.get("CONNECTION_URL", "mongodb://mongodb:27017/")
DB_NAME = os.environ.get("DATABASE_NAME", "news_db")
COLLECTION_NAME = os.environ.get("COLLECTION_NAME", "crypto_articles")
NER = pipeline("token-classification", model="covalenthq/cryptoNER")
SENTIMENT = pipeline("text-classification", model="ElKulako/cryptobert",
                        max_length=64, truncation=True, padding = 'max_length')
SUMMARIZE = pipeline("summarization")

def get_mongo_client():
    """Initialize and return a MongoDB client."""
    client = MongoClient(MONGO_URI)
    return client[DB_NAME][COLLECTION_NAME]

def get_kafka_consumer():
    """Initialize and return a Kafka consumer."""
    return KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=KAFKA_BROKER,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        auto_offset_reset="earliest",
        group_id="crypto_news_group"
    )

def main():
    """Consume messages from Kafka and store them in MongoDB."""
    consumer = get_kafka_consumer()
    collection = get_mongo_client()

    print("Listening for messages on Kafka topic:", TOPIC_NAME)

    for message in consumer:
        news = message.value
        news['entity'] = get_entity_list(news['title'], NER)
        news['sentiment'] = SENTIMENT(news['title'])
        news['summary'] = SUMMARIZE(news['title'])
        try:
            collection.insert_one(news)
            print(f"Inserted article: {news.get('title', 'No Title')}")
        except Exception as e:
            print(f"Failed to insert article: {e}")

if __name__ == "__main__":
    main()
