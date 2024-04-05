from dotenv import load_dotenv
import os

load_dotenv()

STORE_SERVICE = os.getenv("STORE_SERVICE")
KAFKA_SERVICE = os.getenv("KAFKA_SERVICE")
KAFKA_MSG_TIMER_SEC = int(os.getenv("KAFKA_MSG_TIMER_SEC"))
KAFKA_ID = os.getenv("KAFKA_ID")