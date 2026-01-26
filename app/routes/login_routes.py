from flask import Blueprint, request, abort, Response, make_response
from datetime import datetime, timezone
from ..models.admin_user import AdminUser
from ..db import db


bp = Blueprint("login_bp", __name__, url_prefix="/login")


@bp.post("")
def login():
    data = request.get_json() or {}
    username = data.get("username")
    # Give me the first row that matches this query, or None if nothing matches.
    admin = AdminUser.query.filter_by(username=username).first()

    if not username:
        return {"error": "username is required"}, 400

    if admin is None:
        return {"error": "Admin not found"}, 404

    return {
        "id": admin.id,
        "username": admin.username,
        "organization_id": admin.organization_id
    }, 200


@bp.get("/me")
def get_me():
    admin_id = request.headers.get("X-User-Id")

    if not admin_id:
        return {"error": "Missing X-User-Id header"}, 401
    
    admin = AdminUser.query.get(admin_id)

    if not admin:
        return {"error": "Invalid admin user"}, 401
    
    return {
        "id": admin.id,
        "username": admin.username,
        "organization_id": admin.organization_id
    }, 200
    
