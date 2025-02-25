##------ Data models------##

from flask_sqlalchemy import SQLAlchemy
from datetime import date, time, datetime
from sqlalchemy.sql import func


db = SQLAlchemy()


# Entity_1 User
class User_Info(db.Model):
    __tablename__="user_info"
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String,nullable=False)
    full_name=db.Column(db.String,nullable=False)
    qualification=db.Column(db.String,nullable=False)
    dob=db.Column(db.Date,nullable=False)
    role=db.Column(db.Integer,default=1)

    scores=db.relationship("Score",cascade="all,delete",backref="user_info",lazy="select")
    



# Entity_2 Subject
class Subject(db.Model):
    __tablename__="subject"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,nullable=False)
    code=db.Column(db.String,nullable=False,unique=True)
    credit=db.Column(db.Integer,nullable=False)
    description=db.Column(db.String,nullable=False)

    chapters=db.relationship("Chapter",cascade="all,delete",backref="subject",lazy="select")




# Entity_3 Chapter
class Chapter(db.Model):
    __tablename__="chapter"
    id=db.Column(db.Integer,primary_key=True)
    subject_id=db.Column(db.Integer,db.ForeignKey("subject.id"),nullable=False)
    title=db.Column(db.String,nullable=False)
    chapter_no=db.Column(db.Integer,nullable=False)
    
    quizzes=db.relationship("Quiz",cascade="all,delete",backref="chapter",lazy="select")




# Entity_4 Quiz
class Quiz(db.Model):
    __tablename__="quiz"
    id=db.Column(db.Integer,primary_key=True)
    chapter_id=db.Column(db.Integer,db.ForeignKey("chapter.id"),nullable=False)
    duration=db.Column(db.Integer,nullable=False)
    date_of_quiz=db.Column(db.Date,nullable=False)
    total_questions=db.Column(db.Integer,nullable=False)

    scores=db.relationship("Score",cascade="all,delete",backref="quiz",lazy="select")
    questions=db.relationship("Question",cascade="all,delete",backref="quiz",lazy="select")




# Entity_5 Question
class Question(db.Model):
    __tablename__="question"
    id=db.Column(db.Integer,primary_key=True)
    quiz_id=db.Column(db.Integer,db.ForeignKey("quiz.id"),nullable=False)
    question_statement=db.Column(db.Text,nullable=False)
    option1 = db.Column(db.String,nullable=False)
    option2 = db.Column(db.String,nullable=False)
    option3 = db.Column(db.String,nullable=False)
    option4 = db.Column(db.String,nullable=False)
    correct_option = db.Column(db.Integer,nullable=False)

    

    
# Entity_6 Score
class Score(db.Model):
    __tablename__="score"
    id=db.Column(db.Integer,primary_key=True)
    quiz_id=db.Column(db.Integer,db.ForeignKey("quiz.id"),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey("user_info.id"),nullable=False)
    time_stamp = db.Column(db.DateTime,nullable=False,default=func.now())
    total_scored=db.Column(db.Integer,nullable=False,default=0)
    total_possible_score = db.Column(db.Integer,nullable=False)
    percentage_scored=db.Column(db.Float,nullable=False,default=0.0)
    pass_fail_status=db.Column(db.String,nullable=False,default="Fail")
