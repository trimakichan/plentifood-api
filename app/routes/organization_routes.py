from flask import Blueprint, request, abort, Response, make_response
from datetime import datetime, timezone
from ..models.organization import Organization, OrgType
from ..models.site import Site
from ..models.service import Service
from .route_utilities import validate_model, get_models_with_filters
from ..db import db

bp = Blueprint("organizations_bp", __name__, url_prefix="/organizations")

UPDATABLE_FIELDS = {
    "name",
    "organization_type",
    "website_url",
}

@bp.post("/<org_id>/sites")
def create_site(org_id):
    organization = validate_model(Organization, org_id)
    request_body = request.get_json()

    try:

        new_site = Site.from_dict(request_body, org_id=organization.id)
        service_names = request_body["services"]
    except KeyError as error:
        invalid_msg = {"details": f"Invalid data: {error}"}
        abort(make_response(invalid_msg, 400)) 

    services = db.session.scalars(
                db.select(Service).where(Service.name.in_(service_names))
            ).all()
    
    if len(services) != len(service_names):
        invalid_msg = {"details": "One or more services are invalid."}
        abort(make_response(invalid_msg, 400))  
    
    new_site.organization = organization
    new_site.services = services

    db.session.add(new_site)
    db.session.commit()

    return make_response(new_site.to_dict(), 201)

@bp.get("/<org_id>")
def get_organization(org_id):
    organization = validate_model(Organization, org_id)
    return organization.to_dict()

@bp.get("/<org_id>/sites")
# consider refactoring to use get_models_with_filters
def get_organization_sites(org_id):
    organization = validate_model(Organization, org_id)
    
    query = db.select(Site).where(Site.organization_id == organization.id)
    sites = db.session.scalars(query).all()

    sites_list = [site.to_dict() for site in sites]

    return sites_list

# refactor 
@bp.patch("/<org_id>")
def update_organization(org_id):
    organization = validate_model(Organization, org_id)
    request_body = request.get_json()

    if not request_body:
        response = {"message": "Request body cannot be empty."}
        abort(make_response(response, 400))

    for field in UPDATABLE_FIELDS:
        if field in request_body:
            if field == "organization_type":
                organization.organization_type = OrgType.from_frontend(request_body["organization_type"])
            else:
                setattr(organization, field, request_body[field])
    
    organization.updated_at = datetime.now(timezone.utc)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("/<org_id>")
def delete_organization(org_id):
    organization = validate_model(Organization, org_id)

    db.session.delete(organization)
    db.session.commit()

    return Response(status=204, mimetype="application/json")
