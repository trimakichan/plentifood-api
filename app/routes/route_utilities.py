from flask import abort, make_response
from sqlalchemy import func, or_
from app.models.site import Site
from app.models.organization import Organization, OrgType
from app.models.service import Service
from app.models.site_service import SiteService
from math import radians, sin, cos, asin, sqrt

from ..db import db

EARTH_RADIUS_MILES = 3958.8
MILES_PER_DEGREE_LAT = 69.0  # approx


def is_open_on_day(day):
    return func.coalesce(func.jsonb_array_length(Site.hours.op("->")(day)), 0) > 0


def apply_site_filters(query, filters):

    # optional: day
    days = [day.lower() for day in filters.getlist("day")]

    if days:
        query = query.where(or_(*[is_open_on_day(day) for day in days]))

    # Work on this logic once services are added
    # optional: organization_type
    org_types = [OrgType(value) for value in filters.getlist("organization_type")]
    if org_types:
        query = query.join(Organization).where(
            Organization.organization_type.in_(org_types)
        )

    # optional: service
    service_types = [s.lower() for s in filters.getlist("service")]

    if service_types:
        query = (
            query.join(SiteService, SiteService.site_id == Site.id)
            .join(Service, Service.id == SiteService.service_id)
            .where(Service.name.in_(service_types))
            .distinct()
        )

    return query


def validate_model(cls, model_id):

    try:
        model_id = int(model_id)
    except:
        response = {"message": f"{cls.__name__} {model_id} invalid"}
        abort(make_response(response, 400))

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        response = {"message": f"{cls.__name__} {model_id} not found"}
        abort(make_response(response, 404))

    return model


def get_models_with_filters(cls, filters=None):
    query = db.select(cls)

    # check other filters like day, organization_type, service_type
    if filters:
        # find the nearby sites based on lat, lon, radius_miles
        try:
            lat = float(filters["lat"])
            lon = float(filters["lon"])
            radius_miles = float(filters["radius_miles"])
        except ValueError:
            abort(400, description="lat, lon, and radius_miles must be numbers.")
        # Get bounding box
        min_lat, max_lat, min_lon, max_lon = bounding_box(lat, lon, radius_miles)

        query = query.filter(
            Site.latitude.isnot(None),
            Site.longitude.isnot(None),
            Site.latitude.between(min_lat, max_lat),
            Site.longitude.between(min_lon, max_lon)
        )

        query = apply_site_filters(query, filters)

    models = db.session.scalars(query.order_by(cls.id)).all()

    if filters:
        nearby = []
        for model in models:
            distance = haversine_miles(lat, lon, model.latitude, model.longitude)
            if distance <= radius_miles:
                nearby.append(model)


    models_response = [model.to_dict() for model in (nearby if filters else models)]
    return models_response


def haversine_miles(lat1, lon1, lat2, lon2):
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    )
    c = 2 * asin(sqrt(a))
    return EARTH_RADIUS_MILES * c


def bounding_box(lat, lon, radius_miles):
    lat_delta = radius_miles / MILES_PER_DEGREE_LAT
    # guard against cos(±90°) edge case
    lon_delta = radius_miles / (MILES_PER_DEGREE_LAT * max(cos(radians(lat)), 0.000001))

    return (lat - lat_delta, lat + lat_delta, lon - lon_delta, lon + lon_delta)
