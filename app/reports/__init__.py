from flask import Blueprint

bp = Blueprint("reports", __name__, template_folder='templates')

from . import routes