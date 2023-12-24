#!/bin/bash

docker compose up -d
docker compose exec kafka kafka-topics.sh --bootstrap-server kafka:9092 --create --topic hw --partitions 1 --replication-factor 1
docker compose exec jobmanager ./bin/flink run -py /opt/pyflink/tumbling.py -d
python3 producer_1.py
python3 consumer_1.py
