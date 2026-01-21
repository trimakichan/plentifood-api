from flask import Blueprint, request, abort, make_response, Response
from datetime import datetime, timezone
from ..models.site import Site, SiteStatus, Eligibility
from ..models.admin_user import AdminUser
from ..models.organization import Organization
from .route_utilities import validate_model, get_models_with_filters
from ..db import db

bp = Blueprint("register_bp", __name__, url_prefix="/register")

# {
#   "organization": {
#     "name": "Asian Counseling and Referral Service",
#     "organization_type": "food_bank",
#     "website": "https://acrs.org/services/aging-services-for-older-adults/acrs-food-bank/"
#   },
#   "admin": {
#     "username": "Makiko"
#   }
# }

@bp.post("")
def register():
    request_body = request.get_json()

    try:
        admin_data = request_body["admin"]
        org_data = request_body["organization"]
    except KeyError as error:
        response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))

    try:
        new_org = Organization.from_dict(org_data)
        new_admin = AdminUser.from_dict(admin_data)
    except KeyError as error:
        invalid_msg = {"details": "Invalid data"}
        abort(make_response(invalid_msg, 400))
    
    # connect those instances 
    new_admin.organization = new_org

    db.session.add(new_org)
    db.session.add(new_admin)
    db.session.commit()

    return make_response({
        "admin_user": new_admin.to_dict(),
        "organization": new_org.to_dict()
    }, 201)






