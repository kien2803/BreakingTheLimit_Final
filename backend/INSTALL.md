# Hướng dẫn Cài đặt Backend

## Vấn đề: Python không có pip hoặc Flask chưa được cài

### Giải pháp 1: Cài đặt pip cho Python hiện tại

Nếu Python không có pip, cài đặt pip:

**Windows:**
```bash
python -m ensurepip --upgrade
```

Hoặc download get-pip.py:
```bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

### Giải pháp 2: Sử dụng Python khác (khuyến nghị)

Nếu bạn có nhiều Python installations, hãy dùng Python từ Microsoft Store hoặc python.org:

1. **Kiểm tra Python nào có pip:**
   ```bash
   py -3 --version
   py -3 -m pip --version
   ```

2. **Cài đặt dependencies:**
   ```bash
   py -3 -m pip install Flask Flask-CORS Flask-SQLAlchemy bcrypt Werkzeug python-dotenv requests
   ```

3. **Chạy server:**
   ```bash
   py -3 app.py
   ```

### Giải pháp 3: Tạo Virtual Environment (Tốt nhất)

```bash
# Tạo virtual environment
python -m venv venv

# Kích hoạt (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Kích hoạt (Windows CMD)
venv\Scripts\activate.bat

# Cài đặt dependencies
pip install -r requirements.txt

# Chạy server
python app.py
```

### Giải pháp 4: Dùng Python từ python.org

1. Download Python từ: https://www.python.org/downloads/
2. Khi cài đặt, chọn "Add Python to PATH"
3. Mở terminal mới và chạy:
   ```bash
   pip install Flask Flask-CORS Flask-SQLAlchemy bcrypt Werkzeug python-dotenv requests
   cd backend
   python app.py
   ```

## Kiểm tra Setup

Chạy script kiểm tra:
```bash
python check_setup.py
```

Script sẽ cho biết:
- Python version và path
- Modules nào đã cài, modules nào thiếu
- Database có tồn tại không
- Config files có đầy đủ không

## Sau khi cài đặt xong

1. Khởi tạo database (nếu chưa):
   ```bash
   python init_db.py
   ```

2. Chạy server:
   ```bash
   python app.py
   ```

3. Kiểm tra server:
   - Mở: http://localhost:5000/api/health
   - Nếu thấy JSON response thì thành công!

