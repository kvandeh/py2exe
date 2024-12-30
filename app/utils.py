from . import app
import random

def allowed_file(filename, allowed_extensions=app.config["ALLOWED_EXTENSIONS"]):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def random_hex_token(length=16):
    return ''.join(random.choice('0123456789abcdef') for _ in range(length))