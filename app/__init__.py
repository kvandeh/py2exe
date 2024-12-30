from flask import Flask

app = Flask(__name__)
app.secret_key = 'dev'

app.config["ALLOWED_EXTENSIONS"] = "py"

app.config.from_pyfile('../instance/config.py')

from app import routs