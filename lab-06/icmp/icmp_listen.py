from scapy.all import *  # Nhập tất cả các hàm và lớp từ thư viện scapy để xử lý gói tin mạng

# Hàm xử lý callback khi bắt được gói tin
def packet_callback(packet):
    # Kiểm tra xem gói tin có lớp ICMP (Internet Control Message Protocol) hay không
    if packet.haslayer(ICMP):
        icmp_packet = packet[ICMP]  # Lấy lớp ICMP từ gói tin

        # In thông tin gói tin ICMP
        print("ICMP Packet Information:")
        print(f"Source IP: {packet[IP].src}")          # Địa chỉ IP nguồn
        print(f"Destination IP: {packet[IP].dst}")     # Địa chỉ IP đích
        print(f"Type: {icmp_packet.type}")             # Loại gói ICMP (Echo Request = 8, Echo Reply = 0, ...)
        print(f"Code: {icmp_packet.code}")             # Mã code bổ sung của ICMP
        print(f"ID: {icmp_packet.id}")                 # ID của gói ICMP

        print(f"Sequence: {icmp_packet.seq}")          # Số thứ tự (dùng để theo dõi phản hồi ICMP)
        print(f"Load: {icmp_packet.load}")             # Dữ liệu đi kèm (nội dung payload của ICMP nếu có)
        print("=" * 30)                                # In dòng phân cách
        

# Hàm main để bắt đầu chương trình giám sát ICMP
def main():
    # Bắt gói tin ICMP, mỗi gói nhận được sẽ gọi hàm packet_callback, không lưu lại gói (store=0 để tiết kiệm RAM)
    sniff(prn=packet_callback, filter="icmp", store=0)

# Điều kiện để chạy chương trình chính
if __name__ == '__main__':
    main()
