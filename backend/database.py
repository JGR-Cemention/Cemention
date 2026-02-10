import os
import certifi
from motor.motor_asyncio import AsyncIOMotorClient

# Read and sanitize env variables (VERY IMPORTANT)
MONGO_URL = os.environ.get("MONGO_URL", "").strip()
DB_NAME = os.environ.get("DB_NAME", "cemention").strip()

if not MONGO_URL:
    raise RuntimeError("❌ MONGO_URL is missing")

client = AsyncIOMotorClient(
    MONGO_URL,
    tls=True,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=30000,
    connectTimeoutMS=30000,
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
