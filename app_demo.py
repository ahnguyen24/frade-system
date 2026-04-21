import os
from flask import Flask, render_template, jsonify
from extensions import db
from models import User, Transaction

app = Flask(__name__)
app.config['SECRET_KEY'] = 'demo_secret_key_final_v3'

# Cấu hình Database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'frade_system.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# --- LOGIC DETECTOR ĐÃ FIX LỖI NGƯỠNG ĐIỂM ---
class SimpleDetector:
    def predict_risk(self, features):
        amt, freq, dist, is_new = features
        score = 0.0
        
        # 1. Xét Số tiền (Amount)
        if amt >= 15000: 
            score += 7.5  # Case 3: Chạm ngưỡng Blocked ngay lập tức
        elif amt >= 8000: 
            score += 4.0  # Case 6
        elif amt >= 1000: 
            score += 1.5  # Case 7
            
        # 2. Xét Tần suất (Frequency)
        if freq >= 50: 
            score += 8.0  # Case 8: Brute Force
        elif freq >= 12: 
            score += 4.5  # Case 2: Chạm ngưỡng MFA ngay lập tức
        elif freq >= 6: 
            score += 3.0  # Case 7
            
        # 3. Xét Khoảng cách & Thiết bị mới
        if dist >= 500: 
            score += 3.5  # Case 4, 6
        if is_new == 1: 
            score += 2.0  # Case 4, 6
            
        return round(min(float(score), 10.0), 2)

detector = SimpleDetector()

# --- DANH SÁCH 8 CASE STUDY ---
CASE_STUDIES = [
    {"id": 1, "type": "Normal", "desc": "Giao dịch hợp lệ", "amt": 100, "freq": 1, "dist": 0.5, "is_new": 0},
    {"id": 2, "type": "Warning", "desc": "Tần suất giao dịch cao", "amt": 50, "freq": 12, "dist": 1.0, "is_new": 0},
    {"id": 3, "type": "Danger", "desc": "Số tiền giao dịch lớn", "amt": 15000, "freq": 1, "dist": 2.5, "is_new": 0},
    {"id": 4, "type": "Warning", "desc": "Vị trí địa lý bất thường", "amt": 200, "freq": 1, "dist": 800, "is_new": 1},
    {"id": 5, "type": "Normal", "desc": "Giao dịch giá trị nhỏ", "amt": 20, "freq": 2, "dist": 0.1, "is_new": 0},
    {"id": 6, "type": "Danger", "desc": "Thiết bị mới + Số tiền lớn", "amt": 8000, "freq": 1, "dist": 505, "is_new": 1},
    {"id": 7, "type": "Warning", "desc": "Giao dịch nghi vấn (MFA)", "amt": 1200, "freq": 8, "dist": 10, "is_new": 0},
    {"id": 8, "type": "Danger", "desc": "Tấn công vét cạn (Brute Force)", "amt": 99999, "freq": 50, "dist": 0, "is_new": 1},
]

@app.route('/')
def index():
    return render_template('demo/index.html', cases=CASE_STUDIES)

@app.route('/execute/<int:case_id>')
def execute_case(case_id):
    case = next((c for c in CASE_STUDIES if c['id'] == case_id), None)
    if not case: return jsonify({"status": "error", "msg": "Không tìm thấy case"}), 404

    sender = User.query.filter_by(username='user').first()
    receiver = User.query.filter_by(username='des').first()

    if not sender or not receiver:
        return jsonify({"status": "error", "msg": "Chưa có user 'user' hoặc 'des' trong DB!"}), 400

    # Chấm điểm
    features = [case['amt'], case['freq'], case['dist'], case['is_new']]
    risk_score = detector.predict_risk(features)

    # Khởi tạo giao dịch
    new_tx = Transaction(sender_id=sender.id, receiver_id=receiver.id, 
                         amount=case['amt'], risk_score=risk_score)

    # PHÂN LOẠI CHÍNH XÁC THEO ĐIỂM
    if risk_score >= 7.0:
        new_tx.status = 'blocked'
        res = {"status": "blocked", "msg": f"❌ CASE {case_id}: BỊ CHẶN! (Score: {risk_score})", "color": "danger"}
    elif risk_score >= 4.0:
        new_tx.status = 'pending_mfa'
        res = {"status": "mfa", "msg": f"⚠️ CASE {case_id}: CẦN XÁC THỰC MFA! (Score: {risk_score})", "color": "warning"}
    else:
        new_tx.status = 'approved'
        sender.balance -= case['amt']
        receiver.balance += case['amt']
        res = {"status": "success", "msg": f"✅ CASE {case_id}: THÀNH CÔNG! (Score: {risk_score})", "color": "success"}

    db.session.add(new_tx)
    db.session.commit()
    return jsonify(res)

if __name__ == '__main__':
    app.run(port=5003, debug=True)