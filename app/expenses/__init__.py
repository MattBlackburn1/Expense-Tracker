from flask import Blueprint

bp = Blueprint("expenses", __name__, template_folder="templates")
from . import routes  # noqa: F401,E402  (side-effect import; must be after bp)
