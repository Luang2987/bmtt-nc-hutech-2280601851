class PlayfairCipher:
    def __init__(self):
        pass

    def create_playfair_matrix(self, key):
        key = key.replace("J", "I")
        key = key.upper()
        key_set = set(key)

        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        remaining_letters = [
            letter for letter in alphabet if letter not in key_set
        ]

        matrix = list(key)

        for letter in remaining_letters:
            matrix.append(letter)
            if len(matrix) == 25:
                break

        playfair_matrix = [matrix[i:i+5] for i in range(0, len(matrix), 5)]
        return playfair_matrix

    def find_letter_coords(self, matrix, letter):
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                if matrix[row][col] == letter:
                    return row, col
        return -1, -1


    def playfair_encrypt(self, plain_text, matrix):
        plain_text = plain_text.replace("J", "I")
        plain_text = plain_text.upper()
        
        processed_plain_text = ""
        i = 0
        while i < len(plain_text):
            processed_plain_text += plain_text[i]
            if i + 1 < len(plain_text):
                if plain_text[i] == plain_text[i+1]:
                    processed_plain_text += "X"
                else:
                    processed_plain_text += plain_text[i+1]
                    i += 1
            i += 1
        
        if len(processed_plain_text) % 2 != 0:
            processed_plain_text += "X"

        encrypted_text = ""

        for i in range(0, len(processed_plain_text), 2):
            pair = processed_plain_text[i:i+2]
            
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            if row1 == row2:
                encrypted_text += matrix[row1][(col1 + 1) % 5]
                encrypted_text += matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:
                encrypted_text += matrix[(row1 + 1) % 5][col1]
                encrypted_text += matrix[(row2 + 1) % 5][col2]
            else:
                encrypted_text += matrix[row1][col2]
                encrypted_text += matrix[row2][col1]
        
        return encrypted_text


    def playfair_decrypt(self, cipher_text, matrix):
        cipher_text = cipher_text.upper()

        decrypted_text = ""

        for i in range(0, len(cipher_text), 2):
            pair = cipher_text[i:i+2]
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            if row1 == row2:
                decrypted_text += matrix[row1][(col1 - 1) % 5]
                decrypted_text += matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:
                decrypted_text += matrix[(row1 - 1) % 5][col1]
                decrypted_text += matrix[(row2 - 1) % 5][col2]
            else:
                decrypted_text += matrix[row1][col2]
                decrypted_text += matrix[row2][col1]
        
        # Phần xử lý để loại bỏ ký tự 'X' được thêm vào
        final_plain_text = ""
        i = 0
        while i < len(decrypted_text):
            if i + 2 < len(decrypted_text) and \
               decrypted_text[i] == decrypted_text[i+2] and \
               decrypted_text[i+1] == 'X':
                final_plain_text += decrypted_text[i]
                i += 2
            else:
                final_plain_text += decrypted_text[i]
                i += 1

        # Logic loại bỏ 'X' cuối cùng từ hình ảnh c3d40d.png
        banro_from_image = ""
        for j in range(0, len(decrypted_text) - 2, 2):
            if decrypted_text[j] == decrypted_text[j+2]:
                banro_from_image += decrypted_text[j]
            else:
                banro_from_image += decrypted_text[j] + decrypted_text[j+1]
        
        if len(decrypted_text) >= 2:
            if decrypted_text[-1] == "X":
                banro_from_image += decrypted_text[-2]
            else:
                banro_from_image += decrypted_text[-2] + decrypted_text[-1]

        return banro_from_image