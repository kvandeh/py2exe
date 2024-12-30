from app import app
from flask import flash, render_template, redirect, url_for, jsonify, abort, request
from .utils import allowed_file, random_hex_token
from werkzeug.utils import secure_filename
import os

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/convert', methods=["POST", "GET"])
def convert():
    if request.method == "GET":
        return render_template("convert.html")
    file = request.files.get('filepond')
    if not allowed_file(file.filename): abort(400)
    filename = secure_filename(file.filename)
    token = random_hex_token()
    
    os.mkdir(f"instance/{token}")
    file.save(f"instance/{token}/{filename}")

    return token