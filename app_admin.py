import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from extensions import db, login_manager
from models import User, Transaction, Complaint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'admin_secret_key_123'

# Cấu hình Database dùng chung
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'frade_system.db')

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- ROUTES QUẢN TRỊ CHÍNH ---

@app.route('/admin')
@login_required
def admin_dashboard():
    # Lấy dữ liệu cho Dashboard
    transactions = Transaction.query.all()
    users = User.query.filter_by(is_admin=False).all()
    complaints_count = Complaint.query.filter_by(status='pending').count()
    
    return render_template('admin/dashboard.html', 
                           transactions=transactions, 
                           users=users,
                           users_count=len(users),
                           complaints_count=complaints_count)

# --- QUẢN LÝ GIAO DỊCH (APPROVE/BLOCK) ---

@app.route('/admin/approve/<int:tx_id>')
@login_required
def approve_transaction(tx_id):
    tx = Transaction.query.get_or_404(tx_id)
    if tx.status == 'pending_admin':
        tx.status = 'approved'
        # Cập nhật số dư thực tế khi duyệt
        tx.sender.balance -= tx.amount
        tx.receiver.balance += tx.amount
        db.session.commit()
        flash(f'Giao dịch #{tx_id} đã được phê duyệt.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/block/<int:tx_id>')
@login_required
def block_transaction(tx_id):
    tx = Transaction.query.get_or_404(tx_id)
    if tx.status == 'pending_admin':
        tx.status = 'blocked'
        db.session.commit()
        flash(f'Giao dịch #{tx_id} đã bị chặn.', 'danger')
    return redirect(url_for('admin_dashboard'))

# --- QUẢN LÝ KHIẾU NẠI ---

@app.route('/admin/complaints')
@login_required
def view_complaints():
    # Sử dụng complainant (backref đã sửa trong models.py)
    complaints = Complaint.query.filter_by(status='pending').all()
    return render_template('admin/complaints.html', complaints=complaints)

@app.route('/admin/resolve-complaint/<int:id>/<action>')
@login_required
def resolve_complaint(id, action):
    complaint = Complaint.query.get_or_404(id)
    user = complaint.complainant # Truy cập qua backref mới
    
    if action == 'approve':
        user.is_blocked = False
        # Tạo 1 bản ghi uy tín để reset điểm trung bình về ~7.0
        reset_tx = Transaction(sender_id=user.id, receiver_id=user.id, 
                               amount=0, risk_score=7.0, status='system_reset')
        db.session.add(reset_tx)
        complaint.status = 'resolved'
        flash(f'Đã mở khóa tài khoản {user.username}.', 'success')
    
    elif action == 'ban':
        user.is_blocked = True
        user.user_type = 'banned_hacker'
        complaint.status = 'rejected'
        flash(f'Đã chặn vĩnh viễn hacker {user.username}.', 'danger')
        
    db.session.commit()
    return redirect(url_for('view_complaints'))

# --- DỌN DẸP HỆ THỐNG ---

@app.route('/admin/clear-logs', methods=['POST'])
@login_required
def clear_logs():
    Transaction.query.delete()
    db.session.commit()
    flash('Đã xóa sạch lịch sử giao dịch.', 'warning')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/reset-users', methods=['POST'])
@login_required
def reset_users():
    # Xóa các ràng buộc trước
    Complaint.query.delete()
    Transaction.query.delete()
    # Xóa tất cả trừ Admin
    User.query.filter(User.is_admin == False).delete()
    db.session.commit()
    flash('Hệ thống đã được reset. Toàn bộ người dùng đã bị xóa.', 'danger')
    return redirect(url_for('admin_dashboard'))

# --- AUTH ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username, is_admin=True).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        flash('Đăng nhập Admin thất bại.', 'error')
    return render_template('user/login.html') # Dùng chung template login

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=5001, debug=True)