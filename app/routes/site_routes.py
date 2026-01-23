from flask import Blueprint, request, abort, Response, make_response
from datetime import datetime, timezone
from ..models.site import Site, SiteStatus, Eligibility
from .route_utilities import validate_model, get_models_with_filters
from ..db import db

bp = Blueprint("sites_bp", __name__, url_prefix="/sites")

UPDATABLE_FIELDS = {
        "name",
        "status",
        "address_line1",
        "address_line2",
        "city",
        "state",
        "postal_code",
        "phone",
        "eligibility",
        "hours",
        "service_notes",
}

@bp.get("/nearby")
def get_nearby_sites():

    required_params = ["lat", "lon", "radius_miles"]
    for param in required_params:
        if param not in request.args:
            abort(400, description=f"Missing required parameter: {param}")

    return get_models_with_filters(Site, filters=request.args)


def get_site(site_id):
    site = validate_model(Site, site_id)
    return site.to_dict()

@bp.get("<site_id>")
def get_site(site_id):
    site = validate_model(Site, site_id)
    return site.to_dict()

# refactor 
@bp.patch("/<site_id>")
def update_site(site_id):
    site = validate_model(Site, site_id)
    request_body = request.get_json()

    if not request_body:
        response = {"message": "Request body cannot be empty."}
        abort(make_response(response, 400))


    for field in UPDATABLE_FIELDS:
        if field in request_body:
            if field == "status":
                site.status = SiteStatus.from_frontend(request_body["status"])
            elif field == "eligibility":
                site.eligibility = Eligibility.from_frontend(request_body["eligibility"])
            else:
                setattr(site, field, request_body[field])
    
    site.updated_at = datetime.now(timezone.utc)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.delete("/<site_id>")
def delete_site(site_id):
    site = validate_model(Site, site_id)

    db.session.delete(site)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


# Create logic to go get lat and lon based on address. 