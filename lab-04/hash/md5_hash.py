# md5_hash.py

def left_rotate(value, shift):
    return ((value << shift) | (value >> (32 - shift))) & 0xFFFFFFFF

def md5(message):
    # Khởi tạo các biến ban đầu
    a = 0x67452301
    b = 0xEFCDAB89
    c = 0x98BADCFE
    d = 0x10325476

    # Tiền xử lý chuỗi văn bản
    original_length = len(message)
    message += b'\x80'
    while (len(message) % 64) != 56:
        message += b'\x00'
    message += original_length.to_bytes(8, 'little')

    # Chia chuỗi thành các block 512-bit
    for i in range(0, len(message), 64):
        block = message[i:i+64]
        words = [int.from_bytes(block[j:j+4], 'little') for j in range(0, 64, 4)]

        a0, b0, c0, d0 = a, b, c, d

        # Vòng lặp chính của thuật toán MD5
        for j in range(64):
            if j < 16:
                f = (b & c) | ((~b) & d)
                g = j
            elif j < 32:
                f = (d & b) | ((~d) & c)
                g = (5*j + 1) % 16
            elif j < 48:
                f = (b & d) | (c & (~d))
                g = (3*j + 5) % 16
            else: # j >= 48
                f = c ^ (b | (~d))
                g = (7*j) % 16

            # (Phần còn lại của logic vòng lặp sẽ ở trang tiếp theo, dựa trên hình ảnh)
            # Dưới đây là phần code bổ sung từ hình ảnh thứ hai của md5_hash.py
            # Nó thiếu một số hằng số T[i] và các bước phức tạp khác của MD5.
            # Tôi sẽ viết lại theo những gì tôi thấy trên hình ảnh của bạn.

            temp = d
            d = c
            c = b
            b = left_rotate((a + f + 0x5A827999 + words[g]) & 0xFFFFFFFF, 3) # Ví dụ, số 0x5A827999 là hằng số T[j]
            a = temp

        a = (a + a0) & 0xFFFFFFFF
        b = (b + b0) & 0xFFFFFFFF
        c = (c + c0) & 0xFFFFFFFF
        d = (d + d0) & 0xFFFFFFFF

    return '{:08x}{:08x}{:08x}{:08x}'.format(a, b, c, d)

# Phần sử dụng hàm MD5 (từ hình ảnh):
input_string = input("Nhập chuỗi cần băm: ")
md5_hash = md5(input_string.encode('utf-8'))
print(f"Mã băm MD5 của chuỗi '{input_string}' là: {md5_hash}")