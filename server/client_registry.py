import threading
from dataclasses import dataclass
from datetime import datetime
from config import COLORS, USERNAME_FIELD_WIDTH


@dataclass
class RegisteredClient:
    channel: object
    username: str
    input_buffer: object

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
            self.clients.append(RegisteredClient(channel, username, input_buffer))
            return True

    def remove_client(self, channel, username):
        with self.lock:
            self.clients[:] = [client for client in self.clients if client.channel != channel]
            self.usernames.discard(username)

    def broadcast(self, message, username):
        formatted_msg = self._format_message(username, message)

        with self.lock:
            for client in self.clients:
                input_buffer = client.input_buffer
                redraw = input_buffer.show_prompt if client.username == username else input_buffer.redraw_input_line
                self._send_formatted_message(client, formatted_msg, redraw)

    def _get_color(self, username):
        return COLORS[hash(username) % len(COLORS)]

    def _format_message(self, username, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        color = self._get_color(username)
        return f"{timestamp}  \x1b[{color}m{username:>{USERNAME_FIELD_WIDTH}}\x1b[0m  |  {message}\r\n"

    def _send_formatted_message(self, client, formatted_msg, redraw_callback):
        try:
            client.input_buffer.clear_line()
            client.channel.send(formatted_msg.encode())
            redraw_callback()
        except Exception:
            pass
