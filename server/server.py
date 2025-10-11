import socket
import threading
import paramiko
from config import HOST, PORT, PASSWORD
from server.client_registry import ClientRegistry
from server.client_session import ClientSession

class ChatServer:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.registry = ClientRegistry()
        self.host_key = paramiko.RSAKey.generate(2048)
        self.socket = None

    def handle_client(self, conn, addr):
        session = ClientSession(conn, addr, self.host_key, self.registry)
        session.start()

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(100)
        print(f"SSH Chat server running on {self.host}:{self.port}")
        print(f"Connect with: ssh -p {self.port} <username>@localhost (password: {PASSWORD})")
        
        try:
            while True:
                conn, addr = self.socket.accept()
                print(f"New connection from {addr}")
                thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                thread.daemon = True
                thread.start()
        except KeyboardInterrupt:
            print("\nShutting down server...")
        finally:
            if self.socket:
                self.socket.close()
