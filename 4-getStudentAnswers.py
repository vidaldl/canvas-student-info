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






def insertIntoAnswers(rows):
    cnx = mysql.connector.connect(user=dbUser, password=dbPassword, database=dbName)
    cursor = cnx.cursor()

    add_questions = ("INSERT INTO quiz_answers (answer_canvas_id, answer, correct, score, quiz_questions_question_id, student_student_id)" + "VALUES (%s, %s, %s, %s, %s, %s)")
    #INNER JOIN?
    # Insert World Population
    cursor.executemany(add_questions, rows)

    # Make sure data is committed to the database
    cnx.commit()

    cursor.close()
    cnx.close()


def getQuestionScore(question_id):
    cnx = mysql.connector.connect(user=dbUser, password=dbPassword, database='student_answer_data')
    cursor = cnx.cursor()



    query = ("SELECT question_possible_score FROM quiz_questions WHERE question_id = " + question_id)


    cursor.execute(query)

    for question_score in cursor:
        return question_score[0];


    cursor.close()
    cnx.close()




def getStudentId(student_canvas_id):
    cnx = mysql.connector.connect(user=dbUser, password=dbPassword, database='student_answer_data')
    cursor = cnx.cursor()



    query = ("SELECT student_id FROM student WHERE student_canvas_id = " + str(student_canvas_id))


    cursor.execute(query)

    for question_score in cursor:
        return question_score[0];


    cursor.close()
    cnx.close()


def getAnswers(courseId, quizId):
    #Response does not have pages    
    endpoint = "https://byui.instructure.com:443/api/v1/courses/" + str(courseId) + "/quizzes/" + str(quizId) + "/statistics"
    headers = {"Authorization": "Bearer " + token}

    response = requests.get(endpoint, headers=headers)
    responseJson = response.json()


    for statistics in responseJson["quiz_statistics"]:

        for questions in statistics["question_statistics"]:
            questionAnswers = []


            if(questions["question_type"] == "essay_question"):
                for answers in questions["answers"]:
                    for userAnswer in answers["user_ids"]:
                        ## Set an ID for the studentId
                        nullId = 1
                        studentId = 0 
                        if answers["id"] == "None":
                            studentId = noneId
                            nullId = nullId + 1
                        else:
                            studentId = getStudentId(userAnswer)
                        correct = 1 if answers["score"] > 0 else 0
                        userSingleAnswer = (
                            answers["id"],  #answer_canvas_id 
                            "graded essay question", #answer
                            correct, #correct
                            answers["score"], #score
                            questions["id"], #quiz_questions_question_id
                            getStudentId(userAnswer) #student_student_id
                        )
                        
                        questionAnswers.append(userSingleAnswer)
            else:
                for answers in questions["answers"]:
                    for userAnswer in answers["user_ids"]:

                        ## Setup correct for database
                        correct = 1 if answers["correct"] == True else 0

                        ## Set an ID for the answer
                        noneId = 1
                        answerId = 0 
                        if answers["id"] == "None":
                            answerId = noneId
                            noneId = noneId + 1
                        else:
                            answerId = answers["id"]

                        ## Set an ID for the studentId
                        nullId = 1
                        studentId = 0 
                        if answers["id"] == "None":
                            studentId = noneId
                            nullId = nullId + 1
                        else:
                            studentId = getStudentId(userAnswer)


                        userSingleAnswer = (
                            answerId,  #answer_canvas_id 
                            answers["text"], #answer
                            correct, #correct
                            getQuestionScore(questions["id"]), #score
                            questions["id"], #quiz_questions_question_id
                            studentId #student_student_id
                        )
                        
                        questionAnswers.append(userSingleAnswer)

            # Insert per every question
            insertIntoAnswers(questionAnswers);
                   
    
    # Sleep
    time.sleep(0.10)



# Iterate through all quizzes and add them to the database.


quizzesIds = []
getQuizzes()





for quizId in quizzesIds:
    getAnswers(course, quizId)



