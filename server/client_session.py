import paramiko
from server.ssh_auth import SSHAuthHandler
from server.input_buffer import InputBuffer

class ClientSession:
    def __init__(self, conn, addr, host_key, registry):
        self.conn = conn
        self.addr = addr
        self.host_key = host_key
        self.registry = registry
        self.transport = None
        self.channel = None
        self.username = None
        self.input_buffer = None
        self.char_handlers = {
            '\r': self._handle_newline,
            '\n': self._handle_newline,
            '\x7f': self._handle_backspace,
            '\x08': self._handle_backspace,
        }

    def setup_ssh(self):
        self.transport = paramiko.Transport(self.conn)
        self.transport.add_server_key(self.host_key)
        auth_handler = SSHAuthHandler()
        self.transport.set_subsystem_handler('sftp', paramiko.SFTPServer)
        self.transport.start_server(server=auth_handler)
        self.channel = self.transport.accept(20)
        if self.channel:
            self.username = auth_handler.username
            self.input_buffer = InputBuffer(self.channel)
        return self.channel is not None

    def send_welcome(self):
        welcome_msg = f"Welcome to SSH Chat, {self.username}!\r\n"
        self.channel.send(welcome_msg.encode())
        self.input_buffer.show_prompt()

    def process_character(self, char):
        handler = self.char_handlers.get(char)
        if handler:
            handler()
            return
        if char.isprintable():
            self._handle_printable(char)

    def _handle_newline(self):
        message = self.input_buffer.get_and_clear()
        if message:
            self.registry.broadcast(message, self.username)

    def _handle_backspace(self):
        if self.input_buffer:
            self.input_buffer.remove_char()

    def _handle_printable(self, char):
        if self.input_buffer:
            self.input_buffer.add_char(char)

    def run_chat_loop(self):
        while True:
            data = self.channel.recv(1024)
            if not data:
                break
            
            text = data.decode('utf-8', errors='ignore')
            for char in text:
                self.process_character(char)

    def cleanup(self):
        self.registry.remove_client(self.channel, self.username)
        for resource in (self.channel, self.transport, self.conn):
            self._safe_close(resource)

    def start(self):
        try:
            if not self.setup_ssh():
                print(f"Failed to get channel from {self.addr}")
                return
            
            if not self.registry.add_client(self.channel, self.username, self.input_buffer):
                self.channel.send(b"user already exists\r\n")
                self.cleanup()
                return
            
            self.send_welcome()
            self.run_chat_loop()
            
        except Exception as e:
            print(f"Error handling client {self.addr}: {e}")
        finally:
            self.cleanup()

    def _safe_close(self, resource):
        if not resource:
            return
        try:
            resource.close()
        except Exception:
            pass
