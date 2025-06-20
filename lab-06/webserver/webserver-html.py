import socket  # Nhập thư viện socket để tạo kết nối mạng cơ bản

# Hàm xử lý yêu cầu từ client
def handle_request(client_socket, request_data):
    # Kiểm tra xem client có yêu cầu truy cập /admin không
    if "GET /admin" in request_data:
        # Nếu có, tạo phản hồi HTTP với nội dung của file admin.html
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
        with open('admin.html', 'r') as file:
            response += file.read()
    else:
        # Nếu không phải /admin, trả về nội dung file index.html
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"  # <-- Sửa lỗi: ban đầu bạn ghi là HTTP?1.1
        with open('index.html', 'r') as file:
            response += file.read()
    
    # Gửi phản hồi HTTP về cho client
    client_socket.sendall(response.encode('utf-8'))
    # Đóng kết nối với client sau khi xử lý xong
    client_socket.close()

# Hàm main để khởi động server
def main():
    # Tạo socket TCP sử dụng IPv4
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Gán socket vào địa chỉ localhost và cổng 8080
    server_socket.bind(('127.0.0.1', 8080))

    # Lắng nghe tối đa 5 kết nối đang chờ
    server_socket.listen(5)
    print("Server listening on port 8080...")  # Thông báo server đang hoạt động

    # Vòng lặp vô hạn để nhận và xử lý nhiều kết nối từ client
    while True:
        # Chấp nhận kết nối mới từ client
        client_socket, client_address = server_socket.accept()

        # Hiển thị địa chỉ client đã kết nối
        print(f"Connection from {client_address}")

        # Nhận dữ liệu (request) từ client (tối đa 1024 byte)
        request_data = client_socket.recv(1024).decode('utf-8')

        # Gọi hàm xử lý request
        handle_request(client_socket, request_data)

# Kiểm tra nếu đây là file chính được chạy thì gọi hàm main
if __name__ == "__main__":
    main()
