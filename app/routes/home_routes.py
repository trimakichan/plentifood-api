from flask import Blueprint

bp = Blueprint("home_bp", __name__)


@bp.route("/")
def home():
    return "<h1>Welcome to our PlentiFood API!</h1>"
