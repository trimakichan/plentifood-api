from flask import abort, make_response
from sqlalchemy import func, or_
from app.models.site import Site
from ..db import db

VALID_DAYS = {"sunday","monday","tuesday","wednesday","thursday","friday","saturday"}

def is_open_on_day(day):
    return func.coalesce(
        func.jsonb_array_length(Site.hours.op("->")(day)),
        0
    ) > 0

def apply_site_filters(query, filters):
    
    # optional: day
    days = [ day.lower() for day in filters.getlist("day")]

    if days:
        query = query.where(or_(*[is_open_on_day(day) for day in days]))




    # optional: organization_type 

    # optional: service

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
    print(filters)
    query = db.select(cls)
    # find the nearby sites based on lat, lon, radius_miles

    # check other filters like day, organization_type, service_type
    query = apply_site_filters(query, filters)

        
    models = db.session.scalars(query.order_by(cls.id)).all()
    models_response = [model.to_dict() for model in models]
    return models_response