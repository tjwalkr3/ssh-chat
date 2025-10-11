# SSH Chat

## File Organization

```
ssh-chat/
├── chat.py                     (entry point)
├── config.py                   (configuration loader)
├── config.yml                  (yaml chat configurations)
├── server/                     (server implementation)
│   ├── __init__.py
│   ├── server.py               (ChatServer)
│   ├── client_session.py       (ClientSession)
│   ├── client_registry.py      (ClientRegistry)
│   ├── ssh_auth.py             (SSHAuthHandler)
│   └── input_buffer.py         (InputBuffer)
├── Makefile
└── README.md
```


## Usage
**Run the server:**
```bash
make install && make run
```

**Connect with:**
```bash
ssh -p 2222 <username>@localhost
```
Password: `pass`
