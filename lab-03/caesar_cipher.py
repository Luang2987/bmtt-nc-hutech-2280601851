import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox # Đổi lại thành QMainWindow
import requests

# Đặt đường dẫn cho các plugin nền tảng của Qt
# Giả định thư mục 'platforms' nằm cùng cấp với script này
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = "./platforms" 

# Đảm bảo thư mục hiện tại được thêm vào PYTHONPATH để tìm module ui_caesar
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import class UI từ tệp đã chuyển đổi (pyuic5)
# Dựa vào caesar.ui, tên class chính xác là Ui_MainWindow
from ui_caesar import Ui_MainWindow 


class MyApp(QMainWindow): # Kế thừa từ QMainWindow, khớp với thiết kế UI
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self) 

        # Kết nối các nút với các hàm xử lý sự kiện
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/caesar/encrypt"
        payload = {
            "plain_text": self.ui.txt_plain_text.text(), # Sử dụng .text() cho QLineEdit
            "key": self.ui.txt_key.text()
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_cipher_text.setText(data.get("encrypted_message", "Error: No encrypted_message found in response"))
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Encrypted Successfully")
                msg.exec_()
            else:
                print(f"Error while calling API: Status Code {response.status_code}")
                print(f"Response: {response.text}")
                QMessageBox.warning(self, "API Error", f"Error: {response.status_code}\n{response.text}")

        except requests.exceptions.RequestException as e:
            print("Error: %s" % e.message)
            QMessageBox.critical(self, "Connection Error", f"Could not connect to API: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            QMessageBox.critical(self, "Unexpected Error", f"An unexpected error occurred: {e}")


    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/caesar/decrypt"
        payload = {
            "cipher_text": self.ui.txt_cipher_text.text(), # Sử dụng .text() cho QLineEdit
            "key": self.ui.txt_key.text()
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_plain_text.setText(data.get("decrypted_message", "Error: No decrypted_message found in response"))
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Decrypted Successfully")
                msg.exec_()
            else:
                print(f"Error while calling API: Status Code {response.status_code}")
                print(f"Response: {response.text}")
                QMessageBox.warning(self, "API Error", f"Error: {response.status_code}\n{response.text}")

        except requests.exceptions.RequestException as e:
            print("Error: %s" % e.message)
            QMessageBox.critical(self, "Connection Error", f"Could not connect to API: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            QMessageBox.critical(self, "Unexpected Error", f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())