USE student_answer_data;
SELECT student.student_name  AS "student", question.question_title AS "question", question.question_id, answer, correct 
FROM quiz_answers AS answers
	INNER JOIN quiz_questions AS question ON answers.quiz_questions_question_id = question.question_id
    INNER JOIN student ON answers.student_student_id = student.student_id;