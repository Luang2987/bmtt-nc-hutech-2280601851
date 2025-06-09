from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import socket
import threading
import hashlib
import sys

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(5)

print("Server is listening on localhost:12345")

server_key = RSA.generate(2048)

clients = []
clients_lock = threading.Lock()

def encrypt_message(key, message):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(message.encode('utf-8'), AES.block_size))
    return cipher.iv + ciphertext

def decrypt_message(key, encrypted_message):
    try:
        iv = encrypted_message[:AES.block_size]
        ciphertext = encrypted_message[AES.block_size:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_message = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return decrypted_message.decode('utf-8')
    except Exception as e:
        print(f"Error decrypting message: {e}")
        return None

def handle_client(client_socket, client_address):
    print(f"Connected with {client_address}")
    current_aes_key = None

    try:
        client_socket.sendall(server_key.publickey().export_key(format='PEM'))

        client_public_key_pem = client_socket.recv(2048)
        if not client_public_key_pem:
            raise Exception("Client disconnected before sending public key.")
        client_received_key = RSA.import_key(client_public_key_pem)

        aes_key = get_random_bytes(16)
        current_aes_key = aes_key

        cipher_rsa = PKCS1_OAEP.new(client_received_key)
        encrypted_aes_key = cipher_rsa.encrypt(aes_key)
        client_socket.sendall(encrypted_aes_key)

        with clients_lock:
            clients.append((client_socket, aes_key))
        print(f"Client {client_address} added to list. Total clients: {len(clients)}")

        while True:
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message:
                print(f"Client {client_address} disconnected.")
                break

            decrypted_message = decrypt_message(aes_key, encrypted_message)
            if decrypted_message is None:
                print(f"Failed to decrypt message from {client_address}. Skipping.")
                continue

            print(f"Received from {client_address}: {decrypted_message}")

            if decrypted_message.strip().lower() == "exit":
                print(f"Client {client_address} sent 'exit' command. Closing connection.")
                break

            message_to_send = f"{client_address[0]}: {decrypted_message}"
            with clients_lock:
                current_clients = list(clients)

            for other_client_socket, other_aes_key in current_clients:
                if other_client_socket != client_socket:
                    try:
                        encrypted_broadcast = encrypt_message(other_aes_key, message_to_send)
                        other_client_socket.sendall(encrypted_broadcast)
                    except Exception as e:
                        print(f"Error sending message to {other_client_socket.getpeername()}: {e}")
                        with clients_lock:
                            if (other_client_socket, other_aes_key) in clients:
                                clients.remove((other_client_socket, other_aes_key))
                                try:
                                    other_client_socket.close()
                                except OSError:
                                    pass
                                print(f"Removed disconnected client {other_client_socket.getpeername()}. Remaining clients: {len(clients)}")

    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
    finally:
        with clients_lock:
            if (client_socket, current_aes_key) in clients:
                clients.remove((client_socket, current_aes_key))
        try:
            client_socket.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        client_socket.close()
        print(f"Connection with {client_address} closed. Remaining clients: {len(clients)}")

def start_server():
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.daemon = True
            client_thread.start()
            print(f"Active threads: {threading.active_count()}")
    except KeyboardInterrupt:
        print("\nServer shutting down gracefully...")
    except Exception as e:
        print(f"Error in server main loop: {e}")
    finally:
        server_socket.close()
        print("Server socket closed.")

if __name__ == "__main__":
    start_server()