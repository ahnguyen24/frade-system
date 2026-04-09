import math
import pandas as pd

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

def extract_rfm_features(user_transactions):
    # Giả sử nhận vào một DataFrame các giao dịch gần nhất của 1 user
    df = pd.DataFrame(user_transactions)
    recency = (pd.Timestamp.now() - df['timestamp'].max()).total_seconds() / 3600
    frequency = len(df)
    monetary = df['amount'].sum()
    return [recency, frequency, monetary]