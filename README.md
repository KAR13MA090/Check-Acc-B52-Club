# Hướng Dẫn Chạy Tool Check Tài Khoản B52 Club

Tài liệu này hướng dẫn bạn cách cài đặt và sử dụng script check tài khoản B52 Club.

## 1. Yêu cầu hệ thống
*   **Python**: Đã cài đặt phiên bản 3.10 trở lên.
*   **Thư viện**: `requests` (Đã được cài đặt sẵn trên máy).

## 2. Chuẩn bị danh sách tài khoản
Tạo một file `.txt` (ví dụ: `accounts.txt`) chứa danh sách tài khoản theo định dạng:
```text
user1:pass1
user2:pass2
user3:pass3
```

## 3. Cách chạy Script

### Cách 1: Chạy bằng lệnh (Khuyên dùng)
1. Mở **PowerShell** hoặc **CMD**.
2. Copy và dán lệnh sau:
   ```powershell
   py "C:\Users\Administrator\Downloads\check tai khoan b52 club.py"
   ```
3. Nhấn **Enter**.

### Cách 2: Chạy bằng cách kéo thả
1. Tìm file `b52club_fixed.py` trong thư mục Downloads.
2. Chuột phải vào file và chọn **Open with** -> **Python**.

## 4. Cách sử dụng trong Tool
1. Khi script chạy, nó sẽ cố gắng mở một hộp thoại để bạn chọn file tài khoản (`.txt`).
2. Nếu hộp thoại không hiện lên (do lỗi hệ thống), script sẽ yêu cầu bạn nhập tên file trực tiếp vào màn hình đen. Bạn chỉ cần gõ `accounts.txt` (hoặc tên file bạn đã đặt) và nhấn **Enter**.
3. Chờ script chạy xong. Kết quả tài khoản sống sẽ được lưu vào file `live.txt` cùng thư mục.

---
