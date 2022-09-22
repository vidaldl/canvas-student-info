from __future__ import print_function
from datetime import date, datetime, timedelta
from random import randint, random
from config import *

import mysql.connector
import requests

import json
from types import SimpleNamespace



def insertIntoQuizzes(rows):
    cnx = mysql.connector.connect(user=dbUser, password=dbPassword, database=dbName)
    cursor = cnx.cursor()


    add_quizz = ("INSERT INTO quizzes (quiz_canvas_id, quiz_assignment_id, quiz_title, quiz_description) " + "VALUES (%s, %s, %s, %s)")

    cursor.executemany(add_quizz, rows)

    # Make sure data is committed to the database
    cnx.commit()

    cursor.close()
    cnx.close()



quizzes = []
quizId = 0

pageNum = 1
isNextPage = True
while isNextPage:
    endpoint = "https://byui.instructure.com:443/api/v1/courses/" + str(course) + "/quizzes?page=" + str(pageNum)
    headers = {"Authorization": "Bearer " + token}

    response = requests.get(endpoint, headers=headers)
    responseJson = response.json()
    responseHeaders = response.headers["link"]
    if 'rel="next"' not in responseHeaders:
        isNextPage = False

    for quiz in responseJson:
        currentQuiz = {
            "id": quizId,
            "canvas_id": str(quiz["id"]),
            "quiz_title": quiz["title"],
            "description": quiz["description"],
            "assignment_id": str(quiz["assignment_id"])
        }
        quizzes.append(currentQuiz)
        quizId = quizId + 1


    pageNum = pageNum + 1


# Iterate through all quizzes and add them to the database.
quizQueries = []
for quiz in quizzes:
    quizSQL = (quiz["canvas_id"], quiz["assignment_id"], quiz["quiz_title"], quiz["description"])
    quizQueries.append(quizSQL)

insertIntoQuizzes(quizQueries)
