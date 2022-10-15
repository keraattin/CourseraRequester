#!/usr/bin/env python3

# Libraries
##############################################################################
from flask_sqlalchemy import SQLAlchemy
##############################################################################

# Global Values
##############################################################################
LEN_NAME  = 256
LEN_QUERY = 128
##############################################################################

# Database Object
##############################################################################
db = SQLAlchemy()
##############################################################################

# Models
##############################################################################
class Courses(db.Model):
    __tablename__ = 'courses'

    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True
    )
    query = db.Column(
        db.String(LEN_QUERY), nullable=False
    )
    name = db.Column(
        db.String(LEN_NAME), unique=True, nullable=False
    )
    created_date = db.Column(
        db.DateTime, nullable=False
    )

##############################################################################