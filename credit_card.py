import datetime
from flask import Flask, render_template, request, redirect,session
import random

from DBConnection import Db

app = Flask(__name__)
app.secret_key="abc"# #










@app.route('/',methods=['get','post'])
def hello_world():
    if request.method=="POST":
        username=request.form["textfield"]
        password=request.form["textfield2"]
        db=Db()
        ss=db.selectOne("select * from login where username='"+username+"'and password='"+password+"'")
        if ss is not None:
            if ss['usertype']=='admin':
                session['lg'] = "log"
                return redirect('/adminhome')
            elif ss ['usertype'] =='dealer':
                session['lg']="log"
                session['lid'] = ss['login_id']
                return redirect('/dealerhome')
            else:
                return '''<script> alert ('User not found');window.location="/"</script>'''
        else:
            return '''<script> alert ('User not found');window.location="/"</script>'''



    return render_template('index.html')












@app.route('/dealer_add', methods=['get','post'])
def dealer_add():
    if session['lg']=="log":

        if request.method=="POST":
            name=request.form["textfield"]
            place=request.form["textfield2"]
            post=request.form["textfield3"]
            pin=request.form["textfield4"]
            phone=request.form["textfield5"]
            email=request.form["textfield6"]
            pasw = random.randint(0000, 9999)
            db=Db()
            ss = db.insert("INSERT INTO login (username,PASSWORD,usertype) VALUES('"+email+"','"+str(pasw)+"','dealer')")
            db.insert("INSERT INTO dealer(login_id,dealer_name,d_place,d_post,d_phone,d_pin,d_email) VALUES('"+str(ss)+"','"+name+"','"+place+"','"+post+"','"+phone+"','"+pin+"','"+email+"')")
            return '''<script> alert ('Successfully Registered');window.location="/dealer_add"</script>'''
        return render_template('admin/dealer_add_form.html')
    else:
        return redirect('/')











@app.route('/dealer_update/<b>',methods=['get','post'])
def dealer_update(b):
    if session['lg'] == "log":
        if request.method=="POST":
            name=request.form["textfield"]
            place=request.form["textfield2"]
            post=request.form["textfield3"]
            pin=request.form["textfield4"]
            phone=request.form["textfield5"]
            email=request.form["textfield6"]
            db=Db()
            db.update("update dealer set dealer_name='"+name+"',d_place='"+place+"',d_post='"+post+"',d_phone='"+phone+"',d_pin='"+pin+"',d_email='"+email+"' where login_id='"+b+"'")
            return '''<script> alert ('update successfully');window.location="/dealer_view"</script>'''
        else:
            db=Db()
            ss=db.selectOne("select * from dealer where login_id='"+b+"'" )
            return render_template('admin/dealer_update.html',data=ss)
    else:
        return redirect('/')











@app.route('/dealer_delete/<b>')
def dealer_delete(b):
    if session['lg'] == "log":
        db=Db()
        db.delete("delete from dealer where login_id='"+b+"'")
        return redirect('/dealer_view')
    else:
        return redirect('/')









@app.route('/dealer_view')
def dealer_view_form():
    if session['lg'] == "log":
        db=Db()
        ss=db.select("select * from dealer" )
        return render_template('admin/dealer_view_form.html',data=ss)
    else:
        return redirect('/')








@app.route('/feedback')
def feedback():
    if session['lg'] == "log":
        db=Db()
        ss=db.select("select * from feedback,user where feedback.user_id=user.login_id")
        return render_template('admin/feedback.html',data=ss)
    return redirect('/')







@app.route('/viewregistereduser')
def viewregistereduser():
    if session['lg'] == "log":
        db=Db()
        ss=db.select("select * from user")
        return render_template('admin/viewregistereduser.html',data=ss)
    else:
        return redirect('/')








@app.route('/adminhome')
def adminhome():
    if session['lg']=="log":
        return render_template('admin/dashboard.html')
    else:
        return redirect('/')











#****************************************************second module "dealer"****************************************************#

