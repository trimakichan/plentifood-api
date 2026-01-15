import pytest
from app import create_app
from app.db import db
from flask.signals import request_finished
from dotenv import load_dotenv
import os
from app.db import db
from app.models.site import Site
from app.models.service import Service


load_dotenv()

@pytest.fixture
def app():
  test_config = {
      "TESTING": True,
      "SQLALCHEMY_DATABASE_URI_TEST": os.environ.get("SQLALCHEMY_DATABASE_URI_TEST")
  }

  app = create_app(test_config)

  @request_finished.connect_via(app)
  def expire_session(sender, response, **extra):
      db.session.remove()
  
  with app.app_context():
      db.create_all()
      yield app

  with app.app_context():
    db.drop_all()

# This is for tests that make HTTP requests.
@pytest.fixture
def client(app):
  return app.test_client()

# Seeding services. check this later@pytest.fixture
# def seed_services(app):
#     # Create developer-controlled lookup values
#     services = [
#         Service(name="Food Bank"),
#         Service(name="Meal"),
#     ]

#     for s in services:
#         exists = Service.query.filter_by(name=s.name).first()
#         if not exists:
#             db.session.add(s)

#     db.session.commit()
#     return {s.name: Service.query.filter_by(name=s.name).first() for s in services}