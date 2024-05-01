import os


DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_NAME = os.getenv("DB_NAME")
DB_DRIVER = os.getenv("DB_DRIVER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_URL = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

AUTH_SERVICE = os.getenv("AUTH_SERVICE")
REDIS_SERVICE = os.getenv("REDIS_SERVICE")

IMAGE_SERVICE = os.getenv("IMAGE_SERVICE")
IMAGE_SERVICE_API = os.getenv("IMAGE_SERVICE_API")