from flask import Blueprint, request, abort, Response, make_response
from datetime import datetime, timezone
from ..models.organization import Organization
from ..models.site import Site
from .route_utilities import validate_model, get_models_with_filters
from ..db import db

bp = Blueprint("organizations_bp", __name__, url_prefix="/organizations")


@bp.post("/<org_id>/sites")
def create_site(org_id):
    organization = validate_model(Organization, org_id)
    request_body = request.get_json()

    try:
        new_site = Site.from_dict(request_body)
    except KeyError as error:
        invalid_msg = {"details": "Invalid data: {error}"}
        abort(make_response(invalid_msg, 400)) 

    new_site.organization = organization

    db.session.add(new_site)
    db.session.commit()

    return make_response(new_site.to_dict(), 201)