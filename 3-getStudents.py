## LEFT FROM HERE

from __future__ import print_function
from datetime import date, datetime, timedelta
from random import randint, random
from config import *

import mysql.connector
import requests

import json
from types import SimpleNamespace


def insertIntoStudents(rows):
    cnx = mysql.connector.connect(user=dbUser, password=dbPassword, database=dbName)
    cursor = cnx.cursor()


    add_student = ("INSERT INTO student (student_canvas_id, student_name, student_sortable_name) " + "VALUES (%s, %s, %s)")

    # Insert World Population
    cursor.executemany(add_student, rows)

    # Make sure data is committed to the database
    cnx.commit()

    cursor.close()
    cnx.close()



students = []
pageNum = 1
isNextPage = True

endpoint = "https://byui.instructure.com:443/api/v1/courses/" + str(course) + "/students?page=" + str(pageNum)
headers = {"Authorization": "Bearer " + token}

response = requests.get(endpoint, headers=headers)
responseJson = response.json()

for student in responseJson:
    currStudent = (
        student["id"], # student_canvas_id
        student["name"], # student_name
        student["sortable_name"] # student_sortable_name
    )
    students.append(currStudent)
    


pageNum = pageNum + 1


# Add to Database
insertIntoStudents(students)
