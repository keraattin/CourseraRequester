#!/usr/bin/env python3

# Libraries
##############################################################################
import requests
import csv
from datetime import datetime
##############################################################################

# Global Values
##############################################################################
# API KEY for API
API_KEY = "dcc55281ffd7ba6f24c3a9b18288499b"

# Application Id for API
APPLICATION_ID = "LUA9B20G37"

# Url for API
URL = ("https://lua9b20g37-dsn.algolia.net/1/indexes/*/queries?"+
  "&x-algolia-application-id=LUA9B20G37&x-algolia-api-key=%s" % API_KEY)

# Time Format
TF = '%Y-%m-%d_%H-%M-%S'
##############################################################################

# First we need to get nbHits(The number of returned courses)
def get_nb_hits(param):
  payload = """{
    "requests": [
        {
            "indexName": "prod_all_launched_products_term_optimization",
            "params": "query=%s&hitsPerPage=1"
        }
    ]
  }""" % (param)
    
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json'
  }

  response = requests.request("POST", URL, headers=headers, data=payload)
  response = response.json()
  nb_hits = response["results"][0]["nbHits"]
  return nb_hits

# Get Course Contents
def get_courses(param):
  nb_hits = str(get_nb_hits(param))

  payload = """{
    "requests": [
        {
            "indexName": "prod_all_launched_products_term_optimization",
            "params": "query=%s&hitsPerPage=%s&attributes=name,enrollments,instructors,description,numProductRatings"
        }
    ]
  }""" % (param,nb_hits)

  headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json'
  }

  response = requests.request("POST", URL, headers=headers, data=payload)
  response = response.json()

  courses = []
  for data in response["results"][0]["hits"]:
    # Name
    if data["name"]:
      name = data["name"]
    else:
      name = ""

    # Instructor
    if data["instructors"]:
      instructor = data["instructors"][0]
    else:
      instructor = ""

    # Description
    if data["description"]:
      description = data["description"]
    else:
      description = ""
    
    # Enrollments
    if data["enrollments"]:
      enrollments = data["enrollments"]
    else:
      enrollments = ""
    
    # numProductRatings
    if data["numProductRatings"]:
      num_of_ratings = data["numProductRatings"]
    else:
      num_of_ratings = ""

    course = {
      "category":param,
      "name":name,
      "instructor":instructor,
      "description":description,
      "enrollments":enrollments,
      "num_of_ratings":num_of_ratings
    }
    courses.append(course)
  
  return courses

# Write to CSV
def write_to_csv(query,courses):
  header = [
    'Category Name',
    'Course Name',
    'First Instructor Name',
    'Course Description',
    '# of Students Enrolled',
    '# of Ratings'
  ]
  file_path = 'static/reports/'
  file_name = str(query)+"_"+str(datetime.now().strftime(TF))+".csv"

  with open(file=file_path+file_name, mode='w+', encoding='UTF8') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    # write the data
    for data in courses:
      w_data = list(data.values())
      writer.writerow(w_data)
  
  return file_name