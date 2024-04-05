
import asyncio
from collections import deque
import json
from typing import Deque
from singleton_decorator import singleton


@singleton
class SSEManager():

    def __init__(self):
        self.data = (
            "event: product_update\n"
            f"data: None\n\n"
        )

    def update_data(self, data):
        self.data = (
            "event: product_update\n"
            f"data: {json.dumps(data)}\n\n"
        )

    async def streaming(self):
        while True:
            yield self.data
            await asyncio.sleep(0.1)
