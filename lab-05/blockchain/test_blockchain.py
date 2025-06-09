from blockchain import Blockchain
import datetime # Import thư viện datetime để định dạng thời gian tốt hơn nếu cần

# 1. Khởi tạo Blockchain
my_blockchain = Blockchain()
print("Blockchain đã được khởi tạo.")
print("-" * 40)

# 2. Đào Khối #2 (khối đầu tiên sau khối Genesis)
print("Đang đào Khối #2...")
previous_block = my_blockchain.get_previous_block()
previous_proof = previous_block.proof

# Thêm các giao dịch cho Khối #2 (theo ảnh của bạn)
my_blockchain.add_transaction(sender='Alice', receiver='Bob', amount=10)
my_blockchain.add_transaction(sender='Bob', receiver='Charlie', amount=5)
my_blockchain.add_transaction(sender='Miner', receiver='You', amount=1) # Giao dịch phần thưởng cho thợ đào, khớp với ảnh

# Tìm bằng chứng công việc và tạo Khối #2
proof = my_blockchain.proof_of_work(previous_proof)
new_block = my_blockchain.create_block(proof, previous_block.hash)
print("Khối #2 đã được đào thành công.")
print("-" * 40)

# 3. Đào Khối #3 (khối thứ hai sau khối Genesis, hoặc khối tiếp theo)
# Giao dịch 'Charlie' -> 'Alice' từ ảnh của bạn có thể thuộc khối này
print("Đang đào Khối #3...")
previous_block = my_blockchain.get_previous_block() # Lấy khối vừa tạo (Khối #2)
previous_proof = previous_block.proof

# Thêm giao dịch cho Khối #3 (giao dịch còn lại từ test_blockchain.py ban đầu của bạn)
my_blockchain.add_transaction(sender='Charlie', receiver='Alice', amount=3)

# Tìm bằng chứng công việc và tạo Khối #3
proof = my_blockchain.proof_of_work(previous_proof)
new_block_3 = my_blockchain.create_block(proof, previous_block.hash)
print("Khối #3 đã được đào thành công.")
print("-" * 40)


# 4. In thông tin về chuỗi Blockchain
print("Hiển thị thông tin Blockchain:")
for block in my_blockchain.chain:
    print(f"\nBlock #{block.index}")
    # Định dạng timestamp cho dễ đọc (tùy chọn)
    print(f"Timestamp: {datetime.datetime.fromtimestamp(block.timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}")
    print(f"Transactions: {block.transactions}")
    print(f"Proof: {block.proof}")
    print(f"Previous Hash: {block.previous_hash}")
    print(f"Hash: {block.hash}")
    print("-" * 20)

# 5. Kiểm tra tính hợp lệ của chuỗi
is_valid = my_blockchain.is_chain_valid(my_blockchain.chain)
print(f"\nIs Blockchain Valid: {is_valid}")
