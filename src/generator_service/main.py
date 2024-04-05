
import asyncio
import json
import random
import httpx

from typing import Dict, List
from kafka import KafkaProducer
from config import KAFKA_MSG_TIMER_SEC, STORE_SERVICE, KAFKA_SERVICE, KAFKA_ID
from schemas import Product
from aiokafka import AIOKafkaProducer
from contextlib import suppress

# Инициализация Kafka Producer
producer = KafkaProducer(bootstrap_servers=KAFKA_SERVICE,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))


async def get_products() -> List[Product]:
    async with httpx.AsyncClient() as client:
        url = f'http://{STORE_SERVICE}/api/v1/products/'
        res = await client.get(url)

        res.raise_for_status()
        products = res.json()

        return products


async def generate_event():
    products: List[Dict] = await get_products()

    if products:
        product: dict = random.choice(products)
        product["price"] = round(random.uniform(0, 1000), 2)
        product["available_stock"] = random.randint(0, 100)
        return product


async def send_one_async(event):
    try:
        await producer.send_and_wait(KAFKA_ID, value=event)
    finally:
        await producer.stop()


async def main():

    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_SERVICE,
                                value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    await producer.start()

    try:
        while True:
            with suppress(Exception):
                if event := await generate_event():
                    print("SEND", event, flush=True)
                    await producer.send_and_wait(KAFKA_ID, value=event)

            await asyncio.sleep(KAFKA_MSG_TIMER_SEC)
    finally:
        await producer.stop()


if __name__ == "__main__":
    asyncio.run(main())
