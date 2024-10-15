
## Requirements

- Docker and Docker Compose
- Python 3.11 or newer

## Setup

1. Start Kafka and Zookeeper:
   ```
   docker-compose up -d
   ```

2. Use the Python virtual environment:
   ```
   source venv/bin/activate
   ```

## How to Use

1. Create a Kafka topic:
   ```
   docker-compose exec kafka kafka-topics --create --topic test-topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
   ```

2. Run the producer:
   ```
   python producer.py
   ```

3. In a new terminal, run the consumer:
   ```
   source venv/bin/activate
   python consumer.py
   ```


