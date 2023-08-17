from confluent_kafka import Producer
import json


class ClientProducer:

    def __init__(self, bootstrap_servers: str, security_protocol: str='PLAINTEXT', sasl_username=None, sasl_password=None, sasl_mechanism: str='PLAIN'):
        """To validate and initialize the producer connection to kafka broker

        Args:
            bootstrap_servers (str): kafka broker url
            security_protocol (str, optional): security protocol while connecting to broker. Defaults to 'PLAINTEXT'.
            sasl_username (str, optional): username for accessing broker. Defaults to None.
            sasl_password (str, optional): password for accessing broker. Defaults to None.
            sasl_mechanism (str, optional): sasl mechanism to be followed. Defaults to 'PLAIN'.

        Raises:
            ValueError: If username for kafka broker is not provided
            ValueError: If password for kafka broker is not provided
        """
        KAFKA_PRODUCER_CONFIGURATION = {
            'bootstrap.servers': bootstrap_servers,
            'security.protocol' : security_protocol
        }
        if security_protocol == 'SASL_PLAINTEXT':
            if not sasl_username:
                raise ValueError('sasl_username can not be none !')
            if not sasl_password:
                raise ValueError('sasl_password can not be none !')
            KAFKA_PRODUCER_CONFIGURATION['sasl.username'] = sasl_username
            KAFKA_PRODUCER_CONFIGURATION['sasl.password'] = sasl_password
            KAFKA_PRODUCER_CONFIGURATION['sasl.mechanism'] = sasl_mechanism
        self.producer = Producer(KAFKA_PRODUCER_CONFIGURATION)
    
    def delivery_report(self, err, msg):
        """Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush().

        Args:
            err (_type_): callback error message if delivery fails.
            msg (_type_): callback msg which confirms data is sent to which topic, partition and offset.

        Raises:
            Exception: if message delivery fails.
        """
        if err is not None:
            print('Message delivery failed: {}'.format(err))
            raise Exception(err)
        else:
            print('Message delivered to {} partition [{}] offset [{}]'.format(msg.topic(), msg.partition(), msg.offset()))

    def produce_to_broker(self, data: dict, topics: list, key: str='key1'):
        """Method to send data to specific topic in kafka broker 

        Args:
            data (dict): data that has to be send
            topics (list[str]): list of topic where data is to be sent
            key (str, optional): which partition the data has to go. Defaults to 'key1'.
        """
        for _topic in topics:
            data = json.dumps(data)
            try:
                self.producer.produce(_topic, value=data, on_delivery=self.delivery_report)
                self.producer.poll(0)
            except BufferError as e:
                print("Buffer full, waiting for free space on the queue")
                self.producer.poll(5)
                self.producer.produce(_topic, value=data, on_delivery=self.delivery_report)
            self.producer.flush()