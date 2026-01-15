from flask import Flask
import os
from .db import db, migrate
from .models.site import Site
from app.routes.home_routes import bp as home_bp

def create_app(config=None):
  app = Flask(__name__) 
  #__name__ tells Flask which python module is th e starting point so it can correctly locate template, static files and configuration.

  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

  if config:
    app.config.update(config)

  db.init_app(app)
  migrate.init_app(app, db)

  # register blueprint later
  app.register_blueprint(home_bp)

  return app

