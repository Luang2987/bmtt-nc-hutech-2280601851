from block import Block
import hashlib
import time

class Blockchain:
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.create_block(proof=1, previous_hash='0') # Tạo khối Genesis

    def create_block(self, proof, previous_hash):
        block = Block(
            len(self.chain) + 1,
            previous_hash,
            time.time(),
            self.current_transactions,
            proof
        )
        self.current_transactions = [] # Đặt lại danh sách giao dịch hiện tại
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1] # Trả về khối cuối cùng trong chuỗi

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            # Thuật toán băm để tìm bằng chứng
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000': # Kiểm tra xem hash có bắt đầu bằng '0000' không
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def add_transaction(self, sender, receiver, amount):
        self.current_transactions.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })
        return self.get_previous_block().index + 1 # Trả về index của khối sẽ chứa giao dịch này

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            # Kiểm tra hash của khối hiện tại có khớp không
            if block.previous_hash != previous_block.hash:
                return False
            # Kiểm tra bằng chứng công việc có hợp lệ không
            previous_proof = previous_block.proof
            proof = block.proof
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000': # Kiểm tra lại điều kiện '0000'
                return False
            previous_block = block
            block_index += 1
        return True