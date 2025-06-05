from aiokafka import AIOKafkaProducer


class KafkaHelper:
    def __init__(self):
        self.producer: AIOKafkaProducer = None

    async def connect(self):
        self.producer = AIOKafkaProducer(bootstrap_servers="kafka:9092")
        await self.producer.start()

    async def disconnect(self):
        await self.producer.stop()

    def get_kafka_producer(self):
        return self.producer


kafka_helper = KafkaHelper()
