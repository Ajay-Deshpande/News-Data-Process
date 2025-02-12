from kafka.admin import KafkaAdminClient, NewTopic

def create_kafka_topic(bootstrap_servers, topic_name, num_partitions=1, replication_factor=1):
    try:
        admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
        existing_topics = admin_client.list_topics()

        if topic_name not in existing_topics:
            topic = NewTopic(name=topic_name, num_partitions=num_partitions, replication_factor=replication_factor)
            admin_client.create_topics([topic])
            print(f"Kafka topic '{topic_name}' created.")
        else:
            print(f"Kafka topic '{topic_name}' already exists.")

        admin_client.close()
    except Exception as e:
        print(f"Error creating Kafka topic: {e}")
