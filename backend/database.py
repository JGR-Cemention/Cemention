import os
import certifi
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.environ.get("MONGO_URL", "").strip()
DB_NAME = os.environ.get("DB_NAME", "cemention_db").strip()

client = None
db = None

if MONGO_URL:
    try:
        client = AsyncIOMotorClient(
            MONGO_URL,
            tls=True,
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=5000,
        )
        db = client[DB_NAME]
        print("⚠️ Mongo connected (but auth may still fail)")
    except Exception as e:
        print("❌ Mongo connection failed:", e)
else:
    print("⚠️ MONGO_URL not set")

# SAFE collections (won't crash)
users_collection = None
products_collection = None
addresses_collection = None
carts_collection = None
orders_collection = None
request_orders_collection = None
otp_collection = None
