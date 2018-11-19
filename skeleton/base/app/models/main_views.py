import os
from flask import render_template, flash, redirect, url_for, request, current_app, make_response
from werkzeug.utils import secure_filename
from app.common.utils import Utils
from . import main

@main.route('/')
def index():
    return render_template('index.jinja2')