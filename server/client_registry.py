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
        formatted_msg = self._format_message(username, message)

        with self.lock:
            for client_channel, client_username, input_buffer in self.clients:
                redraw = input_buffer.show_prompt if client_username == username else input_buffer.redraw_input_line
                self._send_formatted_message(client_channel, input_buffer, formatted_msg, redraw)

    def _get_color(self, username):
        return COLORS[hash(username) % len(COLORS)]

    def _format_message(self, username, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        color = self._get_color(username)
        return f"{timestamp}  \x1b[{color}m{username:>{USERNAME_FIELD_WIDTH}}\x1b[0m  |  {message}\r\n"

    def _send_formatted_message(self, client_channel, input_buffer, formatted_msg, redraw_callback):
        try:
            input_buffer.clear_line()
            client_channel.send(formatted_msg.encode())
            redraw_callback()
        except Exception:
            pass
