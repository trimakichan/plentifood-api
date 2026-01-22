from flask import Blueprint, request, abort, make_response
from app.models.organization import Organization
from app.models.admin_user import AdminUser
from app.models.site import Site
from ..db import db
from app.routes.route_utilities import validate_model, create_model

bp = Blueprint("organizations_bp", __name__, url_prefix="organizations")

@bp.get("")
def get_all_orgs():
    query = db.select(Organization)
    orgs = db.session.scalars(query)
    orgs_list = [org.to_dict() for org in orgs] 
    return {"orgs": orgs_list}, 200

@bp.get("/<org_id>")
def get_org(org_id):
    org = validate_model(Organization, org_id)
    return org.to_dict(), 200

@bp.delete("/<org_id>")
def delete_org(org_id):
    org = validate_model(Organization, org_id)
    db.session.delete(org)
    db.session.commit()
    return {"details": f'Organization {org_id} "{org.name}" successfully deleted'}, 200

# with sites
@bp.post("/<org_id>/sites")
def create_site_on_org(org_id):
    org = validate_model(Organization, org_id)
    data = request.get_json()
    return create_model(Site, {**data, "organization_id": Organization.id})

@bp.get("/<org_id>/site")
def get_cards_on_board(org_id):
    org = validate_model(Organization, org_id)
    sites = org.sites
    sites_list = [site.to_dict() for site in sites]
    return {"sites": sites_list}, 200

@bp.delete("/<org_id>/<site_id>")
def delete_site_on_org(org_id, site_id):
    org = validate_model(Organization, org_id)
    site = validate_model(Site, site_id)
    if site.org_id != org.org_id:
        response = {"details": f"Site {site_id} does not belong to Organization {org_id}"}
        abort(make_response(response, 400))
    db.session.delete(site)
    db.session.commit()
    return {"details": f'Site {site_id} successfully deleted from Board {site_id}'}, 200