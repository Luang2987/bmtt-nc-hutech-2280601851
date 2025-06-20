# Import các thư viện cần thiết
from scapy.all import *         # Dùng Scapy để tạo và gửi gói tin mạng thấp
import socket                   # Dùng để phân giải tên miền thành địa chỉ IP

# Danh sách các cổng phổ biến để quét (có thể mở rộng thêm)
COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3389]

# Hàm quét các cổng phổ biến trên target
def scan_common_ports(target_domain, timeout=2):
    open_ports = []                                      # Danh sách lưu các cổng đang mở
    target_ip = socket.gethostbyname(target_domain)      # Phân giải domain thành IP

    # Duyệt qua từng cổng trong danh sách
    for port in COMMON_PORTS:
        # Gửi một gói TCP với cờ SYN đến IP và cổng tương ứng
        response = sr1(IP(dst=target_ip)/TCP(dport=port, flags='S'), timeout=timeout, verbose=0)
        
        # Nếu phản hồi có lớp TCP và cờ là SYN-ACK (flags = 0x12), cổng đang mở
        if response and response.haslayer(TCP) and response[TCP].flags == 0x12:
            open_ports.append(port)  # Thêm cổng vào danh sách mở
            
            # Gửi lại gói RST để đóng kết nối lịch sự (tránh treo kết nối)
            send(IP(dst=target_ip)/TCP(dport=port, flags='R'), verbose=0)

    return open_ports   # Trả về danh sách các cổng mở

# Hàm chính: nhập domain và chạy quét
def main():
    target_domain = input("Enter the target domain or IP address: ")  # Nhập domain hoặc IP
    open_ports = scan_common_ports(target_domain)                     # Thực hiện quét
    
    # Hiển thị kết quả
    if open_ports:
        print("Open common ports:")
        print(open_ports)
    else:
        print("No common ports are open on the target.")

# Gọi hàm main khi chạy trực tiếp file
if __name__ == "__main__":
    main()
