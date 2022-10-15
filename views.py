#!/usr/bin/env python3

# Libraries
##############################################################################
from datetime import datetime
from flask import Blueprint, request, render_template
from functions import get_courses, write_to_csv
from flask import send_file
from models import db,Courses
##############################################################################

# Global Values
##############################################################################
TF = '%Y-%m-%d %H:%M:%S' # Time Format
##############################################################################

# Blueprint
##############################################################################
views_bp = Blueprint('views_blueprint', __name__)
##############################################################################


# Views
##############################################################################
@views_bp.route('/', methods = ['GET'])
def index():
    return render_template('search_courses.html')

@views_bp.route('/search_courses', methods = ['GET','POST'])
def search_courses():
    if request.method == 'POST':
        if request.form['search_query']:
            query = request.form['search_query']

            # Getting courses using API
            courses = get_courses(query)

            # Writing courses to the CSV and get filename
            filename = write_to_csv(query,courses)

            # Write to DB
            try:
                course_list = Courses(
                    query=query,
                    name=filename,
                    created_date=datetime.now()
                )
                db.session.add(course_list)
                db.session.commit()
            except Exception as e:
                return render_template(
                    'error.html',
                    error=str(e)
                )

            return render_template(
                'results.html',
                courses=courses,
                filename=filename
            )
    return render_template('search_courses.html')

@views_bp.route('/downloaded_courses', methods = ['GET'])
def downloaded_courses():
    courses = db.session.query(
        Courses,
        Courses.id,
        Courses.query,
        Courses.name,
        Courses.created_date).all()
    return render_template(
                'downloaded_courses.html',
                courses=courses
            )

@views_bp.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    path="./static/reports/"+filename
    return send_file(path, as_attachment=True)
##############################################################################