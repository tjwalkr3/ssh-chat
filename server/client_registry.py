import threading
from datetime import datetime
from config import COLORS, USERNAME_FIELD_WIDTH

class ClientRegistry:
    def __init__(self):
        self.clients = []
        self.usernames = set()
        self.lock = threading.Lock()
    
    def add_client(self, channel, username, input_buffer):
        with self.lock:
            if username in self.usernames:
                return False
            self.usernames.add(username)
            self.clients.append((channel, username, input_buffer))
            return True
    
    def remove_client(self, channel, username):
        with self.lock:
            self.clients[:] = [(ch, un, ib) for ch, un, ib in self.clients if ch != channel]
            self.usernames.discard(username)
    
    def broadcast(self, message, username):
        timestamp = datetime.now().strftime("%H:%M:%S")
        color = self._get_color(username)
        formatted_msg = f"{timestamp}  \x1b[{color}m{username:>{USERNAME_FIELD_WIDTH}}\x1b[0m  |  {message}\r\n"
        
        with self.lock:
            for client_channel, client_username, input_buffer in self.clients:
                try:
                    if client_username == username:
                        # For the sender, clear their input line, show message, show fresh prompt
                        input_buffer.clear_line()
                        client_channel.send(formatted_msg.encode())
                        input_buffer.show_prompt()
                    else:
                        # For other clients, clear line, show message, redraw with their text
                        input_buffer.clear_line()
                        client_channel.send(formatted_msg.encode())
                        input_buffer.redraw_input_line()
                except:
                    pass
    
    def _get_color(self, username):
        return COLORS[hash(username) % len(COLORS)]
