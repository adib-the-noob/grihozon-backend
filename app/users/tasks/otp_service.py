from celery import shared_task

@shared_task
def send_otp(
    to_phone_number: str,
    otp_code: str,
):
    """
    Simulates sending an OTP code to the specified phone number.
    In a real implementation, this function would integrate with an SMS gateway.
    """
    print(f"Sending OTP {otp_code} to phone number {to_phone_number}")