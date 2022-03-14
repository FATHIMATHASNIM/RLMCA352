from flask import Flask,render_template,request
import random
from DBConnection import Db

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('login.html')


@app.route('/dealer_add', methods=['get','post'])
def dealer_add():
    if request.method=="POST":
        name=request.form["textfield"]
        place=request.form["textfield2"]
        post=request.form["textfield3"]
        pin=request.form["textfield4"]
        phone=request.form["textfield5"]
        email=request.form["textfield6"]
        pasw = random.ranind(0000, 9999)
        db=Db()
        ss=db.insert("insert into login values ['','"+email+"','"+str(pasw)+"','dealer']")
    return render_template('admin/dealer_add_form.html')


@app.route('/dealer_update')
def dealer_update():
    return render_template('admin/dealer_update.html')


@app.route('/dealer_view')
def dealer_view_form():
    db=Db()
    ss=db.select("select * from dealer" )
    return render_template('admin/dealer_view_form.html',data=ss)


@app.route('/feedback')
def feedback():
    db=Db()
    ss=db.select("select * from feedback,user where feedback.user_id=user.login_id")
    return render_template('admin/feedback.html',data=ss)


@app.route('/viewregistereduser')
def viewregistereduser():
    db=Db()
    ss=db.select("select * from user")
    return render_template('admin/viewregistereduser.html',data=ss)


@app.route('/adminview')
def adminview():
    return render_template('admin/adminview.html')

if __name__ == '__main__':
    app.run()
