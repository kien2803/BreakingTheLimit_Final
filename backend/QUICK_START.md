# Quick Start - Backend Server

## Cách chạy server nhanh

### Bước 1: Cài đặt dependencies
```bash
pip install Flask Flask-CORS Flask-SQLAlchemy bcrypt Werkzeug python-dotenv requests
```

Hoặc:
```bash
pip install -r requirements.txt
```

### Bước 2: Khởi tạo database (nếu chưa có)
```bash
python init_db.py
```

### Bước 3: Chạy server

**Windows (PowerShell):**
```powershell
cd backend
python app.py
```

**Windows (Command Prompt):**
```cmd
cd backend
python app.py
```

**Hoặc double-click:** `run_server.bat`

### Bước 4: Kiểm tra server

Mở trình duyệt hoặc dùng curl:
```
http://localhost:5000/api/health
```

Nếu thấy response:
```json
{
  "status": "healthy",
  "database": "connected",
  "tables": 14
}
```

Thì server đã chạy thành công! ✅

## Test API

### Health Check
```
GET http://localhost:5000/api/health
```

### Đăng ký user
```
POST http://localhost:5000/api/auth/register
Content-Type: application/json

{
  "name": "Test User",
  "email": "test@example.com",
  "password": "password123",
  "role": "student"
}
```

### Đăng nhập
```
POST http://localhost:5000/api/auth/login
Content-Type: application/json

{
  "email": "test@example.com",
  "password": "password123"
}
```

## Troubleshooting

### Lỗi: "ModuleNotFoundError: No module named 'flask'"
**Giải pháp:** Cài đặt lại dependencies:
```bash
pip install Flask Flask-CORS Flask-SQLAlchemy bcrypt Werkzeug python-dotenv requests
```

### Lỗi: "Database not found"
**Giải pháp:** Chạy:
```bash
python init_db.py
```

### Port 5000 đã được sử dụng
**Giải pháp:** Đổi port trong `app.py`:
```python
app.run(debug=True, port=5001, host='0.0.0.0')
```

