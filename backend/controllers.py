from flask import render_template, request, url_for, redirect, current_app as app, session
from backend.models import *
from datetime import date, datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt



@app.route("/")
def home():
    return render_template("index.html")




@app.route("/login",methods=["GET","POST"])
def signin():
    if request.method=="POST":
        email=request.form.get("email")
        pwd=request.form.get("password")
        usr=User_Info.query.filter_by(email=email,password=pwd).first()
        if usr and usr.role==0:
            return redirect(url_for("admin_dashboard",name=email))
        elif usr and usr.role==1:
            return redirect(url_for("user_dashboard",name=email,user_id=usr.id))
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
            dob = datetime.strptime(dob, "%Y-%m-%d").date()
        except ValueError:
            return render_template("signup.html", msg="Invalid Date format. Please use the correct format.")
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




@app.route("/edit_chapter/<id>/<name>",methods=["GET","POST"])
def edit_chapter(id,name):
    c = get_chapter(id)
    subject_id = c.subject_id
    chapters = Chapter.query.filter_by(subject_id=subject_id).all()

    if request.method=="POST":
        new_name=request.form.get("new_name")
        chapter_no=request.form.get("chapter_no")
        c.new_name=new_name
        c.chapter_no=chapter_no
        db.session.commit()

        return redirect(url_for("admin_dashboard",name=name))
    
    return render_template("edit_chapter.html",chapter=c,name=name,chapters=chapters)




@app.route("/delete_chapter/<id>/<name>",methods=["GET","POST"])
def delete_chapter(id,name):
    c=get_chapter(id)
    db.session.delete(c)
    db.session.commit()

    return redirect(url_for("admin_dashboard",name=name))





@app.route('/quiz_management/<name>')
def quiz_management(name):
    quizzes = Quiz.query.all()

    return render_template("quiz_management.html",name=name,quizzes=quizzes)





@app.route("/quiz/<name>",methods=["POST","GET"])
def add_quiz(name):
    if request.method == "POST":
        chapter_id = request.form.get("chapter_id")
        chapter = Chapter.query.filter_by(id=chapter_id).first()

        if chapter:
            chapter_name = chapter.chapter_name
        else:
            chapter_name = None

        quiz_title = request.form.get("quiz_title")
        duration = request.form.get("duration")
        date_of_quiz = request.form.get("date_of_quiz")
        date_of_quiz = datetime.strptime(date_of_quiz, "%Y-%m-%d").date()
        total_questions = request.form.get("total_questions")

        new_quiz = Quiz(chapter_id=chapter_id,chapter_name=chapter_name,quiz_title=quiz_title,duration=duration,date_of_quiz=date_of_quiz,total_questions=total_questions)

        db.session.add(new_quiz)
        db.session.commit()
        return redirect(url_for("quiz_management",name=name))
    
    chapters_with_quizzes = {quiz.chapter_id for quiz in Quiz.query.all()}
    chapters = Chapter.query.filter(~Chapter.id.in_(chapters_with_quizzes)).all()

    return render_template("add_quiz.html",name=name,chapters=chapters)




@app.route("/edit_quiz/<quiz_id>/<name>",methods=["GET","POST"])
def edit_quiz(quiz_id, name):
    quiz = Quiz.query.get_or_404(quiz_id)

    if request.method == "POST":
        chapter_id = request.form.get("chapter_id")
        chapter = Chapter.query.filter_by(id=chapter_id).first()

        if chapter:
            chapter_name = chapter.chapter_name
        else:
            chapter_name = None

        quiz.chapter_id = chapter_id
        quiz.chapter_name = chapter_name
        quiz.quiz_title = request.form.get("quiz_title")
        quiz.duration = request.form.get("duration")
        quiz.date_of_quiz = datetime.strptime(request.form.get("date_of_quiz"), "%Y-%m-%d").date()
        quiz.total_questions = request.form.get("total_questions")
        db.session.commit()
        return redirect(url_for("quiz_management",name=name))

    chapters_with_quizzes = {q.chapter_id for q in Quiz.query.all()} - {quiz.chapter_id}
    chapters = Chapter.query.filter(~Chapter.id.in_(chapters_with_quizzes)).all()

    return render_template("edit_quiz.html",name=name,quiz=quiz,chapters=chapters)





@app.route('/delete_quiz/<id>/<name>',methods=["GET","POST"])
def delete_quiz(id,name):
    qz = get_quiz(id)
    db.session.delete(qz)
    db.session.commit()

    return redirect(url_for("quiz_management",name=name))





