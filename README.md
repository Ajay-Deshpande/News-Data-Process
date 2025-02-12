# 🚀 Crypto News Processing Pipeline

A **real-time data pipeline** that scrapes crypto news articles, processes them using **LLMs (NER, Sentiment Analysis, Summarization)**, and stores the results in **MongoDB**, with **Kafka** as the messaging backbone.

---

## 📌 Features
- ✅ **Real-time Crypto News Scraping** using **Selenium & GNews**
- ✅ **Kafka-Based Streaming Pipeline**
- ✅ **LLM-Powered Processing**
  - **NER (Named Entity Recognition)**: Extracts key entities from articles
  - **Sentiment Analysis**: Determines the sentiment of each article
  - **Summarization**: Generates concise summaries
- ✅ **Storage in MongoDB**

---

## 📦 Project Architecture
```
+----------------+        +----------------+        +----------------+
|  Python Producer | ---> |  Kafka Broker  | ---> |  Python Consumer  |
| (Scrapes News)   |      | (Message Queue) |      | (LLM Processing)  |
+----------------+        +----------------+        +----------------+
                                                   ⬇   
                                             +----------------+
                                             |   MongoDB DB   |
                                             | (Stores Results) |
                                             +----------------+
```

🛠️ Tech Stack
Python
Selenium, GNews (for web scraping)
Kafka (message broker)
MongoDB (database)
Transformers Library (pipeline)
NER Model: covalenthq/cryptoNER
Sentiment Model: ElKulako/cryptobert
Summarization Model: Seq2Seq

```
├── producer/
│   ├── producer.py      # Scrapes news and sends to Kafka
│   ├── requirements.txt
│   ├── Dockerfile
│
├── consumer/
│   ├── consumer.py      # Reads Kafka messages, processes news, stores in MongoDB
│   ├── kafka_utils.py   # Kafka topic creation utilities
│   ├── requirements.txt
│   ├── Dockerfile
│
├── docker-compose.yml   # Containerizes the entire pipeline
└── README.md
```

🚀 Getting Started
1️⃣ Clone the Repository

```
git clone https://github.com/yourusername/crypto-news-pipeline.git
cd crypto-news-pipeline
```

2️⃣ Build & Start Services with Docker
```docker-compose up --build```


🔍 How It Works
- Python Producer (producer/producer.py)
  - Scrapes crypto news using GNews and Selenium
  - Extracts full article text
  - Publishes data to Kafka topic crypto_news
- Python Consumer (consumer/consumer.py)
  - Reads messages from Kafka
  - Processes each article with LLMs:
    - NER: Extracts crypto-related entities
    - Sentiment Classification: Determines sentiment
    - Summarization: Generates a short summary
  - Stores results in MongoDB

📌 Kafka Setup & Topic Management
Creating Kafka Topic Manually
```
docker exec -it kafka kafka-topics.sh --create --topic crypto_news --bootstrap-server kafka:9092 --partitions 1 --replication-factor 1
```

List Topics
```
docker exec -it kafka kafka-topics.sh --list --bootstrap-server kafka:9092
```


🐞 Troubleshooting
Kafka Producer Fails to Connect?
- Run docker-compose logs kafka to check if Kafka is running
- Restart the services:
```
docker-compose down && docker-compose up --build
```
