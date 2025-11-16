# Hướng dẫn Setup Backend

## Bước 1: Cài đặt Python packages

```bash
cd backend
pip install -r requirements.txt
```

## Bước 2: Khởi tạo Database

```bash
python init_db.py
```

Sẽ tạo file `btl.db` với:
- 14 tables
- 3 users mẫu (admin, student, parent)
- 2 daily messages mẫu

## Bước 3: Kiểm tra Database

```bash
python check_db.py
```

## Bước 4: Chạy Server

```bash
python app.py
```

Server sẽ chạy tại: `http://localhost:5000`

## Test API

### Đăng ký user mới
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","password":"password123","role":"student"}'
```

### Đăng nhập
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

## Users mẫu

Sau khi chạy `init_db.py`, có 3 users:
- **Admin**: admin@btl.com / password: (cần set trong code)
- **Student**: student1@example.com / password: (cần set trong code)
- **Parent**: parent1@example.com / password: (cần set trong code)

**Lưu ý**: Passwords trong database đã được hash, cần set password mới qua API register hoặc update code.

