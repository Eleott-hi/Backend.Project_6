import httpx
from config import STORE_SERVICE


async def update_db_callback(message):
    async with httpx.AsyncClient() as client:
        product_id, price, available_stock = message["id"], message["price"], message["available_stock"]
        url = f"http://{STORE_SERVICE}/api/v1/products/{product_id}?price={price}&stock={available_stock}"

        response = await client.patch(url)
        print(response, flush=True)
