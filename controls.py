from flask import Flask,session,request,render_template
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import os
import time
app=Flask(__name__)
app.config['UPLOAD_FOLDER']="static/image/"
app.config['MAX_CONTENT-PATH']=30000
app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:@localhost:3307/flaskblog"
db = SQLAlchemy(app)
class Photos(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(80), nullable=False)
@app.route("/")
def home():
    getphotos= Photos.query.all()
    return render_template("mypost.html", photos=getphotos)
@app.route("/uploads", methods=['POST','GET'])
def uploads():
    getphotos= Photos.query.all()
    if request.method=="POST":
        fname= request.files['file']
        fname.filename= str(time.time()).split('.')[0] +'.' + fname.filename.split('.')[-1]
        if fname:
            filename = secure_filename(fname.filename)
            fname.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            qry =Photos(fname=filename)
            db.session.add(qry)
            db.session.commit()
            return render_template("mypost.html",photos=getphotos)
        else:
            return render_template("mypost.html",name="File Not be selected",photos=getphotos)
    else:
        return render_template("mypost.html",photos=getphotos)
app.run(debug=True)
