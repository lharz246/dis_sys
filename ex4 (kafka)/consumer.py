from kafka import KafkaConsumer
import json

consumer = KafkaConsumer('test-topic',
                         bootstrap_servers=['localhost:29092'],
                         auto_offset_reset='earliest',
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))

for message in consumer:
    print(f"Received: {message.value}")