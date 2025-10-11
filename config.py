import yaml
import os

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.yml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

_config = load_config()

HOST = _config['server']['host']
PORT = _config['server']['port']
PASSWORD = _config['auth']['password']
MAX_USERNAME_LENGTH = _config['username']['max_length']
USERNAME_FIELD_WIDTH = _config['username']['field_width']
COLORS = _config['colors']
