# backend/otp_service.py

import random

# ================= CONFIG =================

DEMO_MODE = True  # 🔥 FORCE DEMO MODE
print("🟢 OTP SERVICE RUNNING IN DEMO MODE")

# ================= IN-MEMORY STORE (DEMO SAFE) =================
# phone -> otp
_demo_otp_store = {}

# ================= OTP SERVICE =================

class OTPService:
    async def send_otp(self, phone: str):
        otp = str(random.randint(100000, 999999))

        # store OTP in memory
        _demo_otp_store[phone] = otp

        print(f"🧪 DEMO OTP for {phone}: {otp}")

        return {
            "success": True,
            "message": "OTP sent successfully (Demo Mode)",
            "otp": otp,  # frontend can show this
        }

    async def verify_otp(self, phone: str, otp: str):
        stored_otp = _demo_otp_store.get(phone)

        if not stored_otp:
            return {
                "success": False,
                "message": "OTP not found. Please request again."
            }

        if otp == stored_otp:
            # remove after successful verification
            _demo_otp_store.pop(phone, None)

            return {
                "success": True,
                "message": "OTP verified successfully (Demo Mode)"
            }

        return {
            "success": False,
            "message": "Invalid OTP"
        }

otp_service = OTPService()
