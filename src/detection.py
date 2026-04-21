import math
import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

class FraudDetector:
    def __init__(self, model_path='models/iso_forest.pkl'):
        try:
            self.model = joblib.load(model_path)
        except:
            self.model = IsolationForest(contamination=0.02, random_state=42) # Giảm tỷ lệ nhiễm bẩn
    def train(self, X_train):
        self.model.fit(X_train)
        joblib.dump(self.model, 'models/iso_forest.pkl')

    import pandas as pd

    def predict_risk(self, feature_vector):
        # Khai báo tên cột giống hệt lúc train trong train_pipeline.py
        feature_names = ['amount', 'freq_24h', 'distance_km', 'is_new_device']
        X = pd.DataFrame([feature_vector], columns=feature_names)
        
        score = self.model.decision_function(X)[0]
        risk_score = 1 / (1 + math.exp(score * 10)) 
        return risk_score * 10  # Scale to 0-10