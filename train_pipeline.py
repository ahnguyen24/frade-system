import pandas as pd
from src.detection import FraudDetector
from src.utils import logging
import joblib
import os

def run_training_pipeline():
    logging.info("Bắt đầu quy trình huấn luyện lại mô hình...")
    
    # 1. Giả lập tải dữ liệu từ DB (Thay thế bằng query thực tế từ D2: Transactions)
    # Dữ liệu bao gồm các cột: amount, freq_24h, distance_km, is_new_device
    try:
        if not os.path.exists('data/transactions.csv'):
            logging.error("Không tìm thấy dữ liệu huấn luyện!")
            return
            
        df = pd.read_csv('data/transactions.csv')
        X_train = df[['amount', 'freq_24h', 'distance_km', 'is_new_device']]

        # 2. Khởi tạo và huấn luyện
        # Chúng ta dùng Isolation Forest vì dữ liệu thực tế thường không có nhãn (unlabeled)
        detector = FraudDetector()
        logging.info(f"Đang huấn luyện với {len(X_train)} bản ghi...")
        detector.train(X_train)

        logging.info("Huấn luyện hoàn tất. Đã cập nhật models/iso_forest.pkl")
        
    except Exception as e:
        logging.error(f"Lỗi trong quá trình training: {str(e)}")

if __name__ == "__main__":
    run_training_pipeline()