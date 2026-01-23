from flask import Blueprint, request, abort, make_response
from ..routes.route_utilities import get_models_with_filters
from ..models.service import Service
from ..db import db


bp = Blueprint("service_bp", __name__, url_prefix="/services")

@bp.post("")
def create_service():
    request_body = request.get_json()

    try:
        new_service = Service.from_dict(request_body)
    except KeyError as error:
        invalid_msg = {"details": f"Invalid data: {error}"}
        abort(make_response(invalid_msg, 400)) 

    db.session.add(new_service)
    db.session.commit()

    return make_response(new_service.to_dict(), 201)

@bp.get("")
def get_services():
    return get_models_with_filters(Service)