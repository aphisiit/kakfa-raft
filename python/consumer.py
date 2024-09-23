from confluent_kafka import Consumer, TopicPartition
from confluent_kafka.admin import AdminClient

# Kafka broker address
bootstrap_servers = "kafka:9092"

# Create AdminClient to list topics
admin_client = AdminClient({'bootstrap.servers': bootstrap_servers})

# Create a Consumer to query offsets and get committed offsets (messages consumed)
consumer = Consumer({
    'bootstrap.servers': bootstrap_servers,
    'group.id': 'my-group',  # Replace with your actual consumer group ID
    'auto.offset.reset': 'earliest'
})

# Get cluster metadata
cluster_metadata = admin_client.list_topics(timeout=10)

# Total number of topics
total_topics = len(cluster_metadata.topics)
print(f"Total Topics: {total_topics}")

# Iterate over each topic
for topic in cluster_metadata.topics:
    partitions = cluster_metadata.topics[topic].partitions
    print(f"\nTopic: {topic}, Partitions: {len(partitions)}")
    
    for partition_id in partitions:
        tp = TopicPartition(topic, partition_id)

        # Get high watermark offset (latest message available)
        low_offset, high_offset = consumer.get_watermark_offsets(tp)

        # Get committed offset (messages consumed)
        committed_offsets = consumer.committed([tp])[0].offset

        # Calculate the lag (messages not yet consumed)
        if committed_offsets == -1001:
            committed_offsets = low_offset  # If no offset committed, assume the beginning

        messages_consumed = committed_offsets - low_offset
        messages_not_consumed = high_offset - committed_offsets

        print(f"Partition {partition_id}:")
        print(f"  Total messages: {high_offset - low_offset}")
        print(f"  Messages consumed: {messages_consumed}")
        print(f"  Messages not yet consumed (lag): {messages_not_consumed}")

# Close the consumer when done
consumer.close()
