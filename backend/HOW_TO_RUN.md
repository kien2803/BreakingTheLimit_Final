# Cách Chạy Backend Server

## ✅ Đã cài đặt thành công!

Dependencies đã được cài đặt trong virtual environment (`venv`).

## Cách chạy server

### Cách 1: Dùng Python từ venv (Khuyến nghị)

**PowerShell:**
```powershell
cd backend
.\venv\bin\python.exe app.py
```

**Hoặc dùng script:**
```powershell
.\run_with_venv.ps1
```

**Windows CMD:**
```cmd
cd backend
venv\bin\python.exe app.py
```

**Hoặc:**
```cmd
run_with_venv.bat
```

### Cách 2: Activate venv trước

**PowerShell:**
```powershell
cd backend
.\venv\bin\Activate.ps1
python app.py
```

**Windows CMD:**
```cmd
cd backend
venv\bin\activate.bat
python app.py
```

## Kiểm tra server

Sau khi server chạy, bạn sẽ thấy:
```
==================================================
Breaking The Limits Backend Server
==================================================
Server running at: http://localhost:5000
API Health: http://localhost:5000/api/health
Press CTRL+C to stop the server
==================================================
```

Mở trình duyệt:
- http://localhost:5000/api/health

Nếu thấy JSON response thì thành công! ✅

## Lưu ý

- Server chạy ở port **5000**
- Frontend cần chạy ở port **8000**
- Cả 2 cần chạy cùng lúc để web hoạt động đầy đủ

## Nếu gặp lỗi

1. **Lỗi import:** Đảm bảo đang ở trong thư mục `backend`
2. **Lỗi database:** Chạy `python init_db.py` trước
3. **Port đã được sử dụng:** Đổi port trong `app.py` (dòng 102)

