# Cách Chạy Backend Server

## Vấn đề: Python từ msys64 không có pip

Python hiện tại (`C:\msys64\ucrt64\bin\python.exe`) là externally-managed environment và không cho phép cài đặt packages trực tiếp.

## Giải pháp: Dùng Python khác

### Bước 1: Tìm Python có pip

Mở PowerShell và chạy:
```powershell
py -3 -m pip --version
```

Nếu thấy version của pip, thì dùng Python đó.

### Bước 2: Cài đặt dependencies

```powershell
py -3 -m pip install Flask Flask-CORS Flask-SQLAlchemy bcrypt Werkzeug python-dotenv requests
```

### Bước 3: Chạy server

```powershell
cd backend
py -3 app.py
```

## Hoặc: Tạo Virtual Environment

Nếu `py -3` không hoạt động, tạo venv:

```powershell
cd backend
python -m venv venv
venv\Scripts\Activate.ps1
pip install Flask Flask-CORS Flask-SQLAlchemy bcrypt Werkzeug python-dotenv requests
python app.py
```

## Hoặc: Download Python mới

1. Download từ: https://www.python.org/downloads/
2. Khi cài, chọn **"Add Python to PATH"**
3. Mở terminal mới
4. Chạy:
   ```bash
   cd backend
   pip install -r requirements.txt
   python app.py
   ```

## Kiểm tra server

Sau khi server chạy, mở trình duyệt:
- http://localhost:5000/api/health

Nếu thấy JSON response thì thành công!

## Lưu ý

- Server cần chạy ở port 5000
- Frontend đang chạy ở port 8000
- Cả 2 cần chạy cùng lúc để web hoạt động đầy đủ

