A wrapper for kafka producer and consumer that can be used as decorator for a function which can keep consuming data, process this data and broadcast it to next topics/queues.

This uses [confluent-kafka](https://pypi.org/project/confluent-kafka/) python package to create prooducer, consumer and then wraps it. So, big thanks to them!

## Installation
```
$ pip install kafka-client-decorator
```

## Usage
Define your function how you want to process the data and then decorate it.
```
from kafka_client_decorator.kafka_client import KafkaClient

@KafkaClient(bootstrap_servers, security_protocol, sasl_username, sasl_password).consumer_producer(consumer_from_topic='my-topic-1', group_id='pdf', produce_to_topic=['my-topic-2'])
def process_data(data = None):
    # Call your driver modules here to process the data
    result = Driver(data)
    return result
```

> **_NOTE:_**  If you want the your driver result to be pushed to next topic/queue, you can simply pass produce_to_topic as arg in decorator 'consumer_prodcuer' method.

To only produce to topic(s) -
```
from kafka_client_decorator.client_producer import ClientProducer

producer = ClientProducer(bootstrap_servers, security_protocol, sasl_username, sasl_password)
prodcuer.produce_to_broker(data, topics_list)
```
> **_NOTE:_** If your kafka broker does not uses SASL or SSL protocol, no need to pass 'sasl_username' and 'sasl_password'.