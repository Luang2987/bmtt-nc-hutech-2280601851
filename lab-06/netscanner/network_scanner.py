import requests               # Thư viện để gọi HTTP request (lấy thông tin vendor từ API)
import socket                 # Dùng để lấy địa chỉ IP cục bộ của máy
from scapy.all import ARP, Ether, srp  # Scapy dùng để tạo gói ARP, Ether và gửi nhận gói

# Hàm lấy IP nội bộ của máy tính hiện tại
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Kết nối tạm thời đến 8.8.8.8 (Google DNS) để xác định IP nội bộ
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]  # Trả về IP cục bộ
    finally:
        s.close()

# Hàm tra cứu nhà sản xuất thiết bị từ địa chỉ MAC
def get_vendor_by_mac(mac):
    try:
        # Gọi API công khai để tra vendor từ địa chỉ MAC
        response = requests.get(f"https://api.macvendors.com/{mac}")
        if response.status_code == 200:
            return response.text  # Trả về tên nhà sản xuất
        else:
            return "Unknown Vendor"
    except Exception as e:
        print("Error fetching vendor:", e)
        return "Unknown Vendor"

# Hàm quét tất cả thiết bị trong mạng con
def local_network_scan(ip_range):
    arp = ARP(pdst=ip_range)                   # Gói ARP gửi đến dải IP
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")     # Gói Ethernet phát sóng (broadcast)
    packet = ether / arp                       # Tạo gói ARP trong khung Ethernet

    # Gửi gói đi và chờ phản hồi (timeout 3 giây), không hiển thị log (verbose=0)
    result = srp(packet, timeout=3, verbose=0)[0]

    devices = []  # Danh sách thiết bị thu thập được
    for sent, received in result:
        devices.append({
            'ip': received.psrc,                # IP của thiết bị phản hồi
            'mac': received.hwsrc,              # MAC của thiết bị phản hồi
            'vendor': get_vendor_by_mac(received.hwsrc)  # Tra nhà sản xuất
        })
    return devices

# Hàm chính của chương trình
def main():
    local_ip = get_local_ip()
    # Xây dựng subnet từ IP: ví dụ 192.168.1.45 -> 192.168.1.1/24
    subnet = ".".join(local_ip.split('.')[:3]) + ".1/24"
    print(f"Scanning subnet: {subnet}")

    # Bắt đầu quét
    devices = local_network_scan(subnet)

    print("\nDevices found in the network:")
    if devices:
        for device in devices:
            print(f"IP: {device['ip']}, MAC: {device['mac']}, Vendor: {device['vendor']}")
    else:
        print("No devices found.")

# Điểm bắt đầu chương trình
if __name__ == '__main__':
    main()
