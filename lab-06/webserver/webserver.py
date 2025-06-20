import socket  # Nhập thư viện socket để sử dụng giao tiếp mạng

# Hàm xử lý yêu cầu từ client
def handle_request(client_socket, request_data):
    # Kiểm tra nếu request chứa đường dẫn /admin
    if "GET /admin" in request_data:
        # Tạo phản hồi HTTP trả về nội dung cho trang admin
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nWelcome to the admin page!"
    else:
        # Nếu không phải /admin thì trả về nội dung mặc định
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nHello, this is a simple web server!"
    
    # Gửi phản hồi về cho client
    client_socket.sendall(response.encode('utf-8'))

    # Đóng kết nối với client sau khi gửi xong
    client_socket.close()
        
# Hàm chính để khởi chạy server
def main():
    # Tạo socket TCP sử dụng IPv4
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Gán socket vào địa chỉ IP localhost và cổng 8080
    server_socket.bind(('127.0.0.1', 8080))

    # Lắng nghe tối đa 5 kết nối đang chờ
    server_socket.listen(5)
    
    print("Server listening on port 8080...")  # In ra khi server đã sẵn sàng
    
    # Vòng lặp chờ kết nối từ client
    while True:
        # Chấp nhận kết nối mới từ client
        client_socket, client_address = server_socket.accept()

        # In địa chỉ IP và cổng của client đã kết nối
        print(f"Connection from {client_address}")

        # Nhận dữ liệu từ client (request HTTP)
        request_data = client_socket.recv(1024).decode('utf-8')

        # Gọi hàm xử lý yêu cầu
        handle_request(client_socket, request_data)
        
# Kiểm tra nếu file được chạy trực tiếp thì gọi hàm main
if __name__ == "__main__":
    main()
