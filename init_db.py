# init_db.py
import os
from extensions import db
from app_admin import app
from models import User

def init_database():
    print("Đang khởi tạo lại database với cột Phone...")
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'frade_system.db')
    
    if os.path.exists(db_path):
        os.remove(db_path) # Xóa file cũ

    with app.app_context():
        db.create_all() # Tạo lại toàn bộ bảng mới
        
        # Tạo Admin
        admin = User(username='admin', phone='000000000', is_admin=True)
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Tạo user demo cho Port 5003
        u_test = User(username='user', phone='0912345678', balance=10000.0)
        u_test.set_password('123')
        db.session.add(u_test)
        
        # Tạo des demo cho Port 5003
        u_des = User(username='des', phone='0987654321', balance=5000.0)
        u_des.set_password('456')
        db.session.add(u_des)

        # Tạo tài khoản tempo
        u_tempo = User(username='tempo', phone='0111222333', balance=1000.0)
        u_tempo.set_password('111')
        db.session.add(u_tempo)
            
        db.session.commit()
        print("Khởi tạo thành công! Đã sẵn sàng Demo.")

if __name__ == '__main__':
    init_database()