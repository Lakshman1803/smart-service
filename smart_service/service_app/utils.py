import random
from django.conf import settings
from .models import OTP


def generate_otp(mobile, purpose):
    """Generate a 6-digit OTP and save to DB."""
    otp_code = str(random.randint(100000, 999999))
    OTP.objects.filter(mobile=mobile, purpose=purpose, is_used=False).update(is_used=True)
    otp_obj = OTP.objects.create(mobile=mobile, otp=otp_code, purpose=purpose)
    return otp_code


def send_otp(mobile, otp_code, purpose='verification'):
    """Send OTP via SMS. Uses console backend in dev mode."""
    message = f"[SMART SERVICE] Your OTP for {purpose} is: {otp_code}. Valid for 5 minutes. Do not share."

    if settings.SMS_BACKEND == 'console':
        print(f"\n{'='*50}")
        print(f"  📱 OTP SMS (Console Mode)")
        print(f"  To: {mobile}")
        print(f"  OTP: {otp_code}")
        print(f"  Message: {message}")
        print(f"{'='*50}\n")
        return True

    # Real SMS via Twilio
    try:
        from twilio.rest import Client
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=f"+91{mobile}"
        )
        return True
    except Exception as e:
        print(f"SMS Error: {e}")
        return False


def verify_otp(mobile, otp_code, purpose):
    """Verify OTP. Returns True if valid, False otherwise."""
    try:
        otp_obj = OTP.objects.filter(
            mobile=mobile, otp=otp_code, purpose=purpose, is_used=False
        ).latest('created_at')
        if otp_obj.is_valid():
            otp_obj.is_used = True
            otp_obj.save()
            return True
        return False
    except OTP.DoesNotExist:
        return False
