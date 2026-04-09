from flask import Flask, request, jsonify
from src.features import extract_rfm_features, haversine_distance
from src.detection import FraudDetector
from src.response import evaluate_action

app = Flask(__name__)
detector = FraudDetector()

@app.route('/analyze-transaction', methods=['POST'])
def analyze():
    data = request.json
    
    # 1. Trích xuất đặc trưng
    amt = data.get('amount', 0)
    dist = data.get('distance_from_last', 0)
    freq = data.get('freq_24h', 1)
    dev = data.get('is_new_device', 0)
    
    # 2. Lớp Luật cứng (Hard Rules) - Chặn ngay lập tức nếu vi phạm nghiêm trọng
    if dist > 1000 and dev == 1: # Impossible Travel + Thiết bị lạ
        return jsonify({"action": "BLOCK", "message": "Phát hiện xâm nhập trái phép (Location)", "code": 403})
    
    if freq > 40: # Tần suất quá khủng khiếp
        return jsonify({"action": "BLOCK", "message": "Phát hiện tấn công vét cạn", "code": 403})

    # 3. Lớp AI (Nếu không vi phạm luật cứng thì mới hỏi AI)
    features = [amt, freq, dist, dev]
    risk_score = detector.predict_risk(features)
    decision = evaluate_action(risk_score)
    
    return jsonify(decision)

if __name__ == '__main__':
    app.run(port=5000, debug=True)