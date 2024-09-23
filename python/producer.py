from confluent_kafka.admin import AdminClient
from confluent_kafka import Consumer, TopicPartition

# Kafka broker address
bootstrap_servers = "kafka:9092"

# Create Kafka AdminClient to list topics
admin_client = AdminClient({'bootstrap.servers': bootstrap_servers})

# Get cluster metadata
cluster_metadata = admin_client.list_topics(timeout=10)

# Total number of topics
total_topics = len(cluster_metadata.topics)
print(f"Total Topics: {total_topics}")

# Create a Consumer to query offsets
consumer = Consumer({
    'bootstrap.servers': bootstrap_servers,
    'group.id': 'my-group',
    'auto.offset.reset': 'earliest'
})

# Print topics and their partitions' message count
for topic in cluster_metadata.topics:
    partitions = cluster_metadata.topics[topic].partitions
    print(f"Topic: {topic}, Partitions: {len(partitions)}")

    # For each partition, fetch the beginning and end offsets
    for partition_id in partitions:
        tp = TopicPartition(topic, partition_id)
        low_offset, high_offset = consumer.get_watermark_offsets(tp)
        print(f"Partition {partition_id} -> Messages: {high_offset - low_offset}")

# Close the consumer when done
consumer.close()
