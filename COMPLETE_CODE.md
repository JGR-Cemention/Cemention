# CEMENTION - Complete Code Reference

## Table of Contents
1. [Backend Files](#backend-files)
2. [Frontend Files](#frontend-files)
3. [Configuration Files](#configuration-files)
4. [Setup Instructions](#setup-instructions)

---

## Backend Files

### 1. `/app/backend/.env`
```env
MONGO_URL="mongodb://localhost:27017"
DB_NAME="cemention_db"
CORS_ORIGINS="*"
JWT_SECRET_KEY="cemention-jwt-secret-key-change-in-production"
TWILIO_ACCOUNT_SID=""
TWILIO_AUTH_TOKEN=""
TWILIO_PHONE_NUMBER=""
OTP_DEMO_MODE="true"
```

### 2. `/app/backend/requirements.txt`
```txt
fastapi==0.110.1
uvicorn==0.25.0
boto3>=1.34.129
requests-oauthlib>=2.0.0
cryptography>=42.0.8
python-dotenv>=1.0.1
pymongo==4.5.0
pydantic>=2.6.4
email-validator>=2.2.0
pyjwt>=2.10.1
bcrypt==4.1.3
passlib>=1.7.4
tzdata>=2024.2
motor==3.3.1
pytest>=8.0.0
black>=24.1.1
isort>=5.13.2
flake8>=7.0.0
mypy>=1.8.0
python-jose>=3.3.0
requests>=2.31.0
pandas>=2.2.0
numpy>=1.26.0
python-multipart>=0.0.9
jq>=1.6.0
typer>=0.9.0
emergentintegrations==0.1.0
twilio
reportlab
PyPDF2
```

### 3. `/app/backend/models.py`
```python
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List
from datetime import datetime, timezone
from enum import Enum
import uuid

# Enums
class UserRole(str, Enum):
    DEALER = "DEALER"
    RETAILER = "RETAILER"
    CUSTOMER = "CUSTOMER"
    ADMIN = "ADMIN"

class UserStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class PaymentMethod(str, Enum):
    UPI = "UPI"
    CARD = "CARD"
    NETBANKING = "NETBANKING"
    BANK_TRANSFER = "BANK_TRANSFER"
    COD = "COD"

class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    RECEIVED = "RECEIVED"
    FAILED = "FAILED"

class OrderStatus(str, Enum):
    PENDING = "PENDING"
    PAYMENT_RECEIVED = "PAYMENT_RECEIVED"
    ASSIGNED = "ASSIGNED"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

class RequestOrderStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

# User Models
class UserBase(BaseModel):
    phone: str
    role: UserRole
    name: Optional[str] = None
    email: Optional[str] = None
    business_name: Optional[str] = None
    brand_shop_name: Optional[str] = None
    gst_number: Optional[str] = None
    gst_registered_name: Optional[str] = None

class UserCreate(UserBase):
    pass

class User(UserBase):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    status: UserStatus = UserStatus.PENDING
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# OTP Models
class OTPRequest(BaseModel):
    phone: str

class OTPVerify(BaseModel):
    phone: str
    otp: str

class OTPResponse(BaseModel):
    success: bool
    message: str
    sid: Optional[str] = None
    otp: Optional[str] = None

# Product Models
class Product(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    brand: str
    description: Optional[str] = None
    base_price_dealer: int = 300
    base_price_retailer: int = 303
    base_price_customer: int = 305
    min_quantity: int = 100
    stock_available: int = 10000
    image_url: Optional[str] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ProductCreate(BaseModel):
    name: str
    brand: str
    description: Optional[str] = None
    base_price_dealer: int = 300
    base_price_retailer: int = 303
    base_price_customer: int = 305
    min_quantity: int = 100
    stock_available: int = 10000
    image_url: Optional[str] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    brand: Optional[str] = None
    description: Optional[str] = None
    base_price_dealer: Optional[int] = None
    base_price_retailer: Optional[int] = None
    base_price_customer: Optional[int] = None
    stock_available: Optional[int] = None
    is_active: Optional[bool] = None

# Address Models
class Address(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    address_line1: str
    address_line2: Optional[str] = None
    city: str
    state: str
    pincode: str
    is_default: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class AddressCreate(BaseModel):
    address_line1: str
    address_line2: Optional[str] = None
    city: str
    state: str
    pincode: str
    is_default: bool = False

# Cart Models
class CartItem(BaseModel):
    product_id: str
    quantity: int
    price_per_bag: int

class Cart(BaseModel):
    model_config = ConfigDict(extra="ignore")
    user_id: str
    items: List[CartItem] = []
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class CartItemAdd(BaseModel):
    product_id: str
    quantity: int

# Order Models
class OrderItem(BaseModel):
    product_id: str
    product_name: str
    quantity: int
    price_per_bag: int
    total_price: int

class Order(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    order_number: str = Field(default_factory=lambda: f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:6].upper()}")
    items: List[OrderItem]
    subtotal: int
    gst_amount: int = 0
    surcharge_amount: int = 0
    total_amount: int
    payment_method: Optional[PaymentMethod] = None
    payment_status: PaymentStatus = PaymentStatus.PENDING
    order_status: OrderStatus = OrderStatus.PENDING
    delivery_address_id: str
    driver_name: Optional[str] = None
    driver_mobile: Optional[str] = None
    vehicle_number: Optional[str] = None
    invoice_url: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class OrderCreate(BaseModel):
    delivery_address_id: str
    payment_method: PaymentMethod

class OrderUpdate(BaseModel):
    payment_status: Optional[PaymentStatus] = None
    order_status: Optional[OrderStatus] = None
    driver_name: Optional[str] = None
    driver_mobile: Optional[str] = None
    vehicle_number: Optional[str] = None

# Request Order Models
class RequestOrder(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    cement_brand: str
    quantity: int
    delivery_location: str
    phone: str
    preferred_delivery_date: Optional[str] = None
    status: RequestOrderStatus = RequestOrderStatus.PENDING
    admin_notes: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class RequestOrderCreate(BaseModel):
    cement_brand: str
    quantity: int
    delivery_location: str
    phone: str
    preferred_delivery_date: Optional[str] = None

class RequestOrderUpdate(BaseModel):
    status: RequestOrderStatus
    admin_notes: Optional[str] = None

# Response Models
class LoginResponse(BaseModel):
    success: bool
    message: str
    user: Optional[User] = None
    token: Optional[str] = None

class ProductWithPrice(Product):
    user_price: int
```

### 4. `/app/backend/database.py`
```python
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Collections
users_collection = db.users
products_collection = db.products
addresses_collection = db.addresses
carts_collection = db.carts
orders_collection = db.orders
request_orders_collection = db.request_orders
otp_collection = db.otps
```

### 5. `/app/backend/auth.py`
```python
from fastapi import HTTPException, Depends, Header
from typing import Optional
import jwt
import os
from datetime import datetime, timedelta, timezone
from models import User, UserRole
from database import users_collection

SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "cemention-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 43200  # 30 days

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing or invalid")
    
    token = authorization.replace("Bearer ", "")
    payload = verify_token(token)
    user_id = payload.get("user_id")
    
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    
    user_doc = await users_collection.find_one({"id": user_id}, {"_id": 0})
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")
    
    return User(**user_doc)

async def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

async def require_approved(current_user: User = Depends(get_current_user)):
    if current_user.role in [UserRole.DEALER, UserRole.RETAILER]:
        if current_user.status != "APPROVED":
            raise HTTPException(status_code=403, detail="Account pending approval. Contact admin.")
    return current_user
```

### 6. `/app/backend/otp_service.py`
```python
import os
from twilio.rest import Client
from datetime import datetime, timedelta, timezone
import random
from database import otp_collection

# Twilio configuration
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER", "")

# For development/demo mode
DEMO_MODE = os.environ.get("OTP_DEMO_MODE", "true").lower() == "true"

class OTPService:
    def __init__(self):
        self.client = None
        if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and not DEMO_MODE:
            self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    
    async def send_otp(self, phone: str):
        # Generate 6-digit OTP
        otp = str(random.randint(100000, 999999))
        
        # Store OTP in database with expiry
        expiry = datetime.now(timezone.utc) + timedelta(minutes=5)
        await otp_collection.update_one(
            {"phone": phone},
            {"$set": {
                "phone": phone,
                "otp": otp,
                "expiry": expiry.isoformat(),
                "verified": False
            }},
            upsert=True
        )
        
        # Send OTP via Twilio (if not in demo mode)
        if self.client and not DEMO_MODE:
            try:
                message = self.client.messages.create(
                    body=f"Your Cemention verification code is: {otp}. Valid for 5 minutes.",
                    from_=TWILIO_PHONE_NUMBER,
                    to=phone
                )
                return {"success": True, "message": "OTP sent successfully", "sid": message.sid}
            except Exception as e:
                return {"success": False, "message": f"Failed to send OTP: {str(e)}"}
        else:
            # Demo mode - return OTP in response
            return {
                "success": True, 
                "message": "OTP sent successfully (Demo Mode)",
                "otp": otp if DEMO_MODE else None
            }
    
    async def verify_otp(self, phone: str, otp: str):
        # Get OTP from database
        otp_doc = await otp_collection.find_one({"phone": phone})
        
        if not otp_doc:
            return {"success": False, "message": "No OTP found for this phone number"}
        
        # Check if already verified
        if otp_doc.get("verified"):
            return {"success": False, "message": "OTP already used"}
        
        # Check expiry
        expiry = datetime.fromisoformat(otp_doc["expiry"])
        if datetime.now(timezone.utc) > expiry:
            return {"success": False, "message": "OTP has expired"}
        
        # Verify OTP
        if otp_doc["otp"] == otp:
            # Mark as verified
            await otp_collection.update_one(
                {"phone": phone},
                {"$set": {"verified": True}}
            )
            return {"success": True, "message": "OTP verified successfully"}
        else:
            return {"success": False, "message": "Invalid OTP"}

otp_service = OTPService()
```

### 7. `/app/backend/server.py`
```python
from fastapi import FastAPI, APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import os
import logging
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Optional

from models import *
from database import *
from auth import get_current_user, require_admin, require_approved, create_access_token
from otp_service import otp_service
from routes_orders import orders_router
from routes_admin import admin_router

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Create the main app
app = FastAPI(title="Cemention API", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============ AUTH ROUTES ============

@api_router.post("/auth/send-otp", response_model=OTPResponse)
async def send_otp(request: OTPRequest):
    """Send OTP to phone number"""
    result = await otp_service.send_otp(request.phone)
    return OTPResponse(**result)

@api_router.post("/auth/verify-otp", response_model=OTPResponse)
async def verify_otp(request: OTPVerify):
    """Verify OTP"""
    result = await otp_service.verify_otp(request.phone, request.otp)
    return OTPResponse(**result)

@api_router.post("/auth/register", response_model=LoginResponse)
async def register_user(user_data: UserCreate):
    """Register new user with role selection"""
    
    # Check if user already exists
    existing_user = await users_collection.find_one({"phone": user_data.phone}, {"_id": 0})
    if existing_user:
        return LoginResponse(
            success=False,
            message="User already registered. Please login."
        )
    
    # Validate role-specific fields
    if user_data.role in [UserRole.DEALER, UserRole.RETAILER]:
        if not user_data.gst_number or not user_data.gst_registered_name:
            raise HTTPException(status_code=400, detail="GST details are mandatory for Dealers and Retailers")
        if not user_data.business_name or not user_data.brand_shop_name:
            raise HTTPException(status_code=400, detail="Business details are mandatory for Dealers and Retailers")
    
    # Create user
    user = User(**user_data.model_dump())
    
    # Set approval status
    if user.role in [UserRole.DEALER, UserRole.RETAILER]:
        user.status = UserStatus.PENDING
    else:
        user.status = UserStatus.APPROVED
    
    # Store in database
    user_dict = user.model_dump()
    user_dict['created_at'] = user_dict['created_at'].isoformat()
    user_dict['updated_at'] = user_dict['updated_at'].isoformat()
    
    await users_collection.insert_one(user_dict)
    
    # Create token
    token = create_access_token({"user_id": user.id})
    
    return LoginResponse(
        success=True,
        message="Registration successful",
        user=user,
        token=token
    )

@api_router.post("/auth/login", response_model=LoginResponse)
async def login(request: OTPRequest):
    """Login existing user"""
    user_doc = await users_collection.find_one({"phone": request.phone}, {"_id": 0})
    
    if not user_doc:
        return LoginResponse(
            success=False,
            message="User not found. Please register first."
        )
    
    # Convert ISO strings back to datetime
    user_doc['created_at'] = datetime.fromisoformat(user_doc['created_at'])
    user_doc['updated_at'] = datetime.fromisoformat(user_doc['updated_at'])
    
    user = User(**user_doc)
    token = create_access_token({"user_id": user.id})
    
    return LoginResponse(
        success=True,
        message="Login successful",
        user=user,
        token=token
    )

@api_router.get("/auth/me", response_model=User)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user profile"""
    return current_user

# ============ PRODUCT ROUTES ============

@api_router.get("/products", response_model=List[ProductWithPrice])
async def get_products(current_user: User = Depends(require_approved)):
    """Get all active products with role-based pricing"""
    products = await products_collection.find({"is_active": True}, {"_id": 0}).to_list(1000)
    
    # Convert ISO strings to datetime
    for product in products:
        product['created_at'] = datetime.fromisoformat(product['created_at'])
        product['updated_at'] = datetime.fromisoformat(product['updated_at'])
    
    # Add user-specific pricing
    products_with_price = []
    for product in products:
        product_obj = Product(**product)
        
        # Determine price based on role
        if current_user.role == UserRole.DEALER:
            user_price = product_obj.base_price_dealer
        elif current_user.role == UserRole.RETAILER:
            user_price = product_obj.base_price_retailer
        else:
            user_price = product_obj.base_price_customer
        
        product_with_price = ProductWithPrice(**product_obj.model_dump(), user_price=user_price)
        products_with_price.append(product_with_price)
    
    return products_with_price

@api_router.get("/products/{product_id}", response_model=ProductWithPrice)
async def get_product(product_id: str, current_user: User = Depends(require_approved)):
    """Get single product by ID"""
    product = await products_collection.find_one({"id": product_id, "is_active": True}, {"_id": 0})
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product['created_at'] = datetime.fromisoformat(product['created_at'])
    product['updated_at'] = datetime.fromisoformat(product['updated_at'])
    
    product_obj = Product(**product)
    
    # Determine price based on role
    if current_user.role == UserRole.DEALER:
        user_price = product_obj.base_price_dealer
    elif current_user.role == UserRole.RETAILER:
        user_price = product_obj.base_price_retailer
    else:
        user_price = product_obj.base_price_customer
    
    return ProductWithPrice(**product_obj.model_dump(), user_price=user_price)

# ============ CART ROUTES ============

@api_router.get("/cart")
async def get_cart(current_user: User = Depends(require_approved)):
    """Get user's cart"""
    cart = await carts_collection.find_one({"user_id": current_user.id}, {"_id": 0})
    
    if not cart:
        return {"items": [], "total": 0}
    
    # Calculate total
    total = sum(item["quantity"] * item["price_per_bag"] for item in cart.get("items", []))
    
    return {
        "items": cart.get("items", []),
        "total": total
    }

@api_router.post("/cart/add")
async def add_to_cart(item: CartItemAdd, current_user: User = Depends(require_approved)):
    """Add item to cart"""
    
    # Validate quantity
    if item.quantity < 100:
        raise HTTPException(status_code=400, detail="Minimum order quantity is 100 bags")
    
    # Get product
    product = await products_collection.find_one({"id": item.product_id}, {"_id": 0})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product['created_at'] = datetime.fromisoformat(product['created_at'])
    product['updated_at'] = datetime.fromisoformat(product['updated_at'])
    product_obj = Product(**product)
    
    # Get user-specific price
    if current_user.role == UserRole.DEALER:
        price_per_bag = product_obj.base_price_dealer
    elif current_user.role == UserRole.RETAILER:
        price_per_bag = product_obj.base_price_retailer
    else:
        price_per_bag = product_obj.base_price_customer
    
    # Get existing cart
    cart = await carts_collection.find_one({"user_id": current_user.id})
    
    if cart:
        # Check if item already in cart
        items = cart.get("items", [])
        found = False
        for i, cart_item in enumerate(items):
            if cart_item["product_id"] == item.product_id:
                items[i]["quantity"] = item.quantity
                items[i]["price_per_bag"] = price_per_bag
                found = True
                break
        
        if not found:
            items.append({
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price_per_bag": price_per_bag
            })
        
        await carts_collection.update_one(
            {"user_id": current_user.id},
            {"$set": {"items": items, "updated_at": datetime.now(timezone.utc).isoformat()}}
        )
    else:
        # Create new cart
        cart_obj = Cart(
            user_id=current_user.id,
            items=[CartItem(
                product_id=item.product_id,
                quantity=item.quantity,
                price_per_bag=price_per_bag
            )]
        )
        cart_dict = cart_obj.model_dump()
        cart_dict['updated_at'] = cart_dict['updated_at'].isoformat()
        await carts_collection.insert_one(cart_dict)
    
    return {"success": True, "message": "Item added to cart"}

@api_router.delete("/cart/remove/{product_id}")
async def remove_from_cart(product_id: str, current_user: User = Depends(require_approved)):
    """Remove item from cart"""
    cart = await carts_collection.find_one({"user_id": current_user.id})
    
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    items = cart.get("items", [])
    items = [item for item in items if item["product_id"] != product_id]
    
    await carts_collection.update_one(
        {"user_id": current_user.id},
        {"$set": {"items": items, "updated_at": datetime.now(timezone.utc).isoformat()}}
    )
    
    return {"success": True, "message": "Item removed from cart"}

@api_router.delete("/cart/clear")
async def clear_cart(current_user: User = Depends(require_approved)):
    """Clear cart"""
    await carts_collection.update_one(
        {"user_id": current_user.id},
        {"$set": {"items": [], "updated_at": datetime.now(timezone.utc).isoformat()}}
    )
    
    return {"success": True, "message": "Cart cleared"}

# ============ ADDRESS ROUTES ============

@api_router.get("/addresses", response_model=List[Address])
async def get_addresses(current_user: User = Depends(get_current_user)):
    """Get user's addresses"""
    addresses = await addresses_collection.find({"user_id": current_user.id}, {"_id": 0}).to_list(100)
    
    for address in addresses:
        address['created_at'] = datetime.fromisoformat(address['created_at'])
    
    return [Address(**addr) for addr in addresses]

@api_router.post("/addresses", response_model=Address)
async def create_address(address_data: AddressCreate, current_user: User = Depends(get_current_user)):
    """Create new address"""
    
    # If setting as default, unset other defaults
    if address_data.is_default:
        await addresses_collection.update_many(
            {"user_id": current_user.id},
            {"$set": {"is_default": False}}
        )
    
    address = Address(
        **address_data.model_dump(),
        user_id=current_user.id
    )
    
    address_dict = address.model_dump()
    address_dict['created_at'] = address_dict['created_at'].isoformat()
    
    await addresses_collection.insert_one(address_dict)
    
    return address

@api_router.delete("/addresses/{address_id}")
async def delete_address(address_id: str, current_user: User = Depends(get_current_user)):
    """Delete address"""
    result = await addresses_collection.delete_one({"id": address_id, "user_id": current_user.id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Address not found")
    
    return {"success": True, "message": "Address deleted"}

# Include routers
app.include_router(api_router)
app.include_router(orders_router)
app.include_router(admin_router)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
```

### 8. `/app/backend/routes_orders.py`
```python
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import datetime, timezone
import uuid

from models import *
from database import *
from auth import get_current_user, require_approved

orders_router = APIRouter(prefix="/api/orders", tags=["orders"])

@orders_router.post("/create", response_model=Order)
async def create_order(order_data: OrderCreate, current_user: User = Depends(require_approved)):
    """Create order from cart"""
    
    # Get cart
    cart = await carts_collection.find_one({"user_id": current_user.id})
    if not cart or not cart.get("items"):
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    # Verify address
    address = await addresses_collection.find_one({"id": order_data.delivery_address_id, "user_id": current_user.id})
    if not address:
        raise HTTPException(status_code=404, detail="Delivery address not found")
    
    # Build order items
    order_items = []
    subtotal = 0
    
    for cart_item in cart["items"]:
        # Get product details
        product = await products_collection.find_one({"id": cart_item["product_id"]}, {"_id": 0})
        if not product:
            continue
        
        item_total = cart_item["quantity"] * cart_item["price_per_bag"]
        order_items.append(OrderItem(
            product_id=cart_item["product_id"],
            product_name=product["name"],
            quantity=cart_item["quantity"],
            price_per_bag=cart_item["price_per_bag"],
            total_price=item_total
        ))
        subtotal += item_total
    
    # Calculate GST (18% for cement)
    gst_amount = int(subtotal * 0.18)
    
    # Calculate surcharge for card payments
    surcharge_amount = 0
    if order_data.payment_method == PaymentMethod.CARD:
        surcharge_amount = int(subtotal * 0.02)  # 2% surcharge
    
    total_amount = subtotal + gst_amount + surcharge_amount
    
    # Create order
    order = Order(
        user_id=current_user.id,
        items=order_items,
        subtotal=subtotal,
        gst_amount=gst_amount,
        surcharge_amount=surcharge_amount,
        total_amount=total_amount,
        payment_method=order_data.payment_method,
        delivery_address_id=order_data.delivery_address_id
    )
    
    order_dict = order.model_dump()
    order_dict['created_at'] = order_dict['created_at'].isoformat()
    order_dict['updated_at'] = order_dict['updated_at'].isoformat()
    
    await orders_collection.insert_one(order_dict)
    
    # Clear cart
    await carts_collection.update_one(
        {"user_id": current_user.id},
        {"$set": {"items": [], "updated_at": datetime.now(timezone.utc).isoformat()}}
    )
    
    return order

@orders_router.get("/my-orders", response_model=List[Order])
async def get_my_orders(current_user: User = Depends(get_current_user)):
    """Get user's orders"""
    orders = await orders_collection.find({"user_id": current_user.id}, {"_id": 0}).sort("created_at", -1).to_list(1000)
    
    for order in orders:
        order['created_at'] = datetime.fromisoformat(order['created_at'])
        order['updated_at'] = datetime.fromisoformat(order['updated_at'])
    
    return [Order(**order) for order in orders]

@orders_router.get("/{order_id}", response_model=Order)
async def get_order(order_id: str, current_user: User = Depends(get_current_user)):
    """Get order by ID"""
    order = await orders_collection.find_one({"id": order_id, "user_id": current_user.id}, {"_id": 0})
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order['created_at'] = datetime.fromisoformat(order['created_at'])
    order['updated_at'] = datetime.fromisoformat(order['updated_at'])
    
    return Order(**order)

@orders_router.post("/payment-confirmation/{order_id}")
async def confirm_payment(order_id: str, confirmation_data: dict, current_user: User = Depends(get_current_user)):
    """Confirm payment received (for bank transfer/manual verification)"""
    order = await orders_collection.find_one({"id": order_id, "user_id": current_user.id})
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Update payment status to pending (admin will verify)
    await orders_collection.update_one(
        {"id": order_id},
        {"$set": {
            "payment_status": PaymentStatus.PENDING.value,
            "updated_at": datetime.now(timezone.utc).isoformat()
        }}
    )
    
    return {"success": True, "message": "Payment confirmation submitted. Admin will verify."}

# ============ REQUEST ORDER ROUTES ============

@orders_router.post("/request-order", response_model=RequestOrder)
async def create_request_order(request_data: RequestOrderCreate, current_user: User = Depends(require_approved)):
    """Create a request order for large/custom quantities"""
    
    request_order = RequestOrder(
        user_id=current_user.id,
        **request_data.model_dump()
    )
    
    request_dict = request_order.model_dump()
    request_dict['created_at'] = request_dict['created_at'].isoformat()
    
    await request_orders_collection.insert_one(request_dict)
    
    return request_order

@orders_router.get("/request-orders", response_model=List[RequestOrder])
async def get_my_request_orders(current_user: User = Depends(get_current_user)):
    """Get user's request orders"""
    requests = await request_orders_collection.find(
        {"user_id": current_user.id}, 
        {"_id": 0}
    ).sort("created_at", -1).to_list(1000)
    
    for req in requests:
        req['created_at'] = datetime.fromisoformat(req['created_at'])
    
    return [RequestOrder(**req) for req in requests]
```

### 9. `/app/backend/routes_admin.py`
```python
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime, timezone

from models import *
from database import *
from auth import require_admin

admin_router = APIRouter(prefix="/api/admin", tags=["admin"])

# ============ USER MANAGEMENT ============

@admin_router.get("/users/pending", response_model=List[User])
async def get_pending_users(current_admin: User = Depends(require_admin)):
    """Get all pending user approvals"""
    users = await users_collection.find(
        {"status": UserStatus.PENDING.value},
        {"_id": 0}
    ).to_list(1000)
    
    for user in users:
        user['created_at'] = datetime.fromisoformat(user['created_at'])
        user['updated_at'] = datetime.fromisoformat(user['updated_at'])
    
    return [User(**user) for user in users]

@admin_router.get("/users", response_model=List[User])
async def get_all_users(role: Optional[str] = None, current_admin: User = Depends(require_admin)):
    """Get all users"""
    query = {}
    if role:
        query["role"] = role
    
    users = await users_collection.find(query, {"_id": 0}).to_list(1000)
    
    for user in users:
        user['created_at'] = datetime.fromisoformat(user['created_at'])
        user['updated_at'] = datetime.fromisoformat(user['updated_at'])
    
    return [User(**user) for user in users]

@admin_router.patch("/users/{user_id}/approve")
async def approve_user(user_id: str, current_admin: User = Depends(require_admin)):
    """Approve user registration"""
    result = await users_collection.update_one(
        {"id": user_id},
        {"$set": {
            "status": UserStatus.APPROVED.value,
            "updated_at": datetime.now(timezone.utc).isoformat()
        }}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"success": True, "message": "User approved"}

@admin_router.patch("/users/{user_id}/reject")
async def reject_user(user_id: str, current_admin: User = Depends(require_admin)):
    """Reject user registration"""
    result = await users_collection.update_one(
        {"id": user_id},
        {"$set": {
            "status": UserStatus.REJECTED.value,
            "updated_at": datetime.now(timezone.utc).isoformat()
        }}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"success": True, "message": "User rejected"}

# ============ PRODUCT MANAGEMENT ============

@admin_router.post("/products", response_model=Product)
async def create_product(product_data: ProductCreate, current_admin: User = Depends(require_admin)):
    """Create new product"""
    product = Product(**product_data.model_dump())
    
    product_dict = product.model_dump()
    product_dict['created_at'] = product_dict['created_at'].isoformat()
    product_dict['updated_at'] = product_dict['updated_at'].isoformat()
    
    await products_collection.insert_one(product_dict)
    
    return product

@admin_router.get("/products", response_model=List[Product])
async def get_all_products(current_admin: User = Depends(require_admin)):
    """Get all products (including inactive)"""
    products = await products_collection.find({}, {"_id": 0}).to_list(1000)
    
    for product in products:
        product['created_at'] = datetime.fromisoformat(product['created_at'])
        product['updated_at'] = datetime.fromisoformat(product['updated_at'])
    
    return [Product(**product) for product in products]

@admin_router.patch("/products/{product_id}", response_model=Product)
async def update_product(product_id: str, product_data: ProductUpdate, current_admin: User = Depends(require_admin)):
    """Update product"""
    update_data = {k: v for k, v in product_data.model_dump().items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    update_data["updated_at"] = datetime.now(timezone.utc).isoformat()
    
    result = await products_collection.update_one(
        {"id": product_id},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Return updated product
    product = await products_collection.find_one({"id": product_id}, {"_id": 0})
    product['created_at'] = datetime.fromisoformat(product['created_at'])
    product['updated_at'] = datetime.fromisoformat(product['updated_at'])
    
    return Product(**product)

@admin_router.delete("/products/{product_id}")
async def delete_product(product_id: str, current_admin: User = Depends(require_admin)):
    """Soft delete product (mark as inactive)"""
    result = await products_collection.update_one(
        {"id": product_id},
        {"$set": {
            "is_active": False,
            "updated_at": datetime.now(timezone.utc).isoformat()
        }}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {"success": True, "message": "Product deactivated"}

# ============ ORDER MANAGEMENT ============

@admin_router.get("/orders", response_model=List[Order])
async def get_all_orders(current_admin: User = Depends(require_admin)):
    """Get all orders"""
    orders = await orders_collection.find({}, {"_id": 0}).sort("created_at", -1).to_list(1000)
    
    for order in orders:
        order['created_at'] = datetime.fromisoformat(order['created_at'])
        order['updated_at'] = datetime.fromisoformat(order['updated_at'])
    
    return [Order(**order) for order in orders]

@admin_router.patch("/orders/{order_id}", response_model=Order)
async def update_order(order_id: str, order_data: OrderUpdate, current_admin: User = Depends(require_admin)):
    """Update order status/details"""
    update_data = {k: v.value if isinstance(v, Enum) else v for k, v in order_data.model_dump().items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    update_data["updated_at"] = datetime.now(timezone.utc).isoformat()
    
    result = await orders_collection.update_one(
        {"id": order_id},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Return updated order
    order = await orders_collection.find_one({"id": order_id}, {"_id": 0})
    order['created_at'] = datetime.fromisoformat(order['created_at'])
    order['updated_at'] = datetime.fromisoformat(order['updated_at'])
    
    return Order(**order)

# ============ REQUEST ORDER MANAGEMENT ============

@admin_router.get("/request-orders", response_model=List[RequestOrder])
async def get_all_request_orders(current_admin: User = Depends(require_admin)):
    """Get all request orders"""
    requests = await request_orders_collection.find({}, {"_id": 0}).sort("created_at", -1).to_list(1000)
    
    for req in requests:
        req['created_at'] = datetime.fromisoformat(req['created_at'])
    
    return [RequestOrder(**req) for req in requests]

@admin_router.patch("/request-orders/{request_id}", response_model=RequestOrder)
async def update_request_order(request_id: str, request_data: RequestOrderUpdate, current_admin: User = Depends(require_admin)):
    """Update request order status"""
    update_data = {k: v.value if isinstance(v, Enum) else v for k, v in request_data.model_dump().items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    result = await request_orders_collection.update_one(
        {"id": request_id},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Request order not found")
    
    # Return updated request
    request_order = await request_orders_collection.find_one({"id": request_id}, {"_id": 0})
    request_order['created_at'] = datetime.fromisoformat(request_order['created_at'])
    
    return RequestOrder(**request_order)

# ============ REPORTS ============

@admin_router.get("/reports/summary")
async def get_summary_report(current_admin: User = Depends(require_admin)):
    """Get summary statistics"""
    total_users = await users_collection.count_documents({})
    pending_users = await users_collection.count_documents({"status": UserStatus.PENDING.value})
    total_orders = await orders_collection.count_documents({})
    pending_orders = await orders_collection.count_documents({"payment_status": PaymentStatus.PENDING.value})
    completed_orders = await orders_collection.count_documents({"order_status": OrderStatus.DELIVERED.value})
    
    # Calculate revenue
    orders = await orders_collection.find({"payment_status": PaymentStatus.RECEIVED.value}, {"_id": 0}).to_list(10000)
    total_revenue = sum(order.get("total_amount", 0) for order in orders)
    
    return {
        "total_users": total_users,
        "pending_users": pending_users,
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "completed_orders": completed_orders,
        "total_revenue": total_revenue
    }
```

### 10. `/app/backend/seed_db.py`
```python
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

async def seed_data():
    print("Seeding database...")
    
    # Create admin user
    admin_exists = await db.users.find_one({"role": "ADMIN"})
    if not admin_exists:
        admin_user = {
            "id": "admin-001",
            "phone": "+911234567890",
            "role": "ADMIN",
            "name": "Admin User",
            "email": "admin@cemention.com",
            "status": "APPROVED",
            "is_active": True,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        await db.users.insert_one(admin_user)
        print("✓ Admin user created (Phone: +911234567890)")
    
    # Create sample products
    products_exist = await db.products.count_documents({})
    if products_exist == 0:
        products = [
            {
                "id": "prod-001",
                "name": "UltraTech PPC Cement",
                "brand": "UltraTech",
                "description": "Portland Pozzolana Cement - 50kg bags",
                "base_price_dealer": 300,
                "base_price_retailer": 303,
                "base_price_customer": 305,
                "min_quantity": 100,
                "stock_available": 10000,
                "image_url": "https://images.unsplash.com/photo-1625308216182-218ff63d47bb?w=400",
                "is_active": True,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat()
            },
            {
                "id": "prod-002",
                "name": "ACC Gold Cement",
                "brand": "ACC",
                "description": "High strength cement - 50kg bags",
                "base_price_dealer": 305,
                "base_price_retailer": 308,
                "base_price_customer": 310,
                "min_quantity": 100,
                "stock_available": 8000,
                "image_url": "https://images.unsplash.com/photo-1625308216182-218ff63d47bb?w=400",
                "is_active": True,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat()
            },
            {
                "id": "prod-003",
                "name": "Ambuja OPC Cement",
                "brand": "Ambuja",
                "description": "Ordinary Portland Cement - 50kg bags",
                "base_price_dealer": 298,
                "base_price_retailer": 301,
                "base_price_customer": 303,
                "min_quantity": 100,
                "stock_available": 12000,
                "image_url": "https://images.unsplash.com/photo-1625308216182-218ff63d47bb?w=400",
                "is_active": True,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat()
            }
        ]
        await db.products.insert_many(products)
        print(f"✓ {len(products)} products created")
    
    print("Database seeding completed!")
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_data())
```

---

## Frontend Files

### 1. `/app/frontend/.env`
```env
REACT_APP_BACKEND_URL=https://your-domain.preview.emergentagent.com
WDS_SOCKET_PORT=443
ENABLE_HEALTH_CHECK=false
```

### 2. `/app/frontend/package.json`
```json
{
  "name": "frontend",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "@hookform/resolvers": "^5.0.1",
    "@radix-ui/react-accordion": "^1.2.8",
    "@radix-ui/react-alert-dialog": "^1.1.11",
    "@radix-ui/react-aspect-ratio": "^1.1.4",
    "@radix-ui/react-avatar": "^1.1.7",
    "@radix-ui/react-checkbox": "^1.2.3",
    "@radix-ui/react-collapsible": "^1.1.8",
    "@radix-ui/react-context-menu": "^2.2.12",
    "@radix-ui/react-dialog": "^1.1.11",
    "@radix-ui/react-dropdown-menu": "^2.1.12",
    "@radix-ui/react-hover-card": "^1.1.11",
    "@radix-ui/react-label": "^2.1.4",
    "@radix-ui/react-menubar": "^1.1.12",
    "@radix-ui/react-navigation-menu": "^1.2.10",
    "@radix-ui/react-popover": "^1.1.11",
    "@radix-ui/react-progress": "^1.1.4",
    "@radix-ui/react-radio-group": "^1.3.4",
    "@radix-ui/react-scroll-area": "^1.2.6",
    "@radix-ui/react-select": "^2.2.2",
    "@radix-ui/react-separator": "^1.1.4",
    "@radix-ui/react-slider": "^1.3.2",
    "@radix-ui/react-slot": "^1.2.0",
    "@radix-ui/react-switch": "^1.2.2",
    "@radix-ui/react-tabs": "^1.1.9",
    "@radix-ui/react-toast": "^1.2.11",
    "@radix-ui/react-toggle": "^1.1.6",
    "@radix-ui/react-toggle-group": "^1.1.7",
    "@radix-ui/react-tooltip": "^1.2.4",
    "axios": "^1.8.4",
    "class-variance-authority": "^0.7.1",
    "clsx": "^2.1.1",
    "cmdk": "^1.1.1",
    "cra-template": "1.2.0",
    "date-fns": "^4.1.0",
    "embla-carousel-react": "^8.6.0",
    "input-otp": "^1.4.2",
    "lucide-react": "^0.507.0",
    "next-themes": "^0.4.6",
    "react": "^19.0.0",
    "react-day-picker": "8.10.1",
    "react-dom": "^19.0.0",
    "react-hook-form": "^7.56.2",
    "react-resizable-panels": "^3.0.1",
    "react-router-dom": "^7.5.1",
    "react-scripts": "5.0.1",
    "recharts": "^3.6.0",
    "sonner": "^2.0.3",
    "tailwind-merge": "^3.2.0",
    "tailwindcss-animate": "^1.0.7",
    "vaul": "^1.1.2",
    "zod": "^3.24.4"
  },
  "scripts": {
    "start": "craco start",
    "build": "craco build",
    "test": "craco test"
  },
  "browserslist": {
    "production": [">0.2%", "not dead", "not op_mini all"],
    "development": ["last 1 chrome version", "last 1 firefox version", "last 1 safari version"]
  },
  "devDependencies": {
    "@babel/plugin-proposal-private-property-in-object": "^7.21.11",
    "@craco/craco": "^7.1.0",
    "@eslint/js": "9.23.0",
    "autoprefixer": "^10.4.20",
    "eslint": "9.23.0",
    "eslint-plugin-import": "2.31.0",
    "eslint-plugin-jsx-a11y": "6.10.2",
    "eslint-plugin-react": "7.37.4",
    "eslint-plugin-react-hooks": "5.2.0",
    "globals": "15.15.0",
    "postcss": "^8.4.49",
    "tailwindcss": "^3.4.17"
  },
  "packageManager": "yarn@1.22.22"
}
```

### 3. `/app/frontend/tailwind.config.js`
```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: [
    './pages/**/*.{js,jsx}',
    './components/**/*.{js,jsx}',
    './app/**/*.{js,jsx}',
    './src/**/*.{js,jsx}',
  ],
  prefix: "",
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "#0F172A",
          foreground: "#F8FAFC",
          hover: "#1E293B",
        },
        secondary: {
          DEFAULT: "#F1F5F9",
          foreground: "#0F172A",
          hover: "#E2E8F0",
        },
        accent: {
          DEFAULT: "#F97316",
          foreground: "#FFFFFF",
          hover: "#EA580C",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
        slate: {
          900: "#0F172A",
          800: "#1E293B",
          600: "#475569",
          500: "#64748B",
          200: "#E2E8F0",
          100: "#F1F5F9",
        },
        orange: {
          600: "#EA580C",
          500: "#F97316",
        },
      },
      fontFamily: {
        heading: ['Manrope', 'sans-serif'],
        body: ['Inter', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}
```

### 4. `/app/frontend/src/index.css`
```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&family=Manrope:wght@400;700;800&display=swap');

@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
    --primary: 222.2 47% 11%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47% 11%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47% 11%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 222.2 84% 4.9%;
    --radius: 0.25rem;
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground font-body;
  }
  h1, h2, h3, h4, h5, h6 {
    @apply font-heading;
  }
}
```

### 5. `/app/frontend/src/App.css`
```css
.App-logo {
    height: 40vmin;
    pointer-events: none;
}

@media (prefers-reduced-motion: no-preference) {
    .App-logo {
        animation: App-logo-spin infinite 20s linear;
    }
}

.App-header {
    background-color: #0f0f10;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-size: calc(10px + 2vmin);
    color: white;
}

.App-link {
    color: #61dafb;
}

@keyframes App-logo-spin {
    from {
        transform: rotate(0deg);
    }
    to {
        transform: rotate(360deg);
    }
}
```

---

## Configuration Files

### `/app/frontend/src/api.js`
```javascript
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
export const API_BASE = `${BACKEND_URL}/api`;

const api = axios.create({
  baseURL: API_BASE,
});

// Add auth token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Auth API
export const authAPI = {
  sendOTP: (phone) => api.post('/auth/send-otp', { phone }),
  verifyOTP: (phone, otp) => api.post('/auth/verify-otp', { phone, otp }),
  register: (userData) => api.post('/auth/register', userData),
  login: (phone) => api.post('/auth/login', { phone }),
  getMe: () => api.get('/auth/me'),
};

// Products API
export const productsAPI = {
  getAll: () => api.get('/products'),
  getById: (id) => api.get(`/products/${id}`),
};

// Cart API
export const cartAPI = {
  get: () => api.get('/cart'),
  add: (productId, quantity) => api.post('/cart/add', { product_id: productId, quantity }),
  remove: (productId) => api.delete(`/cart/remove/${productId}`),
  clear: () => api.delete('/cart/clear'),
};

// Address API
export const addressAPI = {
  getAll: () => api.get('/addresses'),
  create: (addressData) => api.post('/addresses', addressData),
  delete: (id) => api.delete(`/addresses/${id}`),
};

// Orders API
export const ordersAPI = {
  create: (orderData) => api.post('/orders/create', orderData),
  getMyOrders: () => api.get('/orders/my-orders'),
  getById: (id) => api.get(`/orders/${id}`),
  confirmPayment: (orderId, data) => api.post(`/orders/payment-confirmation/${orderId}`, data),
  createRequestOrder: (requestData) => api.post('/orders/request-order', requestData),
  getMyRequestOrders: () => api.get('/orders/request-orders'),
};

// Admin API
export const adminAPI = {
  // Users
  getPendingUsers: () => api.get('/admin/users/pending'),
  getAllUsers: (role) => api.get('/admin/users', { params: { role } }),
  approveUser: (userId) => api.patch(`/admin/users/${userId}/approve`),
  rejectUser: (userId) => api.patch(`/admin/users/${userId}/reject`),
  
  // Products
  createProduct: (productData) => api.post('/admin/products', productData),
  getAllProducts: () => api.get('/admin/products'),
  updateProduct: (productId, productData) => api.patch(`/admin/products/${productId}`, productData),
  deleteProduct: (productId) => api.delete(`/admin/products/${productId}`),
  
  // Orders
  getAllOrders: () => api.get('/admin/orders'),
  updateOrder: (orderId, orderData) => api.patch(`/admin/orders/${orderId}`, orderData),
  
  // Request Orders
  getAllRequestOrders: () => api.get('/admin/request-orders'),
  updateRequestOrder: (requestId, requestData) => api.patch(`/admin/request-orders/${requestId}`, requestData),
  
  // Reports
  getSummaryReport: () => api.get('/admin/reports/summary'),
};

export default api;
```

### `/app/frontend/src/AuthContext.js`
```javascript
import React, { createContext, useContext, useState, useEffect } from 'react';
import { authAPI } from './api';

const AuthContext = createContext(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        const response = await authAPI.getMe();
        setUser(response.data);
      } catch (error) {
        console.error('Auth check failed:', error);
        localStorage.removeItem('token');
      }
    }
    setLoading(false);
  };

  const login = (userData, token) => {
    localStorage.setItem('token', token);
    setUser(userData);
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, checkAuth }}>
      {children}
    </AuthContext.Provider>
  );
};
```

### `/app/frontend/src/utils.js`
```javascript
export const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0,
  }).format(amount);
};

export const formatPhone = (phone) => {
  if (phone.startsWith('+91')) return phone;
  if (phone.startsWith('91')) return `+${phone}`;
  return `+91${phone}`;
};

export const getRoleName = (role) => {
  const roleMap = {
    DEALER: 'Dealer',
    RETAILER: 'Retailer',
    CUSTOMER: 'Customer',
    ADMIN: 'Admin',
  };
  return roleMap[role] || role;
};

export const getStatusColor = (status) => {
  const colors = {
    PENDING: 'bg-yellow-100 text-yellow-800 border-yellow-200',
    APPROVED: 'bg-green-100 text-green-800 border-green-200',
    REJECTED: 'bg-red-100 text-red-800 border-red-200',
    RECEIVED: 'bg-green-100 text-green-800 border-green-200',
    FAILED: 'bg-red-100 text-red-800 border-red-200',
    DELIVERED: 'bg-green-100 text-green-800 border-green-200',
    CANCELLED: 'bg-red-100 text-red-800 border-red-200',
    ASSIGNED: 'bg-blue-100 text-blue-800 border-blue-200',
    OUT_FOR_DELIVERY: 'bg-blue-100 text-blue-800 border-blue-200',
    PAYMENT_RECEIVED: 'bg-green-100 text-green-800 border-green-200',
  };
  return colors[status] || 'bg-gray-100 text-gray-800 border-gray-200';
};
```

---

## Setup Instructions

### Backend Setup
```bash
cd /app/backend

# Install dependencies
pip install -r requirements.txt

# Seed database
python seed_db.py

# Run server (managed by supervisor)
sudo supervisorctl restart backend
```

### Frontend Setup
```bash
cd /app/frontend

# Install dependencies
yarn install

# Run development server (managed by supervisor)
sudo supervisorctl restart frontend
```

### Environment Variables
1. Update `/app/backend/.env` with your credentials
2. Update `/app/frontend/.env` with your backend URL

### Admin Credentials
- Phone: +911234567890
- Use Demo OTP shown on screen

### Key Features
- Phone + OTP Authentication
- Role-based pricing (Dealer/Retailer/Customer)
- Product management (Add/Edit products and pricing)
- Shopping cart and checkout
- Order management
- Admin dashboard

---

**Note:** Due to file size limits, I've included the main structure. For complete page components (LandingPage, AuthPage, ProductsPage, CartPage, CheckoutPage, OrdersPage, AdminPage), please refer to the files in `/app/frontend/src/pages/` directory.
