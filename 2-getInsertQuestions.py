from __future__ import print_function
from datetime import date, datetime, timedelta
from random import randint, random
from config import *

import mysql.connector
import requests
import time

import json
from types import SimpleNamespace


def getQuizzes():
    cnx = mysql.connector.connect(user=dbUser, password=dbPassword, database=dbName)
    cursor = cnx.cursor()



    query = ("SELECT quiz_canvas_id FROM quizzes")


    cursor.execute(query)

    for quiz_canvas_id in cursor:
        quizzesIds.append(quiz_canvas_id[0]);

    cursor.close()
    cnx.close()






def insertIntoQuestions(rows):
    cnx = mysql.connector.connect(user=dbUser, password=dbPassword, database=dbName)
    cursor = cnx.cursor()

    # "question_id": str(quizQuestion["id"]),
    # "question_title": str(quizQuestion["question_name"]),
    # "question_body": quizQuestion["question_text"],
    # "quizzes_quiz_id": str(quizId)

    add_questions = ("INSERT INTO quiz_questions (question_id, question_title, question_body, question_possible_score, quizzes_quiz_canvas_id)" + "VALUES (%s, %s, %s, %s, %s)")

    # Insert World Population
    cursor.executemany(add_questions, rows)

    # Make sure data is committed to the database
    cnx.commit()

    cursor.close()
    cnx.close()



def getQuestions(courseId, quizId):

    pageNum = 1
    isNextPage = True
    while isNextPage:
        endpoint = "https://byui.instructure.com:443/api/v1/courses/" + str(courseId) + "/quizzes/" + str(quizId) + "/questions?page=" + str(pageNum)
        headers = {"Authorization": "Bearer " + token}

        response = requests.get(endpoint, headers=headers)
        responseJson = response.json()
        responseHeaders = response.headers["link"]
        if 'rel="next"' not in responseHeaders:
            isNextPage = False

        questions = []

        for quizQuestion in responseJson:
            question = (
                 quizQuestion["id"],  #question_id
                 quizQuestion["question_name"], #question_title
                 quizQuestion["question_text"], #question_body
                 quizQuestion["points_possible"], #question_possible_score
                 quizId #quizzes_quiz_id
            )
            questions.append(question)
        # print(questions)
        insertIntoQuestions(questions);
        # Sleep
        time.sleep(0.10)


        pageNum = pageNum + 1


# Iterate through all quizzes and add them to the database.

quizzesIds = []
getQuizzes()

print(quizzesIds)


for quizId in quizzesIds:
    getQuestions(course, quizId)



# quizQueries = []
# for quiz in quizzes:
#     quizSQL = (quiz["canvas_id"], quiz["assignment_id"], quiz["quiz_title"], quiz["description"])
#     quizQueries.append(quizSQL)

# insertIntoQuizzes(quizQueries)