@app.route("/add_question/<id>/<name>",methods=["GET","POST"])
def add_question(id,name):
    qz = get_quiz(id)

    if request.method == "POST":
        question_statement = request.form.get("question_statement")
        option1 = request.form.get("option1")
        option2 = request.form.get("option2")
        option3 = request.form.get("option3")
        option4 = request.form.get("option4")
        correct_option = request.form.get("correct_option")

        if not question_statement or not option1 or not option2 or not option3 or not option4 or not correct_option:
            return render_template("add_question.html", name=name, quiz=qz, msg="All fields are required!")
        
        new_question = Question(quiz_id=id,question_statement=question_statement,option1=option1,option2=option2,option3=option3,option4=option4,correct_option=correct_option)
        db.session.add(new_question)
        db.session.commit()

        return redirect(url_for("quiz_management",name=name))

    return render_template("add_question.html",name=name,quiz=qz, msg="")




@app.route("/edit_question/<id>/<name>",methods=["GET","POST"])
def edit_question(id,name):
    que=get_question(id)
    if request.method == "POST":
        question_statement = request.form.get("question_statement")
        option1 = request.form.get("option1")
        option2 = request.form.get("option2")
        option3 = request.form.get("option3")
        option4 = request.form.get("option4")
        correct_option = request.form.get("correct_option")

        if not question_statement or not option1 or not option2 or not option3 or not option4 or not correct_option:
            return render_template("edit_question.html",name=name,question=que,msg="All fields are required!")

        que.question_statement = question_statement
        que.option1 = option1
        que.option2 = option2
        que.option3 = option3
        que.option4 = option4
        que.correct_option = correct_option
        db.session.commit()

        return redirect(url_for("quiz_management",name=name))

    return render_template("edit_question.html",name=name,question=que,msg="")





@app.route("/delete_question/<id>/<name>",methods=["GET"])
def delete_question(id,name):
    que=get_question(id)
    db.session.delete(que)
    db.session.commit()

    return redirect(url_for("quiz_management",name=name))




@app.route("/admin/user_details/<name>")
def admin_user_details(name):
    users = get_user_details()
    return render_template("admin_user_details.html",users=users,name=name)




@app.route("/admin_summary/<name>")
def admin_summary(name):
    plot = get_admin_summary()
    plot.savefig("./static/images/admin_summary.jpeg")
    plot.clf()
    return render_template("admin_summary.html",name=name)























# Common route for user dashboard
@app.route("/user/<user_id>/<name>")
def user_dashboard(user_id,name):
    quizzes=get_quizzes()
    date_today=date.today()

    return render_template("user_dashboard.html",name=name,quizzes=quizzes,date_today=date_today,user_id=user_id)




@app.route('/view_quiz/<quiz_id>/<name>/<user_id>')
def view_quiz(quiz_id,name,user_id):
    quiz=get_quiz(quiz_id) 

    return render_template("view_quiz.html",quiz=quiz,name=name,user_id=user_id)




@app.route("/start_quiz/<quiz_id>/<name>/<int:question_index>/<user_id>")
def start_quiz(quiz_id,name,question_index,user_id):
    quiz = get_quiz(quiz_id)
    questions = get_questions(quiz_id)
    total_questions = len(questions)
    question = questions[question_index]
    user = get_user(user_id)

    return render_template("start_quiz.html",quiz=quiz,question=question,name=name,question_index=question_index,total=total_questions,user=user,user_id=user_id)




@app.route("/save_answer/<quiz_id>/<name>/<int:question_index>/<user_id>",methods=["POST"])
def save_answer(quiz_id,name,question_index,user_id):
    selected_answer = request.form.get("answer")
    if "quiz_answers" not in session:
        session["quiz_answers"] = {}
    session["quiz_answers"][f"quiz_{quiz_id}_q{question_index}"] = int(selected_answer)
    total_questions = len(get_questions(quiz_id))
    if question_index + 1 < total_questions:
        return redirect(url_for("start_quiz",quiz_id=quiz_id,name=name,question_index=question_index + 1,user_id=user_id))
    else:
        return redirect(url_for("submit_quiz",quiz_id=quiz_id,name=name,user_id=user_id))

  


