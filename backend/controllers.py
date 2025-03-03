from flask import Flask, render_template, request, url_for, redirect, current_app as app
from backend.models import *
from datetime import date, datetime, time



@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login",methods=["GET","POST"])
def signin():
    if request.method=="POST":
        email=request.form.get("email")
        pwd=request.form.get("password")
        usr=User_Info.query.filter_by(email=email,password=pwd).first()
        if usr and usr.role==0: # Existed and admin
            return redirect(url_for("admin_dashboard",name=email))
        elif usr and usr.role==1: # Existed and normal user
            return redirect(url_for("user_dashboard",name=email,id=usr.id))
        else:
            return render_template("login.html",msg1="Invalide User Credentials...")
    return render_template("login.html",msg="")



@app.route("/register",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        email=request.form.get("email")
        pwd=request.form.get("password")
        full_name=request.form.get("full_name")
        qualification=request.form.get("qualification")
        dob=request.form.get("dob")
        try:
            dob = datetime.strptime(dob, "%Y-%m-%d").date()  # Converting from YYYY-MM-DD format
        except ValueError:
            return render_template("signup.html", msg="Invalid Date format. Please use the correct format.")
        # Validate required fields
        if not email or not pwd or not full_name:
            return render_template("signup.html",msg="All fields are required. Please fill out the form completely.")
        usr=User_Info.query.filter_by(email=email).first()
        if usr:
            return render_template("signup.html",msg="Sorry, already register with this email!!! try to signup with another email.")
        new_user=User_Info(email=email,password=pwd,full_name=full_name,qualification=qualification,dob=dob)
        db.session.add(new_user)
        db.session.commit()
        return render_template("login.html",msg2="Registration Successful, try logging in now.")
    return render_template("signup.html",msg="")



# Common route for adminr dashboard
@app.route("/admin/<name>")
def admin_dashboard(name):
    subjects=get_subjects()
    return render_template("admin_dashboard.html",name=name,subjects=subjects)




# Common route for user dashboard
@app.route("/user/<id>/<name>")
def user_dashboard(id,name):
    quizzes=get_quizzes()
    return render_template("user_dashboard.html",name=name,quizzes=quizzes)




@app.route("/subject/<name>",methods=["POST","GET"])
def add_subject(name):
    if request.method=="POST":
        sname=request.form.get("subject_name")
        code=request.form.get("code")
        credit=request.form.get("credit")
        description=request.form.get("description")
        new_subject=Subject(subject_name=sname,code=code,credit=credit,description=description)
        db.session.add(new_subject)
        db.session.commit()
        return redirect(url_for("admin_dashboard",name=name))
    return render_template("add_subject.html",name=name)
 



@app.route("/edit_subject/<id>/<name>",methods=["GET","POST"])
def edit_subject(id,name):
    s=get_subject(id)
    if request.method=="POST":
        new_name=request.form.get("subject_name")
        code=request.form.get("code")
        credit=request.form.get("credit")
        description=request.form.get("description")
        s.subject_name =new_name
        s.code=code
        s.credit=credit
        s.description=description
        db.session.commit()        
        return redirect(url_for("admin_dashboard",name=name))
    return render_template("edit_subject.html",subject=s,name=name)




@app.route("/delete_subject/<id>/<name>",methods=["GET","POST"])
def delete_subject(id,name):
    s=get_subject(id)
    db.session.delete(s)
    db.session.commit()
    return redirect(url_for("admin_dashboard",name=name))




@app.route("/chapter/<subject_id>/<name>",methods=["POST","GET"])
def add_chapter(subject_id,name):
    if request.method=="POST":
        chapter_name=request.form.get("chapter_name")
        chapter_no=request.form.get("chapter_no")
        new_chapter=Chapter(chapter_name=chapter_name,chapter_no=chapter_no,subject_id=subject_id)
        db.session.add(new_chapter)
        db.session.commit()
        return redirect(url_for("admin_dashboard",name=name))
    return render_template("add_chapter.html",subject_id=subject_id,name=name)




@app.route("/edit_chapter/<id>/<name>", methods=["GET", "POST"])
def edit_chapter(id, name):
    c = get_chapter(id)  # Fetch the chapter based on ID
    subject_id = c.subject_id  # Get the subject ID for this chapter
    chapters = Chapter.query.filter_by(subject_id=subject_id).all()  # Fetch all chapters for the subject
    if request.method=="POST":
        new_name=request.form.get("new_name")
        chapter_no=request.form.get("chapter_no")
        c.new_name=new_name
        c.chapter_no=chapter_no
        db.session.commit()        
        return redirect(url_for("admin_dashboard",name=name))
    
    return render_template("edit_chapter.html", chapter=c, name=name, chapters=chapters)




@app.route("/delete_chapter/<id>/<name>",methods=["GET","POST"])
def delete_chapter(id,name):
    c=get_chapter(id)
    db.session.delete(c)
    db.session.commit()
    return redirect(url_for("admin_dashboard",name=name))





@app.route('/quiz_management/<name>')
def quiz_management(name):
    quizzes = Quiz.query.all()  # Fetch updated quiz list after deletion
    return render_template("quiz_management.html", name=name, quizzes=quizzes)





@app.route("/quiz/<name>", methods=["POST", "GET"])
def add_quiz(name):
    if request.method == "POST":
        chapter_id = request.form.get("chapter_id")
        chapter = Chapter.query.filter_by(id=chapter_id).first()

        if chapter:
            chapter_name = chapter.chapter_name
        else:
            chapter_name = None  # Handle case if chapter_id is invalid

        quiz_title = request.form.get("quiz_title")
        duration = request.form.get("duration")
        date_of_quiz = request.form.get("date_of_quiz")
        date_of_quiz = datetime.strptime(date_of_quiz, "%Y-%m-%d").date()
        total_questions = request.form.get("total_questions")

        new_quiz = Quiz(
            chapter_id=chapter_id,
            chapter_name=chapter_name,
            quiz_title=quiz_title,
            duration=duration,
            date_of_quiz=date_of_quiz,
            total_questions=total_questions
        )

        db.session.add(new_quiz)
        db.session.commit()
        return redirect(url_for("quiz_management", name=name))

    # Filter out chapters that already have a quiz
    chapters_with_quizzes = {quiz.chapter_id for quiz in Quiz.query.all()}
    chapters = Chapter.query.filter(~Chapter.id.in_(chapters_with_quizzes)).all()

    return render_template("add_quiz.html", name=name, chapters=chapters)





@app.route("/edit_quiz/<quiz_id>/<name>", methods=["GET", "POST"])
def edit_quiz(quiz_id, name):
    quiz = Quiz.query.get_or_404(quiz_id)  # Fetch quiz by ID

    if request.method == "POST":
        chapter_id = request.form.get("chapter_id")
        chapter = Chapter.query.filter_by(id=chapter_id).first()

        if chapter:
            chapter_name = chapter.chapter_name
        else:
            chapter_name = None  # Handle case if chapter_id is invalid

        # Update quiz details
        quiz.chapter_id = chapter_id
        quiz.chapter_name = chapter_name
        quiz.quiz_title = request.form.get("quiz_title")
        quiz.duration = request.form.get("duration")
        quiz.date_of_quiz = datetime.strptime(request.form.get("date_of_quiz"), "%Y-%m-%d").date()
        quiz.total_questions = request.form.get("total_questions")

        db.session.commit()  # Save changes
        return redirect(url_for("quiz_management", name=name))

    # Fetch chapters excluding those already assigned to quizzes (except the current quiz's chapter)
    chapters_with_quizzes = {q.chapter_id for q in Quiz.query.all()} - {quiz.chapter_id}
    chapters = Chapter.query.filter(~Chapter.id.in_(chapters_with_quizzes)).all()

    return render_template("edit_quiz.html", name=name, quiz=quiz, chapters=chapters)





@app.route('/delete_quiz/<id>/<name>',methods=["GET", "POST"])
def delete_quiz(id, name):
    qz = get_quiz(id)
    db.session.delete(qz)
    db.session.commit()
    return redirect(url_for("quiz_management", name=name))







@app.route("/add_question/<id>/<name>", methods=["GET", "POST"])
def add_question(id, name):
    qz = get_quiz(id)  # Get the quiz details

    if request.method == "POST":
        question_statement = request.form.get("question_statement")
        option1 = request.form.get("option1")
        option2 = request.form.get("option2")
        option3 = request.form.get("option3")
        option4 = request.form.get("option4")
        correct_option = request.form.get("correct_option")

        # Ensure all fields are filled
        if not question_statement or not option1 or not option2 or not option3 or not option4 or not correct_option:
            return render_template("add_question.html", name=name, quiz=qz, msg="All fields are required!")

        # Create new question entry
        new_question = Question(
            quiz_id=id,
            question_statement=question_statement,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            correct_option=correct_option
        )

        db.session.add(new_question)
        db.session.commit()
        return redirect(url_for("quiz_management", name=name))

    return render_template("add_question.html", name=name, quiz=qz, msg="")




@app.route("/edit_question/<id>/<name>", methods=["GET", "POST"])
def edit_question(id, name):
    que=get_question(id) # Fetch question by ID

    if request.method == "POST":
        question_statement = request.form.get("question_statement")
        option1 = request.form.get("option1")
        option2 = request.form.get("option2")
        option3 = request.form.get("option3")
        option4 = request.form.get("option4")
        correct_option = request.form.get("correct_option")

        # Ensure all fields are filled
        if not question_statement or not option1 or not option2 or not option3 or not option4 or not correct_option:
            return render_template("edit_question.html", name=name, question=que, msg="All fields are required!")

        # Update question fields
        que.question_statement = question_statement
        que.option1 = option1
        que.option2 = option2
        que.option3 = option3
        que.option4 = option4
        que.correct_option = correct_option

        db.session.commit()
        return redirect(url_for("quiz_management", name=name))

    return render_template("edit_question.html", name=name, question=que, msg="")





@app.route("/delete_question/<id>/<name>", methods=["GET"])
def delete_question(id, name):
    que=get_question(id)  # Fetch question by ID

    db.session.delete(que)
    db.session.commit()

    return redirect(url_for("quiz_management", name=name))  # Redirect to quiz management page





# Other support function

def get_subjects():
    subjects=Subject.query.all()
    return subjects

def get_subject(id):
    subject=Subject.query.filter_by(id=id).first()
    return subject

def get_chapters():
    chapters=Chapter.query.all()
    return chapters

def get_chapter(id):
    chapter=Chapter.query.filter_by(id=id).first()
    return chapter

def get_quizzes():
    quizzes=Quiz.query.all()
    return quizzes

def get_quiz(id):
    quiz=Quiz.query.filter_by(id=id).first()
    return quiz

def get_question(id):
    question=Question.query.filter_by(id=id).first()
    return question
