from flask import Flask, request, jsonify
from src.features import extract_rfm_features, haversine_distance
from src.detection import FraudDetector
from src.response import evaluate_action

app = Flask(__name__)
detector = FraudDetector()

@app.route('/analyze-transaction', methods=['POST'])
def analyze():
    data = request.json
    
    # 1. Extract Features
    amt = data.get('amount', 0)
    dist = data.get('distance_from_last', 0)
    freq = data.get('freq_24h', 1)
    dev = data.get('is_new_device', 0)
    
    features = [amt, freq, dist, dev]

    # 2. ALWAYS calculate risk score first to ensure it's displayed
    risk_score = detector.predict_risk(features)
    risk_score_rounded = round(float(risk_score), 4)

    # 3. Hard Rules (Now checking after scoring, or using score in response)
    # Impossible Travel Rule
    if dist > 1000 and dev == 1:
        return jsonify({
            "action": "BLOCK",
            "message": "Security Alert: Impossible Travel Detected",
            "code": 403,
            "risk_score": risk_score_rounded
        })
    
    # High Velocity Rule
    if freq > 40:
        return jsonify({
            "action": "BLOCK",
            "message": "Security Alert: Excessive Transaction Velocity",
            "code": 403,
            "risk_score": risk_score_rounded
        })

    # 4. AI-based Decision (If hard rules didn't trigger)
    decision = evaluate_action(risk_score)
    
    # Ensure all AI responses also include the score and English messages
    decision['risk_score'] = risk_score_rounded
    
    return jsonify(decision)

if __name__ == '__main__':
    app.run(port=5000, debug=True)