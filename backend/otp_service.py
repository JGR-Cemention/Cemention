import os
import random
from datetime import datetime, timedelta, timezone
from twilio.rest import Client

from database import otp_collection

# ================= ENV CONFIG =================

TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "").strip()
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "").strip()
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER", "").strip()

DEMO_MODE = os.environ.get("OTP_DEMO_MODE", "true").lower() == "true"


# ================= OTP SERVICE =================

class OTPService:
    def __init__(self):
        self.client = None

        if not DEMO_MODE and TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
            try:
                self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
                print("✅ Twilio client initialized")
            except Exception as e:
                print("❌ Twilio init failed:", e)

    async def send_otp(self, phone: str):
        if otp_collection is None:
            print("❌ otp_collection is None (DB not connected)")
            return {
                "success": False,
                "message": "Database not available. Please try later."
            }

        otp = str(random.randint(100000, 999999))
        expiry = datetime.now(timezone.utc) + timedelta(minutes=5)

        # ---- STORE OTP ----
        try:
            await otp_collection.update_one(
                {"phone": phone},
                {
                    "$set": {
                        "phone": phone,
                        "otp": otp,
                        "expiry": expiry.isoformat(),
                        "verified": False,
                    }
                },
                upsert=True,
            )
            print(f"✅ OTP stored for {phone}")
        except Exception as e:
            print("❌ Failed to store OTP in DB:", e)
            return {
                "success": False,
                "message": "Failed to generate OTP. Please retry."
            }

        # ---- REAL SMS MODE ----
        if self.client and not DEMO_MODE:
            try:
                message = self.client.messages.create(
                    body=f"Your Cemention verification code is {otp}. Valid for 5 minutes.",
                    from_=TWILIO_PHONE_NUMBER,
                    to=phone,
                )
                return {
                    "success": True,
                    "message": "OTP sent successfully",
                    "sid": message.sid,
                }
            except Exception as e:
                print("❌ Twilio send failed:", e)
                return {
                    "success": False,
                    "message": "Failed to send OTP via SMS",
                }

        # ---- DEMO MODE ----
        print(f"🧪 DEMO MODE OTP for {phone}: {otp}")
        return {
            "success": True,
            "message": "OTP sent successfully (Demo Mode)",
            "otp": otp,
        }

    async def verify_otp(self, phone: str, otp: str):
        if otp_collection is None:
            return {
                "success": False,
                "message": "Database not available"
            }

        otp_doc = await otp_collection.find_one({"phone": phone})

        if not otp_doc:
            return {"success": False, "message": "No OTP found"}

        if otp_doc.get("verified"):
            return {"success": False, "message": "OTP already used"}

        expiry = datetime.fromisoformat(otp_doc["expiry"])
        if datetime.now(timezone.utc) > expiry:
            return {"success": False, "message": "OTP expired"}

        if otp_doc["otp"] != otp:
            return {"success": False, "message": "Invalid OTP"}

        await otp_collection.update_one(
            {"phone": phone},
            {"$set": {"verified": True}},
        )

        return {"success": True, "message": "OTP verified successfully"}


otp_service = OTPService()

