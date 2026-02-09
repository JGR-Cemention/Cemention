import os
import certifi
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.environ["MONGO_URL"]
DB_NAME = os.environ["DB_NAME"]

client = AsyncIOMotorClient(
    MONGO_URL,
    tls=True,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=30000,
    connectTimeoutMS=30000
)

db = client[DB_NAME]

# Collections
users_collection = db.users
products_collection = db.products
addresses_collection = db.addresses
carts_collection = db.carts
orders_collection = db.orders
request_orders_collection = db.request_orders
otp_collection = db.otps
