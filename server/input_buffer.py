class InputBuffer:
    def __init__(self, channel):
        self.channel = channel
        self.buffer = ""
        self.prompt = "> "
    
    def add_char(self, char):
        self.buffer += char
        self.channel.send(char.encode())
    
    def remove_char(self):
        if self.buffer:
            self.buffer = self.buffer[:-1]
            self.channel.send(b'\x08 \x08')
    
    def get_and_clear(self):
        message = self.buffer.strip()
        self.buffer = ""
        return message
    
    def clear_line(self):
        self.channel.send(b'\r\x1b[K')
    
    def show_prompt(self):
        self.channel.send(self.prompt.encode())
    
    def redraw_input_line(self):
        """Clear the current line and redraw the prompt with current buffer content"""
        self.channel.send(b'\r\x1b[K')
        self.channel.send(self.prompt.encode())
        if self.buffer:
            self.channel.send(self.buffer.encode())
