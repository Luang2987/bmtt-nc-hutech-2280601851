import subprocess
from scapy.all import *

# Hàm lấy danh sách các giao diện mạng từ Windows sử dụng lệnh netsh
def get_interfaces():
    result = subprocess.run(['netsh', 'interface', 'show', 'interface'], capture_output=True, text=True)
    output_lines = result.stdout.splitlines()[3:]  # Bỏ 3 dòng đầu tiêu đề
    interfaces = [line.split()[3] for line in output_lines if len(line.split()) >= 4]  # Lấy tên giao diện (cột thứ 4)
    return interfaces

# Hàm xử lý khi bắt được một gói tin
def packet_handler(packet):
    if packet.haslayer(Raw):  # Kiểm tra nếu gói tin có chứa dữ liệu tầng ứng dụng
        print("Captured Packet:")
        print(str(packet))  # In toàn bộ gói tin

# Lấy danh sách các giao diện
interfaces = get_interfaces()

# Hiển thị danh sách cho người dùng lựa chọn
print("Danh sách các giao diện mạng:")
for i, iface in enumerate(interfaces, start=1):
    print(f"{i}. {iface}")

# Nhận lựa chọn từ người dùng
choice = int(input("Chọn giao diện để bắt đầu bắt gói: "))
selected_iface = interfaces[choice - 1]

# Bắt gói tin trên giao diện đã chọn, lọc chỉ bắt gói TCP
sniff(iface=selected_iface, prn=packet_handler, filter="tcp")
