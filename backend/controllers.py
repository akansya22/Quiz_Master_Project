from flask import Flask,render_template,request,url_for,redirect
from .models import *
from datetime import datetime
from flask import current_app as app


@app.route("/")
def home():
    return render_template("index.html")



@app.route("/login",methods=["GET","POST"])
def signin():
    if request.method=="POST":
        uname=request.form.get("user_name")
        pwd=request.form.get("password")
        usr=User_Info.query.filter_by(email=uname,password=pwd).first()
        if usr and usr.role==0: # Existed and admin
            return redirect(url_for("admin_dashboard",name=uname))
        elif usr and usr.role==1: # Existed and normal user
            return redirect(url_for("user_dashboard",name=uname,id=usr.id))
        else:
            return render_template("login.html",msg1="Invalide User Credentials...")
    return render_template("login.html",msg="")



@app.route("/register",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        uname=request.form.get("user_name")
        pwd=request.form.get("password")
        full_name=request.form.get("full_name")
        qualification=request.form.get("qualification")
        dob=request.form.get("dob")
        try:
            dob = datetime.strptime(dob, "%Y-%m-%d").date()  # Converting from YYYY-MM-DD format
        except ValueError:
            return render_template("signup.html", msg="Invalid Date format. Please use the correct format.")
        # Validate required fields
        if not uname or not pwd or not full_name:
            return render_template("signup.html",msg="All fields are required. Please fill out the form completely.")
        usr=User_Info.query.filter_by(email=uname).first()
        if usr:
            return render_template("signup.html",msg="Sorry, already register with this email!!! try to signup with another email.")
        new_user=User_Info(email=uname,password=pwd,full_name=full_name,qualification=qualification,dob=dob)
        db.session.add(new_user)
        db.session.commit()
        return render_template("login.html",msg2="Registration Successfull, try login now.")
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
    return render_template("user_dashboard.html",name=name)


# Other support function

def get_subjects():
    subjects=Subject.query.all()
    return subjects

def get_quizzes():
    quizzes=Quiz.query.all()
    return quizzes