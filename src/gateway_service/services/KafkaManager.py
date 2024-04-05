import json
from inspect import iscoroutinefunction
from typing import Dict
from config import KAFKA_ID, KAFKA_SERVICE, KAFKA_GROUP_ID
from aiokafka import AIOKafkaConsumer


class KafkaManager():
    def __init__(self) -> None:
        self.callbacks = []

    def add_callback(self, callback):
        self.callbacks.append(callback)

    async def consume_async(self):
        consumer = AIOKafkaConsumer(
            KAFKA_ID,
            bootstrap_servers=KAFKA_SERVICE,
            group_id=KAFKA_GROUP_ID,
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
        await consumer.start()
        
        try:
            async for msg in consumer:
                data: Dict = msg.value
                print("CONSUME", data, flush=True)
                await self.__callback(data)
        finally:
            await consumer.stop()

    async def __callback(self, event):
        for callback in self.callbacks:
            if iscoroutinefunction(callback):
                await callback(event)
            else:
                callback(event)
