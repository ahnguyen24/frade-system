# Hệ Thống Phát Hiện Gian Lận Giao Dịch (Fraud Detection System)

Hệ thống mô phỏng giao dịch ngân hàng tích hợp bộ máy phân tích rủi ro dựa trên các yếu tố: Số tiền, Tần suất, Khoảng cách và Thiết bị. Hệ thống hỗ trợ xác thực đa yếu tố (MFA) qua số điện thoại và quản trị viên phê duyệt các giao dịch nghi vấn.

## 🚀 Tính năng chính
* **MFA Security:** Xác thực OTP qua số điện thoại cho các giao dịch rủi ro trung bình.
* **Real-time Detection:** Tự động phân loại giao dịch (Thành công, MFA, Chặn).
* **Admin Panel:** Quản lý người dùng, xem lịch sử giao dịch và phản hồi khiếu nại.
* **Demo Engine:** Cổng mô phỏng 8 kịch bản kiểm thử độc lập (Port 5003).

## 🛠 Yêu cầu hệ thống
* Python 3.8+
* Flask & Flask-SQLAlchemy
* Requests (cho bộ Demo)

## 📦 Hướng dẫn cài đặt

1. **Khởi tạo môi trường ảo (Virtual Environment):**
   ```bash
   python -m venv .venv
   # Kích hoạt trên Windows:
   .venv\Scripts\activate
   # Kích hoạt trên macOS/Linux:
   source .venv/bin/activate
   ```

2. **Cài đặt các thư viện cần thiết:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Khởi tạo cơ sở dữ liệu:**
   ```bash
   python init_db.py
   ```

## 🖥 Hướng dẫn chạy Project

Để hệ thống hoạt động đầy đủ tính năng, bạn nên mở 3 Terminal riêng biệt và chạy các lệnh sau theo thứ tự:

### Bước 1: Chạy User App (Cổng 5002)
Đây là giao diện dành cho khách hàng thực hiện chuyển tiền và xác thực MFA.
```bash
python app_user.py
```
### Bước 2: Chạy Admin App (Cổng 5001)
Đây là giao diện dành cho quản trị viên quản lý người dùng, xem lịch sử giao dịch và xử lý khiếu nại.
```bash
python app_admin.py
```
### Bước 3: Chạy Demo Engine (Cổng 5003)
Đây là cổng mô phỏng 8 kịch bản kiểm thử độc lập, giúp bạn kiểm tra hệ thống với các tình huống khác nhau.
```bash
python app_demo.py
```
### Bước 4: Truy cập giao diện
* **User App:** Mở trình duyệt và truy cập `http://localhost:5002` để đăng ký và thực hiện giao dịch.
* **Admin App:** Mở trình duyệt và truy cập `http://localhost:5001` để quản lý hệ thống.
* **Demo Engine:** Mở trình duyệt và truy cập `http://localhost:5003` để chạy các kịch bản kiểm thử.

## 🧪 Kịch bản kiểm thử
1. **Giao dịch bình thường:** Chuyển tiền 100 USD từ tài khoản A sang B.
## 🧪 Kịch bản Kiểm thử (8 Case Studies)

Hệ thống cung cấp 8 kịch bản mô phỏng các tình huống giao dịch từ bình thường đến nguy hiểm. Bạn có thể thực thi nhanh tại cổng **5003**:

| STT | Tên Case Study | Thông số mô phỏng (Payload) | Trạng thái hệ thống |
| :-- | :--- | :--- | :--- |
| **01** | **Giao dịch hợp lệ** | `amt: 100`, `freq: 1`, `dist: 0.5` | ✅ **Approved** (Thành công) |
| **02** | **Tần suất cao** | `amt: 50`, `freq: 12`, `dist: 1.0` | ⚠️ **Warning** (Yêu cầu MFA) |
| **03** | **Số tiền lớn** | `amt: 15000`, `freq: 1`, `dist: 2.5` | ❌ **Danger** (Bị chặn ngay) |
| **04** | **Vị trí bất thường** | `amt: 200`, `dist: 800`, `is_new: true` | ⚠️ **Warning** (Yêu cầu MFA) |
| **05** | **Giao dịch nhỏ** | `amt: 20`, `freq: 2`, `dist: 0.1` | ✅ **Approved** (Thành công) |
| **06** | **Thiết bị mới + Tiền lớn** | `amt: 8000`, `dist: 505`, `is_new: true` | ❌ **Danger** (Bị chặn ngay) |
| **07** | **Nghi vấn (MFA)** | `amt: 1200`, `freq: 8`, `dist: 10` | ⚠️ **Warning** (Yêu cầu MFA) |
| **08** | **Tấn công vét cạn** | `amt: 99999`, `freq: 50`, `is_new: true` | ❌ **Danger** (Bị chặn ngay) |

---

## 📝 Quy trình Kiểm tra & Đối chiếu kết quả

Để kiểm chứng tính đồng bộ của hệ thống, bạn có thể thực hiện theo các bước sau:

1. **Thực thi Demo (Port 5003):** - Truy cập `http://127.0.0.1:5003`.
   - Click vào một Case bất kỳ (VD: Case 3). Quan sát thông báo: *"❌ CASE 3: BỊ CHẶN! (Score: 7.5)"*.
2. **Kiểm tra phía Admin (Port 5001):**
   - Đăng nhập tài khoản `admin` / `admin123`.
   - Vào mục **Transaction Logs**, bạn sẽ thấy giao dịch Case 3 đã được lưu vào DB với trạng thái `blocked`.
3. **Kiểm tra phía Người dùng (Port 5002):**
   - Đăng nhập tài khoản `user` / `123`.
   - Kiểm tra **Số dư (Balance)**: Nếu giao dịch Thành công, số dư sẽ giảm. Nếu bị Chặn/MFA, số dư sẽ giữ nguyên cho đến khi được xác thực.

## 📂 Cấu trúc thư mục dự án

```text
frade-system/
├── app_admin.py        # Quản lý giao diện & logic Admin (Port 5001)
├── app_user.py         # Quản lý giao diện & logic Người dùng (Port 5002)
├── app_demo.py         # Engine chạy 8 kịch bản giả lập (Port 5003)
├── models.py           # Khai báo cấu trúc bảng (User, Transaction, Complaint)
├── extensions.py       # Khởi tạo SQLAlchemy chung
├── init_db.py          # Script khởi tạo Database và dữ liệu mẫu
├── frade_system.db     # Cơ sở dữ liệu SQLite (Tự động tạo)
├── requirements.txt    # Danh sách thư viện cần cài đặt
└── templates/          # Chứa các file giao diện HTML
    ├── admin/          # Giao diện Admin
    ├── user/           # Giao diện User
    └── demo/           # Giao diện Demo Portal
```


