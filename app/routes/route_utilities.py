from flask import abort, make_response
from sqlalchemy import func, or_
from app.models.site import Site
from app.models.organization import Organization, OrgType
from app.models.service import Service
from app.models.site_service import SiteService
from ..db import db

# VALID_DAYS = {
#     "sunday",
#     "monday",
#     "tuesday",
#     "wednesday",
#     "thursday",
#     "friday",
#     "saturday",
# }


def is_open_on_day(day):
    return func.coalesce(func.jsonb_array_length(Site.hours.op("->")(day)), 0) > 0


def apply_site_filters(query, filters):
    if not filters:
        return query

    # optional: day
    days = [day.lower() for day in filters.getlist("day")]

    if days:
        query = query.where(or_(*[is_open_on_day(day) for day in days]))

    # optional: organization_type
    org_types = [
        OrgType.from_frontend(value) for value in filters.getlist("organization_type")
    ]
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

# def create_model(cls, model_data):
#     try:
#         new_model = cls.from_dict(model_data)
#     except KeyError as error:
#         invalid_msg = {"details": "Invalid data"}
#         abort(make_response(invalid_msg, 400))
    
#     db.session.add(new_model)
#     db.session.commit()

#     return new_model



# day={{DAY}}&
# organization_type={{ORGANIZATION_TYPE}}&
# service={{SERVICE_TYPE}}

# Filters received: ImmutableMultiDict([('lat', '47.6204'),
# ('lon', '-122.3494'),
# ('radius_miles', '5'),
# ('day', '["wednesday\', "friday"]'),
# ('organization_type', '"food_bank"'),
# ('service', "['food_bank', 'meal']")])


def get_models_with_filters(cls, filters=None):
    query = db.select(cls)
    # find the nearby sites based on lat, lon, radius_miles

    # check other filters like day, organization_type, service_type
    query = apply_site_filters(query, filters)

    models = db.session.scalars(query.order_by(cls.id)).all()
    models_response = [model.to_dict() for model in models]
    return models_response
