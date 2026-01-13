from flask import Flask
from .db import db, migrate
import os

def create_app(config=None):
  app = Flask(__name__) 
  #__name__ tells Flask which python module is th e starting point so it can correctly locate template, static files and configuration.

  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')