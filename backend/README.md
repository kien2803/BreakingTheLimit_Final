# Breaking The Limits - Backend API

## Cài đặt

### 1. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 2. Khởi tạo database
```bash
python init_db.py
```

### 3. Chạy server
```bash
python app.py
```

Server sẽ chạy tại: `http://localhost:5000`

## API Endpoints

### Authentication (`/api/auth`)
- `POST /api/auth/register` - Đăng ký user mới
- `POST /api/auth/login` - Đăng nhập
- `GET /api/auth/me` - Lấy thông tin user hiện tại
- `POST /api/auth/logout` - Đăng xuất
- `POST /api/auth/change-password` - Đổi mật khẩu

### Journal (`/api/journal`)
- `POST /api/journal` - Tạo nhật ký mới
- `GET /api/journal` - Lấy danh sách nhật ký
- `GET /api/journal/<id>` - Lấy nhật ký cụ thể
- `PUT /api/journal/<id>` - Cập nhật nhật ký
- `DELETE /api/journal/<id>` - Xóa nhật ký
- `GET /api/journal/stats` - Thống kê nhật ký

### AI Analysis (`/api/ai`)
- `POST /api/ai/analyze` - Phân tích cảm xúc

### Family (`/api/family`)
- `POST /api/family/link` - Kết nối phụ huynh - học sinh
- `GET /api/family/children` - Lấy danh sách con
- `GET /api/family/child/<id>/summary` - Tổng quan cảm xúc của con
- `POST /api/family/encourage` - Gửi tin nhắn động viên
- `PUT /api/family/privacy` - Cập nhật cài đặt riêng tư

### Admin (`/api/admin`)
- `GET /api/admin/users` - Lấy danh sách users
- `GET /api/admin/users/<id>` - Lấy thông tin user
- `PUT /api/admin/users/<id>` - Cập nhật user
- `DELETE /api/admin/users/<id>` - Xóa user
- `GET /api/admin/messages` - Lấy danh sách thông điệp
- `POST /api/admin/messages` - Tạo thông điệp mới
- `GET /api/admin/stats` - Thống kê hệ thống

### Activities (`/api/activities`)
- `GET /api/activities/message/today` - Lấy thông điệp hôm nay

## Database

Database SQLite được lưu tại: `backend/btl.db`

### Kiểm tra database
```bash
python check_db.py
```

## Models

- **User**: Người dùng (student, parent, admin)
- **Journal**: Nhật ký cảm xúc
- **DailyMessage**: Thông điệp hàng ngày
- **PrivacySettings**: Cài đặt riêng tư

## Security

- Passwords được hash bằng bcrypt
- Authentication qua token (cần implement JWT trong production)

