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
                return redirect('/adminhome')
            elif ss ['usertype'] =='dealer':
                session['lid'] = ss['login_id']
                return redirect('/dealerhome')
            else:
                return '''<script> alert ('User not found');window.location="/"</script>'''
        else:
            return '''<script> alert ('User not found');window.location="/"</script>'''



    return render_template('index.html')












@app.route('/dealer_add', methods=['get','post'])
def dealer_add():
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











@app.route('/dealer_update/<b>',methods=['get','post'])
def dealer_update(b):
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











@app.route('/dealer_delete/<b>')
def dealer_delete(b):
    db=Db()
    db.delete("delete from dealer where login_id='"+b+"'")
    return redirect('/dealer_view')









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








@app.route('/adminhome')
def adminhome():
    return render_template('admin/adminview.html')











#****************************************************second module "dealer"****************************************************#

@app.route('/product_add',methods=['get','post'])
def product_add():
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








@app.route('/product_view')
def product_view():
    db=Db()
    ss=db.select("select * from product,dealer where product.dealer_id=dealer.login_id AND product.dealer_id='"+str(session['lid'])+"'")
    return render_template('dealer/product_view.html',data=ss)





@app.route('/product_update/<p_id>',methods=['get','post'])
def product_update(p_id):
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



@app.route('/product_delete/<p_id>')
def product_delete(p_id):
    db = Db()
    db.delete("delete from product where product_id='" + p_id + "'")
    return redirect('/product_view')





@app.route('/stock')
def view_stock():
    return render_template('dealer/stock.html')



@app.route('/view_orders')
def view_orders():
    return render_template('dealer/view_orders.html')




@app.route('/complaint_view')
def complaint_view():
    db=Db()
    se=db.select("select * from user,complaint where user.login_id=complaint.user_id")
    return render_template('dealer/complaint.html',data=se)




@app.route('/replay')
def replay():
    db=Db()
    return render_template('dealer/replay.html')





@app.route('/dealerhome')
def dealerhome():
    return render_template('dealer/dealer_home.html')

if __name__ == '__main__':
    app.run()

