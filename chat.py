#!/usr/bin/env python3
"""
Minimal SSH chat server using paramiko.
Run: python3 chat.py
Connect: ssh -p 2222 user@localhost
"""

import logging
from server.server import ChatServer
from config import HOST, PORT

logging.getLogger("paramiko").setLevel(logging.WARNING)

if __name__ == "__main__":
    server = ChatServer(HOST, PORT)
    server.start()
