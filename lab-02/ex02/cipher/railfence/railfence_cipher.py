class RailFenceCipher:
    def __init__(self):
        pass

    def rail_fence_encrypt(self, plain_text, num_rails):
        # Khởi tạo các "đường ray"
        # Mỗi đường ray là một danh sách để chứa các ký tự
        rails = [[] for _ in range(num_rails)]
        rail_index = 0
        direction = 1  # 1: xuống, -1: lên

        for char in plain_text:
            rails[rail_index].append(char)

            # Thay đổi hướng khi chạm đến đường ray trên cùng hoặc dưới cùng
            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1

            # Di chuyển đến đường ray tiếp theo
            rail_index += direction

        # Ghép các ký tự từ các đường ray để tạo ra văn bản đã mã hóa
        cipher_text = ''.join(''.join(rail) for rail in rails)
        return cipher_text

    def rail_fence_decrypt(self, cipher_text, num_rails):
        # Tạo cấu trúc để theo dõi độ dài của mỗi đường ray
        # rail_lengths = [0] * num_rails  <-- Chỉnh sửa từ ảnh 1, hình như thiếu `* num_rails`
        rail_lengths = [0] * num_rails # Đảm bảo mảng có số phần tử bằng num_rails

        rail_index = 0
        direction = 1

        # Xác định độ dài của mỗi "đường ray" trong văn bản đã mã hóa
        for _ in range(len(cipher_text)):
            rail_lengths[rail_index] += 1

            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1

            rail_index += direction

        # Tạo lại cấu trúc đường ray ban đầu với các vị trí trống
        rails = []
        start = 0
        for length in rail_lengths:
            # Gán lại các phần của văn bản đã mã hóa vào các đường ray
            rails.append(list(cipher_text[start:start + length]))
            start += length

        # Bắt đầu quá trình giải mã
        plain_text = ""
        rail_index = 0
        direction = 1

        for _ in range(len(cipher_text)):
            # Lấy ký tự từ đường ray tương ứng
            plain_text += rails[rail_index][0]
            # Xóa ký tự đã lấy khỏi đường ray
            rails[rail_index] = rails[rail_index][1:]

            # Điều chỉnh hướng di chuyển
            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1

            # Di chuyển đến đường ray tiếp theo
            rail_index += direction

        return plain_text