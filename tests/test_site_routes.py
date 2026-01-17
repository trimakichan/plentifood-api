from werkzeug.exceptions import HTTPException
from app.models.site import Site, SiteStatus, Eligibility
from app.db import db
import pytest


def test_get_nearby_sites_with_no_records(client):
    # Act
    response = client.get("/sites/nearby?lat=47.3&lon=-122.2&radius_miles=50")
    response_body = response.get_json()
    print(response, response_body)

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_nearby_sites_with_two_sites(client, two_saved_sites):
    # Act
    response = client.get("/sites/nearby?lat=47.3&lon=-122.2&radius_miles=50")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2

    query = db.select(Site).order_by(Site.id)
    sites = db.session.scalars(query).all()

    assert response_body[0] == sites[0].to_dict()
    assert response_body[1] == sites[1].to_dict()

def test_nearby_filter_day_single_wednesday(client, three_saved_sites):
    response = client.get("/sites/nearby?lat=47.3&lon=-122.2&radius_miles=50&day=wednesday")
    assert response.status_code == 200
    
    response_body = response.get_json()
    names = {s["name"] for s in response_body}
    assert names == {"Wed Site"}


def test_nearby_filter_day_single_friday(client, three_saved_sites):
    response = client.get("/sites/nearby?lat=47.3&lon=-122.2&radius_miles=50&day=friday")
    assert response.status_code == 200
    
    response_body = response.get_json()
    names = {s["name"] for s in response_body}
    assert names == {"Fri Site"}


def test_nearby_filter_day_multiple_or(client, three_saved_sites):
    response = client.get("/sites/nearby?lat=47.3&lon=-122.2&radius_miles=50&day=wednesday&day=friday")
    assert response.status_code == 200
    
    response_body = response.get_json()
    names = {s["name"] for s in response_body}
    assert names == {"Wed Site", "Fri Site"}

def test_nearby_filter_day_no_result(client, three_saved_sites):
    response = client.get("/sites/nearby?lat=47.3&lon=-122.2&radius_miles=50&day=sunday")
    assert response.status_code == 200
    
    response_body = response.get_json()
    assert response_body == []

# def test_nearby_filter_missing_params(client, three_saved_sites):
#     # Act
#     response = client.get("/sites/nearby")
#     response_body = response.get_json()
    
#     # Assert
#     assert response.status_code == 400
#     assert response_body == {"Missing required parameter: lat"}
