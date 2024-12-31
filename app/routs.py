from app import app
from flask import flash, render_template, redirect, url_for, jsonify, abort, request, send_file
from .utils import allowed_file, random_hex_token, start_conversion
from werkzeug.utils import secure_filename
import os

@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for('convert'))

@app.route('/convert', methods=["POST", "GET"])
def convert():
    if request.method == "GET":
        return render_template("convert.html")
    file = request.files.get('filepond')
    if not allowed_file(file.filename): abort(400)
    filename = secure_filename(file.filename)
    token = random_hex_token()
    
    os.mkdir(f"instance/conversions/{token}")
    file.save(f"instance/conversions/{token}/{filename}")

    start_conversion.delay(token)

    return token

@app.route('/convert/<conversion_id>/download')
def download_conversion(conversion_id):
    if os.path.exists(f"instance/conversions/{conversion_id}/output.zip"):
        return send_file(f"../instance/conversions/{conversion_id}/output.zip")
    abort(404)

@app.route('/convert/<conversion_id>')
def view_conversion(conversion_id):
    with open(f"instance/conversions/{conversion_id}/info.txt", "r") as info_file:
        status = list(info_file.readlines())[-1]
        download = None
        if "download" in status:
            download = url_for('download_conversion', conversion_id=conversion_id)
    original_files = [fn for fn in os.listdir(f"instance/conversions/{conversion_id}") if fn.endswith(".py")]
    return render_template("view_conversion.html", status=status, download=download, filenames=original_files)