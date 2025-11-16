# Sửa lỗi: Server không chạy được

## Vấn đề hiện tại

Python từ `C:\msys64\ucrt64\bin\python.exe` **không có pip** và **chưa cài Flask**.

## Giải pháp nhanh

### Cách 1: Cài đặt pip trước (Thử cách này trước)

**Windows PowerShell:**
```powershell
cd backend
python -m ensurepip --upgrade
python -m pip install Flask Flask-CORS Flask-SQLAlchemy bcrypt Werkzeug python-dotenv requests
```

**Hoặc dùng script:**
```powershell
.\install_dependencies.ps1
```

**Windows CMD:**
```cmd
cd backend
install_dependencies.bat
```

### Cách 2: Dùng Python khác (Nếu cách 1 không được)

Nếu Python hiện tại không có pip, hãy dùng Python từ Microsoft Store hoặc python.org:

1. **Kiểm tra Python nào có pip:**
   ```bash
   py -3 -m pip --version
   ```

2. **Nếu có, cài đặt:**
   ```bash
   py -3 -m pip install Flask Flask-CORS Flask-SQLAlchemy bcrypt Werkzeug python-dotenv requests
   ```

3. **Chạy server:**
   ```bash
   py -3 app.py
   ```

### Cách 3: Tạo Virtual Environment (Khuyến nghị)

```bash
# Tạo venv
python -m venv venv

# Kích hoạt (PowerShell)
.\venv\Scripts\Activate.ps1

# Kích hoạt (CMD)  
venv\Scripts\activate.bat

# Cài đặt
pip install Flask Flask-CORS Flask-SQLAlchemy bcrypt Werkzeug python-dotenv requests

# Chạy server
python app.py
```

## Kiểm tra sau khi cài đặt

Chạy:
```bash
python check_setup.py
```

Nếu thấy tất cả modules là `[OK]`, thì có thể chạy server:
```bash
python app.py
```

## Nếu vẫn không được

1. **Download Python mới từ:** https://www.python.org/downloads/
2. Khi cài đặt, **chọn "Add Python to PATH"**
3. Mở terminal mới và chạy lại các lệnh cài đặt

## Test server

Sau khi server chạy, mở trình duyệt:
- http://localhost:5000/api/health

Nếu thấy JSON response thì thành công!

