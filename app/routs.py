from app import app
from flask import flash, render_template, redirect, url_for, jsonify, abort, request

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")