import os
import random
from datetime import datetime, timedelta, timezone
from twilio.rest import Client

# ================= CONFIG =================

DEMO_MODE = True  # 🔥 FORCE DEMO MODE (APP WILL WORK)
print("🟢 OTP SERVICE RUNNING IN DEMO MODE")

# ================= OTP SERVICE =================

class OTPService:
    async def send_otp(self, phone: str):
        otp = str(random.randint(100000, 999999))

        print(f"🧪 DEMO OTP for {phone}: {otp}")

        return {
            "success": True,
            "message": "OTP sent successfully (Demo Mode)",
            "otp": otp,
        }

    async def verify_otp(self, phone: str, otp: str):
        # In demo mode, accept ANY 6-digit OTP
        if len(otp) == 6:
            return {"success": True, "message": "OTP verified (Demo Mode)"}

        return {"success": False, "message": "Invalid OTP"}

otp_service = OTPService()