@app.route('/product_add',methods=['get','post'])
def product_add():
    if session['lg']=="log":
        if request.method == 'POST':
            name=request.form["textfield"]
            category=request.form["select"]
            freshness=request.form["RadioGroup1"]
            quant=request.form["textfield10"]
            image=request.files["fileField"]
            date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
            image.save(r"C:\Users\USER\PycharmProjects\credit_card\static\productimg\\"+date+'.jpg')
            sd='/static/productimg/'+date+'.jpg'
            descr=request.form["textarea"]
            price=request.form["textfield2"]
            db=Db()
            ss=db.insert("insert into product(prod_name,prod_quantity,price,dealer_id,image,category,fresh,details) values ('"+name+"','"+quant+"','"+price+"','"+str(session['lid'])+"','"+str(sd)+"','"+category+"','"+freshness+"','"+descr+"')")
            return '''<script>alert ('product add');window.location="/dealerhome"</script>'''
        else:
            return render_template('dealer/product_add.html')
    else:
        return redirect('/')








@app.route('/product_view')
def product_view():
    if session['lg']=="log":
        db=Db()
        ss=db.select("select * from product,dealer where product.dealer_id=dealer.login_id AND product.dealer_id='"+str(session['lid'])+"'")
        return render_template('dealer/product_view.html',data=ss)
    else:
        return redirect('/')





@app.route('/product_update/<p_id>',methods=['get','post'])
def product_update(p_id):
    if session['lg'] == "log":
        if request.method == "POST":
            name = request.form["textfield"]
            category = request.form["select"]
            freshness = request.form["RadioGroup1"]
            quant = request.form["textfield10"]
            image = request.files["file"]
            date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
            image.save(r"C:\Users\USER\PycharmProjects\credit_card\static\productimg\\" + date + '.jpg')
            sd = '/static/productimg/' + date + '.jpg'
            descr = request.form["textarea"]
            price = request.form["textfield2"]
            db=Db()
            db.update("update product set prod_name='"+name+"',prod_quantity='"+quant+"',price='"+price+"',image='"+str(sd)+"',category='"+category+"',fresh='"+freshness+"',details='"+descr+"' where product_id='"+p_id+"'")
            return '''<script> alert ('update successfully');window.location="/product_view"</script>'''
        else:
            db=Db()
            ss=db.selectOne("select * from product where product_id='"+p_id+"'")
            return render_template('dealer/product_update.html',data=ss)
    else:
        return redirect('/')



@app.route('/product_delete/<p_id>')
def product_delete(p_id):
    if session['lg'] == "log":
        db = Db()
        db.delete("delete from product where product_id='" + p_id + "'")
        return redirect('/product_view')
    else:
        return redirect('/')





@app.route('/stock')
def view_stock():
    if session['lg'] == "log":
        return render_template('dealer/stock.html')
    else:
        return redirect('/')



@app.route('/view_orders')
def view_orders():
    if session['lg'] == "log":
        db=Db()
        ss=db.select("select * from cart,bookings,product,user where cart.user_id=user.login_id AND cart.cart_id=bookings.cart_id AND cart.prod_id=product.product_id AND cart.c_status='booked' AND bookings.b_status='booked'")
        return render_template('dealer/view_orders.html',data=ss)
    else:
        return redirect('/')




@app.route('/complaint_view')
def complaint_view():
    if session['lg'] == "log":
        db=Db()
        se=db.select("select * from user,complaint where user.login_id=complaint.user_id and complaint.replay='pending'")
        return render_template('dealer/complaint.html',data=se)
    else:
        return redirect('/')




@app.route('/replay/<complaint_id>',methods=['get','post'])
def replay(complaint_id):
    if session['lg'] == "log":
        if request.method=="POST":
            replay=request.form["textarea"]
            db=Db()
            db.update("update complaint set replay='"+replay+"',rep_date=curdate() where comp_id='"+complaint_id+"'")
            return '''<script> alert ('successfully updated');window.location="/complaint_view"</script>'''#window.location="/comaplint_view"-rule name#
        else:
            db=Db()
            ss=db.selectOne("select * from complaint where comp_id='"+complaint_id+"'")
            return render_template('dealer/replay.html',data=ss)
    else:
        return redirect('/')





@app.route('/dealerhome')
def dealerhome():
    if session['lg']=="log":
        return render_template('dealer/dashboard_dealer.html')
    else:
        return redirect('/')




@app.route('/logout')
def logout():
    session.clear()
    session['lg']=" "

    return redirect('/')



if __name__ == '__main__':
    app.run()




