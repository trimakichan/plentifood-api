from flask import Flask
import os
from .db import db, migrate
from .models.site import Site
from .models.service import Service
from .models.site_service import SiteService
from app.routes.home_routes import bp as home_bp
from app.routes.site_routes import bp as site_bp

def create_app(config=None):
    app = Flask(__name__)
    # __name__ tells Flask which python module is the starting point so it can correctly locate template, static files and configuration.

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")

    if config:
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(home_bp)
    app.register_blueprint(site_bp)

    return app
