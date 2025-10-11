import paramiko
from config import PASSWORD, MAX_USERNAME_LENGTH

class SSHAuthHandler(paramiko.ServerInterface):
    def __init__(self):
        self.username = None
    
    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if password == PASSWORD:
            self.username = username[:MAX_USERNAME_LENGTH]
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_channel_shell_request(self, channel):
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True