@app.route("/submit_quiz/<quiz_id>/<name>/<user_id>")
def submit_quiz(quiz_id, name, user_id):
    user = get_user(user_id)
    answers = session.get("quiz_answers", {})
    total_questions = len(get_questions(quiz_id))
    correct_answers = 0

    for index in range(total_questions):
        question = get_questions(quiz_id)[index]
        correct_option = question.correct_option
        user_answer = answers.get(f"quiz_{quiz_id}_q{index}")
        if user_answer == correct_option:
            correct_answers += 1

    percentage = (correct_answers / total_questions) * 100
    pass_fail_status = "Pass" if percentage >= 40 else "Fail"

    existing_score = Score.query.filter_by(quiz_id=quiz_id, user_id=user.id).first()

    if existing_score:
        existing_score.total_scored = correct_answers
        existing_score.total_possible_score = total_questions
        existing_score.percentage_scored = percentage
        existing_score.pass_fail_status = pass_fail_status
        existing_score.time_stamp = datetime.now()
    else:
        new_score = Score(quiz_id=quiz_id,user_id=user.id,total_scored=correct_answers,total_possible_score=total_questions,percentage_scored=percentage,pass_fail_status=pass_fail_status)
        db.session.add(new_score)

    db.session.commit()
    session.pop("quiz_answers", None)  # Clear the session after submission

    return render_template("quiz_result.html", name=name, user=user, score=new_score if not existing_score else existing_score, user_id=user_id)




@app.route("/scores/<user_id>/<name>")
def user_scores(user_id,name):
    scores=get_scores(user_id)

    return render_template('scores.html',scores=scores,name=name,user_id=user_id)




@app.route("/user_summary/<user_id>/<name>")
def user_summary(user_id,name):
    plot = get_user_summary(user_id)
    plot.savefig("./static/images/user_summary.jpeg")
    plot.clf()
    return render_template("user_summary.html",name=name,user_id=user_id)






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


def get_quiz(quiz_id):
    quiz=Quiz.query.filter_by(id=quiz_id).first()
    return quiz


def get_questions(quiz_id):
    return Question.query.filter_by(quiz_id=quiz_id).all()


def get_question(id):
    question=Question.query.filter_by(id=id).first()
    return question


def get_user_by_name(email):
    return User_Info.query.filter_by(email=email).first()


def get_user(user_id):
    user=User_Info.query.filter_by(id=user_id).first()
    return user


def get_scores(user_id):
    scores = Score.query.filter_by(user_id=user_id).all()
    return scores


def get_user_details():
    users = User_Info.query.all()
    user_data = []

    for user in users:
        scores = get_scores(user.id)
        total_quizzes = len(scores)
        avg_score = round(sum(score.percentage_scored for score in scores) / total_quizzes, 2) if total_quizzes else 0
        user_data.append({"id": user.id,"name": user.full_name,"email": user.email,"total_quizzes": total_quizzes,"average_score": avg_score})
    return user_data


def get_user_summary(user_id):
    scores = get_scores(user_id)
    summary = {}
    for score in scores:
        chapter_name = score.quiz.chapter.chapter_name
        summary[chapter_name] = score.percentage_scored
    x_names = list(summary.keys())
    y_percentages = list(summary.values())
    plt.figure(figsize=(20, 12))
    plt.bar(x_names, y_percentages, color="blue", width=0.5)
    plt.xlabel("Chapters", fontsize=40, fontweight='bold')
    plt.ylabel("Percentage (%)", fontsize=30, fontweight='bold')
    plt.xticks(rotation=30, ha="right", fontsize=15)
    plt.yticks(fontsize=15)

    plt.tight_layout(pad=2)
    return plt


def get_admin_summary():
    results = db.session.query(
        Chapter.chapter_name,
        func.max(Score.percentage_scored).label("top_score")
    ).join(Quiz, Quiz.id == Score.quiz_id) \
     .join(Chapter, Chapter.id == Quiz.chapter_id) \
     .group_by(Chapter.chapter_name) \
     .all()

    summary = {chapter: score for chapter, score in results}
    x_names = list(summary.keys())
    y_scores = list(summary.values())

    plt.figure(figsize=(20, 12))
    plt.bar(x_names, y_scores, color="green", width=0.5)
    plt.xlabel("Chapters", fontsize=40, fontweight='bold')
    plt.ylabel("Top Scores (%)", fontsize=30, fontweight='bold')
    plt.xticks(rotation=30, ha="right", fontsize=20)
    plt.yticks(fontsize=20)

    plt.tight_layout(pad=2)
    return plt

