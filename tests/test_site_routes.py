from werkzeug.exceptions import HTTPException
from app.models.site import Site, SiteStatus, Eligibility
from app.db import db
import pytest

# --------------get_nearby_sites tests--------------
def test_get_nearby_sites_with_no_records(client):
    # Act
    response = client.get("/sites/nearby?lat=47.3&lon=-122.2&radius_miles=50")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {"total_results": 0, "results": []}

def test_get_nearby_sites_with_two_sites(client, two_saved_sites):
    # Act
    response = client.get("/sites/nearby?lat=47.3&lon=-122.2&radius_miles=50")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body["total_results"] == 2

    query = db.select(Site).order_by(Site.id)
    sites = db.session.scalars(query).all()

    assert response_body["results"][0] == sites[0].to_dict()
    assert response_body["results"][1] == sites[1].to_dict()


def test_nearby_filter_day_single_wednesday(client, three_saved_sites):
    resp = client.get("/sites/nearby?lat=47.3&lon=-122.2&radius_miles=50&day=wednesday")
    assert resp.status_code == 200
    data = resp.get_json()

    names = {s["name"] for s in data["results"]}
    assert names == {"Wed Site"}


def test_nearby_filter_day_single_friday(client, three_saved_sites):
    resp = client.get("/sites/nearby?lat=47.3&lon=-122.2&radius_miles=50&day=friday")
    assert resp.status_code == 200
    data = resp.get_json()

    names = {s["name"] for s in data["results"]}
    assert names == {"Fri Site"}


def test_nearby_filter_day_multiple_or(client, three_saved_sites):
    resp = client.get("/sites/nearby?lat=47.3&lon=-122.2&radius_miles=50&day=wednesday&day=friday")
    assert resp.status_code == 200
    data = resp.get_json()

    names = {s["name"] for s in data["results"]}
    assert names == {"Wed Site", "Fri Site"}

# --------------get_site tests--------------
def test_get_site_by_id(client, one_saved_site):
    # Act
    response = client.get(f"/sites/{one_saved_site.id}")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200

    query = db.select(Site).where(Site.id == one_saved_site.id)
    site = db.session.scalars(query).one()

    assert response_body == site.to_dict()

def test_get_site_invalid_site_id(client):
    # Arrange
    response = client.get("/sites/id")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Site id invalid"}

def test_get_site_not_found(client):
    # Arrange
    response = client.get("/sites/0")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Site 0 not found"}





# 
