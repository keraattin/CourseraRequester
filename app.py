#!/usr/bin/env python3

# Libraries
##############################################################################
from flask import Flask

from models import db
from views import views_bp
##############################################################################


# Configs
##############################################################################
# App
app = Flask(__name__,template_folder='templates',static_folder='static')

# Database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# SQLAlchemy Configs
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Port
PORT = 5000

# Host
HOST = '0.0.0.0'

# Inıt Database
db.init_app(app)

# Create Database
with app.app_context():
    db.create_all()
##############################################################################


# Blueprints
##############################################################################
app.register_blueprint(views_bp, url_prefix='/')
##############################################################################


# Main
##############################################################################
if __name__ == '__main__':
    app.run(debug=True,host=HOST, port=PORT)
##############################################################################