import hashlib
import hmac
import logging
import os

# Cấu hình Logging
logging.basicConfig(
    filename='frade_system.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

SECRET_KEY = "SECRET_FRADE_KEY" # Trong thực tế nên dùng biến môi trường (env)

def generate_device_hash(device_info_string):
    """Băm thông tin thiết bị bằng HMAC-SHA256 để bảo mật"""
    hash_result = hmac.new(
        SECRET_KEY.encode(), 
        device_info_string.encode(), 
        hashlib.sha256
    ).hexdigest()
    return hash_result

def log_fraud_event(user_id, transaction_id, score, action):
    """Ghi lại các sự kiện rủi ro cao vào file log"""
    msg = f"USER: {user_id} | TX_ID: {transaction_id} | SCORE: {score} | ACTION: {action}"
    if action == "BLOCK":
        logging.warning(f"CRITICAL: {msg}")
    else:
        logging.info(msg)