from unicodedata import name
from flask import Flask,render_template,flash, redirect,url_for,session,logging,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userList.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))
    created = db.Column(db.DateTime, default=datetime.utcnow)

class maids(db.Model):
    mid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    phone = db.Column(db.String(13))
    category = db.Column(db.String(20))
    address = db.Column(db.String(20))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        
        login = user.query.filter_by(email=email, password=password).first()
        if login is not None:
            return redirect(url_for("welcome"))
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form['uname']
        mail = request.form['email']
        passw = request.form['password']

        register = user(username = uname, email = mail, password = passw)
        db.session.add(register)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/adminpanel")
def adminpanel():
    return render_template("admin-panel.html")


@app.route("/adminlogin", methods=["GET", "POST"])
def adminlogin():
    if request.method == "POST":
        uname = request.form['uname']
        password = request.form['password']

        if (uname == "admin" and password == "admin"):
          return redirect(url_for("adminpanel"))

    return render_template("admin-login.html")    
    
@app.route("/viewusers")
def viewusers():
    allusers = user.query.all()
    return render_template("ad-viewusers.html", allusers = allusers)

@app.route("/addmaid", methods=["GET", "POST"])
def addmaid():
    if request.method == "POST":
        mName = request.form['m_name']
        mPhone = request.form['m_phone']
        mAddress = request.form['m_add']
        category = request.form['Category']

        newMaid = maids(name = mName, phone = mPhone, category = category, address = mAddress)
        db.session.add(newMaid)
        db.session.commit()

        return redirect(url_for("addmaid"))
    return render_template("addmaid.html")

@app.route("/viewmaids")
def viewmaids():
    allmaids = maids.query.all()
    return render_template("ad-viewmaids.html", allmaids = allmaids)

@app.route("/hire")
def hire():
    return render_template("hire.html")

@app.route("/hirelist", methods=["GET", "POST"])
def hirelist():
    sCategory = request.form['SCategory']
    selectmaids = maids.query.filter_by(category = sCategory).all()
    return render_template("hirelist.html",selectmaids = selectmaids)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, port=8000)