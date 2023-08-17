from confluent_kafka import Consumer, KafkaError, KafkaException
from .client_producer import ClientProducer
import functools
import json


class KafkaClient():
    
    def __init__(self, bootstrap_servers: str, security_protocol: str='PLAINTEXT', sasl_username: str=None, sasl_password: str=None, sasl_mechanism: str='PLAIN', max_poll_interval_ms: int=300000):
        """To validate and initialize the kafka client

        Args:
            bootstrap_servers (str): kafka broker url
            security_protocol (str, optional): security protocol while connecting to broker. Defaults to 'PLAINTEXT'.
            sasl_username (str, optional): username for accessing broker. Defaults to None.
            sasl_password (str, optional): password for accessing broker. Defaults to None.
            sasl_mechanism (str, optional): sasl mechanism to be followed. Defaults to 'PLAIN'.
            max_poll_interval_ms (int, optional): custom max.poll.interval.ms for consumer. Defaults to 300000 ms.

        Raises:
            ValueError: If username for kafka broker is not provided
            ValueError: If password for kafka broker is not provided
        """
        self.bootstrap_servers = bootstrap_servers
        self.security_protocol = security_protocol
        self.sasl_username = sasl_username
        self.sasl_password = sasl_password
        self.sasl_mechanism = sasl_mechanism
        self.max_poll_interval_ms = max_poll_interval_ms
        if security_protocol == 'SASL_PLAINTEXT':
            if not sasl_username:
                raise ValueError('sasl_username can not be none !')
            if not sasl_password:
                raise ValueError('sasl_password can not be none !')
    
    def get_kafka_consumer_config(self, group_id: str) -> dict:
        """Creates the custom consumer configuration based on security protocol provided

        Args:
            group_id (str): determines which consumers belong to which group. If there are four consumers with the same Group ID assigned to the same topic, they will all share the work of reading from the same topic.

        Returns:
            dict: consumer configuration which kafka broker will follow
        """
        config = {
            'bootstrap.servers': self.bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': False,
            'security.protocol' : self.security_protocol,
            'max.poll.interval.ms': self.max_poll_interval_ms
        }
        if self.security_protocol == 'SASL_PLAINTEXT':
            config['sasl.username'] = self.sasl_username
            config['sasl.password'] = self.sasl_password
            config['sasl.mechanism'] = self.sasl_mechanism
        return config

    def producer_conn(self, produce_to_topic: list=None):
        """Creates the consumer connection to kafka broker

        Args:
            produce_to_topic (list[str], optional): Topics to which data will be queued. Defaults to None.

        Returns:
            producer_object: This object provides all producer methods to interact with broker.
        """
        if produce_to_topic and len(produce_to_topic)>0:
            producer = ClientProducer(self.bootstrap_servers, self.security_protocol, self.sasl_username, self.sasl_password, self.sasl_mechanism)
            return producer
        else:
            return None

    def consumer_producer(self, _func=None, *, consumer_from_topic: str, group_id: str, produce_to_topic: list=None):
        """A method that can be used as decorator to keep consuming data from topics, process this data as per your func and alternatively broadcast the func result to next topic(s)

        Args:
            consumer_from_topic (str): from which topic to consume.
            group_id (str): determines which consumers belong to which group. If there are four consumers with the same Group ID assigned to the same topic, they will all share the work of reading from the same topic.
            _func (_type_, optional): _description_. Defaults to None.
            produce_to_topic (list[str], optional): broadcast the results to topic(s). Defaults to None.

        Raises:
            KafkaError: if consumer is not able to get data from broker in case kafka is not available.

        Returns:
            _type_: _description_
        """
        producer = self.producer_conn(produce_to_topic)
        KAFKA_CONSUMER_CONFIGURATION = self.get_kafka_consumer_config(group_id)
        def decorator_consumer(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                consumer = Consumer(KAFKA_CONSUMER_CONFIGURATION)
                try:
                    consumer.subscribe([consumer_from_topic])
                    while True:
                        msg = consumer.poll(2)
                        if msg is None:
                            continue
                        if msg.error():
                            if msg.error().code() == KafkaError._PARTITION_EOF:
                                continue
                            else:
                                print(msg.error())
                                raise KafkaError(msg.error())
                        else:
                            print('Message received from {} partition [{}] offset [{}]'.format(msg.topic(), msg.partition(), msg.offset()))
                            data = json.loads(msg.value())
                            print('consumer', data)
                            result = func(data)
                            print(result)
                            if producer:
                                producer.produce_to_broker(result, produce_to_topic)
                            consumer.commit(asynchronous=False)
                finally:
                    consumer.close()
            return wrapper
        
        if _func is None:
            return decorator_consumer
        return decorator_consumer(_func)
