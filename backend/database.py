import os
import certifi
from motor.motor_asyncio import AsyncIOMotorClient

# ==============================
# Read & sanitize environment variables
# ==============================
MONGO_URL = os.environ.get("MONGO_URL", "").strip()
DB_NAME = os.environ.get("DB_NAME", "cemention_db").strip()

client = None
db = None

# ==============================
# Initialize MongoDB client safely
# ==============================
if MONGO_URL:
    try:
        client = AsyncIOMotorClient(
            MONGO_URL,
            tls=True,
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=30000,
            connectTimeoutMS=30000,
        )
        db = client[DB_NAME]
        print("✅ MongoDB client initialized")
    except Exception as e:
        print("❌ MongoDB initialization failed:", e)
else:
    print("⚠️ WARNING: MONGO_URL not set. Database disabled.")

# ==============================
# Collections (safe even if db is None)
# ==============================
users_collection = db.users if db else None
products_collection = db.products if db else None
addresses_collection = db.addresses if db else None
carts_collection = db.carts if db else None
orders_collection = db.orders if db else None
request_orders_collection = db.request_orders if db else None
otp_collection = db.otps if db else None
