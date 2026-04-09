import pandas as pd
import numpy as np
import os
import sys

# Thiết lập output terminal hỗ trợ UTF-8 để tránh lỗi hiển thị tiếng Việt
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

def generate_sample_data(file_path='data/transactions.csv'):
    # Tạo thư mục data nếu chưa có
    folder = os.path.dirname(file_path)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)

    np.random.seed(42)
    n_samples = 1000
    
    # --- NHÓM 1: GIAO DỊCH BÌNH THƯỜNG ---
    normal_data = {
        'amount': np.random.normal(500, 200, 950).clip(10, 2000),
        'freq_24h': np.random.randint(1, 5, 950),
        'distance_km': np.random.exponential(5, 950).clip(0, 50),
        'is_new_device': np.random.choice([0, 1], 950, p=[0.9, 0.1])
    }
    
    # --- NHÓM 2: GIAO DỊCH GIAN LẬN (Outliers) ---
    fraud_data = {
        'amount': np.random.uniform(5000, 20000, 50),
        'freq_24h': np.random.randint(10, 50, 50),
        'distance_km': np.random.uniform(200, 2000, 50),
        'is_new_device': np.random.choice([0, 1], 50, p=[0.2, 0.8])
    }

    df_normal = pd.DataFrame(normal_data)
    df_fraud = pd.DataFrame(fraud_data)
    df = pd.concat([df_normal, df_fraud]).sample(frac=1).reset_index(drop=True)

    # Lưu file với encoding utf-8
    df.to_csv(file_path, index=False, encoding='utf-8')
    
    print(f"Success: Da tao file tai {file_path}")
    print(f"Total records: {len(df)}")
    print(df.head())

if __name__ == "__main__":
    generate_sample_data()