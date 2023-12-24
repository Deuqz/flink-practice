import random

from kafka import KafkaConsumer
import time


def backoff(tries, sleep):
    def wrap(func):
        def wrapped_f(*args, **kwargs):
            for i in range(tries):
                try:
                    func(*args, **kwargs)
                    break
                except Exception as e:
                    print(f'Function call falls with {e}')
                    time.sleep(sleep)
        return wrapped_f
    return wrap


@backoff(tries=10, sleep=3)
def message_handler(value) -> None:
    if random.random() < 0.5:
        print(value)
    else:
        raise Exception('boom')


def create_consumer():
    print("Connecting to Kafka brokers")
    consumer = KafkaConsumer("hw_processed",
                             group_id="hw_processed_group1",
                             bootstrap_servers='localhost:29092',
                             auto_offset_reset='earliest',
                             enable_auto_commit=True)

    for message in consumer:
        #save to DB
        message_handler(message)


if __name__ == '__main__':
    create_consumer()
