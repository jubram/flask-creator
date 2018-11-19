from flask import Blueprint

main = Blueprint('/', __name__)

from . import main_views