from flask import Flask,render_template,request,session,redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import json
with open("config.json") as c:
    params=json.load(c)['params']
app= Flask(__name__)
if params['local_server']:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
    app.config['UPLOAD_FOLDER']="static/image/"
    app.config['MAX_CONTENT-PATH']=30000
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
db = SQLAlchemy(app)
app.secret_key = 'super-secret'
class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=False)
    email = db.Column(db.String(20), nullable=False)
class Post(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(12), nullable=False)
    content = db.Column(db.String(120), nullable=False)
    img_file=db.Column(db.String(50), nullable=True)
    date = db.Column(db.String(12), nullable=False)
    def __repr__(self):
        return f"{self.sno,self.title,self.slug,self.content,self.date}"


@app.route("/")
def home():
    record=Post.query.all()
    return  render_template("index.html",params=params,post=record)
@app.route("/about")
def about():
    return  render_template("about.html",params=params)

@app.route("/contact", methods = ['GET','POST'])
def contact():
    if(request.method=='POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contacts(name=name, phone_num = phone, msg = message, date= datetime.now(),email = email )
        db.session.add(entry)
        db.session.commit()
        return render_template("contact.html",success="Our executive contact to you coming soon !",params=params)
    else:
        return  render_template("contact.html",params=params)

@app.route("/post")
def post():
    post=Post.query.all()
    return  render_template("post.html",params=params,post=post)
@app.route("/addpost", methods=["GET","POST"])
def addpost():
    if request.method=="GET":
        return render_template("addpost.html",params=params,user=session)
    else:
        title=request.form.get('title')
        slug=request.form.get('slug')
        content= request.form.get('content')
        img_file= request.files['post_img']
        post=Post(title=title,slug=slug,content=content,img_file=img_file.filename,date=datetime.now())
        db.session.add(post)
        db.session.commit()
        post=Post.query.all()
        return render_template("dashboard.html",params=params,user=session,record=post)
@app.route("/login", methods=["POST","GET"])
def login():
    post=Post.query.all()
    if 'user' in session:
        return render_template("dashboard.html",params=params,user=session,record=post)
    if (request.method=="POST"):
        email=request.form.get('email')
        password = request.form.get('password')
        if (email==params['user_admin'] and password==params['user_pass']):
            session['user']=email
            return render_template("dashboard.html",params=params,user=session,record=post)
        else:
            return render_template('login.html',params=params)
    else:
        return render_template("login.html",params=params)
@app.route("/logout")
def logout():
    session.pop('user',None)
    return render_template("login.html",params=params)
@app.route("/delete/<string:delete_id>", methods=["GET"])
def delete(delete_id):
    mypost=Post.query.filter_by(sno=int(delete_id)).first()
    db.session.delete(mypost)
    db.session.commit()
    mypost=Post.query.all()
    return render_template("dashboard.html",params=params,record=mypost)
app.run(debug=True)