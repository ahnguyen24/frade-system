import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from extensions import db, login_manager
from models import User, Transaction, Complaint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'user_secret_key_456'

# Cấu hình Database dùng chung với Admin
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'frade_system.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- BỘ MÁY PHÁT HIỆN RỦI RO (MÔ PHỎNG AI) ---
class SimpleDetector:
    def predict_risk(self, features):
        amt, freq, dist, is_new = features
        score = 0.0
        # Logic chấm điểm dựa trên các tham số truyền vào
        if amt > 10000: score += 5.0
        if freq > 10: score += 4.0
        if dist > 500: score += 3.5
        if is_new == 1: score += 2.0
        
        # Giới hạn điểm từ 0.0 đến 10.0
        return round(min(float(score), 10.0), 2)

detector = SimpleDetector()

# --- ROUTES ---

@app.route('/')
@login_required
def user_dashboard():
    return render_template('user/dashboard.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Tên đăng nhập đã tồn tại!', 'danger')
            return redirect(url_for('register'))
        
        new_user = User(username=username, balance=5000.0) # Tặng 5000$ khi đăng ký
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Đăng ký thành công! Hãy đăng nhập.', 'success')
        return redirect(url_for('login'))
    return render_template('user/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Chỉ cho phép User thường đăng nhập ở đây, không cho Admin
        user = User.query.filter_by(username=username, is_admin=False).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('user_dashboard'))
        flash('Sai tài khoản hoặc mật khẩu.', 'danger')
    return render_template('user/login.html')

@app.route('/transfer', methods=['POST'])
@login_required
def transfer():
    if current_user.is_blocked:
        flash('Tài khoản đã bị khóa. Không thể thực hiện giao dịch.', 'danger')
        return redirect(url_for('user_dashboard'))

    receiver_name = request.form.get('receiver')
    amount = float(request.form.get('amount', 0))
    password_confirm = request.form.get('password_confirm')
    is_test_case = request.form.get('is_test_case') == 'true'
    case_id = request.form.get('case_id', 'Manual')

    # KIỂM TRA BẢO MẬT: Bỏ qua mật khẩu nếu là Testcase
    if not is_test_case:
        if not current_user.check_password(password_confirm):
            flash('Mật khẩu xác nhận không chính xác!', 'danger')
            return redirect(url_for('user_dashboard'))

    # KIỂM TRA NGƯỜI NHẬN & SỐ DƯ
    receiver = User.query.filter_by(username=receiver_name).first()
    if not receiver:
        flash(f'Lỗi: Người nhận "{receiver_name}" không tồn tại.', 'warning')
        return redirect(url_for('user_dashboard'))
    
    if current_user.balance < amount:
        flash('Lỗi: Số dư không đủ.', 'warning')
        return redirect(url_for('user_dashboard'))
    risk_score = detector.predict_risk(features)
    
    # Tạo giao dịch tạm thời (status='pending_mfa')
    new_tx = Transaction(
        sender_id=current_user.id,
        receiver_id=receiver.id,
        amount=amount,
        risk_score=risk_score,
        status='pending_mfa' if 4 <= risk_score < 7 else ('blocked' if risk_score >= 7 else 'approved')
    )
    db.session.add(new_tx)
    db.session.commit()

    if new_tx.status == 'pending_mfa':
        # Chuyển hướng sang trang xác thực
        return redirect(url_for('mfa_verify', tx_id=new_tx.id))
    # THU THẬP FEATURES CHO AI
    dist = float(request.form.get('distance', 0.5))
    freq = int(request.form.get('freq', 1))
    is_new = int(request.form.get('is_new_device', 0))
    
    features = [amount, freq, dist, is_new]
    risk_score = detector.predict_risk(features)
    
    new_tx = Transaction(
        sender_id=current_user.id,
        receiver_id=receiver.id,
        amount=amount,
        risk_score=risk_score,
        status='pending'
    )
    
    # PHÂN LOẠI RỦI RO
    if risk_score >= 7.0:
        new_tx.status = 'blocked'
        # Nếu rủi ro quá cao, tự động khóa tài khoản để demo
        current_user.is_blocked = True 
        flash(f'CẢNH BÁO: Case {case_id} bị CHẶN. Tài khoản đã bị tạm khóa do nghi ngờ gian lận!', 'danger')
    elif risk_score >= 4.0:
        new_tx.status = 'pending_admin'
        flash(f'Case {case_id}: Giao dịch đang được Admin kiểm duyệt (Score: {risk_score})', 'info')
    else:
        new_tx.status = 'approved'
        current_user.balance -= amount
        receiver.balance += amount
        flash(f'Case {case_id}: Giao dịch thành công.', 'success')

    db.session.add(new_tx)
    db.session.commit()
    return redirect(url_for('user_dashboard'))
@app.route('/mfa-verify/<int:tx_id>')
@login_required
def mfa_verify(tx_id):
    tx = Transaction.query.get_or_404(tx_id)
    return render_template('user/mfa.html', tx=tx, phone=current_user.phone)

@app.route('/mfa-confirm/<int:tx_id>', methods=['POST'])
@login_required
def mfa_confirm(tx_id):
    tx = Transaction.query.get_or_404(tx_id)
    # Giả lập xác thực thành công
    tx.status = 'approved'
    tx.sender.balance -= tx.amount
    tx.receiver.balance += tx.amount
    db.session.commit()
    flash('Xác thực MFA thành công! Giao dịch đã hoàn tất.', 'success')
    return redirect(url_for('user_dashboard'))
@app.route('/send-complaint', methods=['POST'])
@login_required
def send_complaint():
    reason = request.form.get('reason')
    if reason:
        # Sử dụng backref 'complainant' hoặc 'user_id' tùy model
        new_complaint = Complaint(user_id=current_user.id, reason=reason)
        db.session.add(new_complaint)
        db.session.commit()
        flash('Khiếu nại đã được gửi tới Ban quản trị.', 'info')
    return redirect(url_for('user_dashboard'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Chạy ở port 5002 cho User
    app.run(port=5002, debug=True)