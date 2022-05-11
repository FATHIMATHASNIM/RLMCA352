import datetime
from flask import Flask, render_template, request, redirect, session, jsonify
import random

from DBConnection import Db

app = Flask(__name__)
app.secret_key = "abc"
# #
otp1=1
sid1=0
#________________login rule___________________
@app.route('/', methods=['get', 'post'])
def hello_world():
    if request.method == "POST":
        username = request.form["textfield"]
        password = request.form["textfield2"]
        db = Db()
        ss = db.selectOne("select * from login where username='" + username + "'and password='" + password + "'")
        if ss is not None:
            if ss['usertype'] == 'admin':
                session['lg'] = "log"
                return redirect('/adminhome')
            elif ss['usertype'] == 'dealer':
                session['lg'] = "log"
                session['lid'] = ss['login_id']
                return redirect('/dealerhome')
            elif ss['usertype']=='user':
                session['lid']=ss['login_id']
                return redirect('/userhome')
            else:
                return '''<script> alert ('User not found');window.location="/"</script>'''
        else:
            return '''<script> alert ('User not found');window.location="/"</script>'''

    return render_template('index.html')


@app.route('/dealer_add', methods=['get', 'post'])
def dealer_add():
    if session['lg'] == "log":

        if request.method == "POST":
            name = request.form["textfield"]
            place = request.form["textfield2"]
            post = request.form["textfield3"]
            pin = request.form["textfield4"]
            phone = request.form["textfield5"]
            email = request.form["textfield6"]
            pasw = random.randint(0000, 9999)
            db = Db()
            ss = db.insert(
                "INSERT INTO login (username,PASSWORD,usertype) VALUES('" + email + "','" + str(pasw) + "','dealer')")
            db.insert("INSERT INTO dealer(login_id,dealer_name,d_place,d_post,d_phone,d_pin,d_email) VALUES('" + str(
                ss) + "','" + name + "','" + place + "','" + post + "','" + phone + "','" + pin + "','" + email + "')")
            return '''<script> alert ('Successfully Registered');window.location="/dealer_add"</script>'''
        return render_template('admin/dealer_add_form.html')
    else:
        return redirect('/')


@app.route('/dealer_update/<b>', methods=['get', 'post'])
def dealer_update(b):
    if session['lg'] == "log":
        if request.method == "POST":
            name = request.form["textfield"]
            place = request.form["textfield2"]
            post = request.form["textfield3"]
            pin = request.form["textfield4"]
            phone = request.form["textfield5"]
            email = request.form["textfield6"]
            db = Db()
            db.update(
                "update dealer set dealer_name='" + name + "',d_place='" + place + "',d_post='" + post + "',d_phone='" + phone + "',d_pin='" + pin + "',d_email='" + email + "' where login_id='" + b + "'")
            return '''<script> alert ('update successfully');window.location="/dealer_view"</script>'''
        else:
            db = Db()
            ss = db.selectOne("select * from dealer where login_id='" + b + "'")
            return render_template('admin/dealer_update.html', data=ss)
    else:
        return redirect('/')


@app.route('/dealer_delete/<b>')
def dealer_delete(b):
    if session['lg'] == "log":
        db = Db()
        db.delete("delete from dealer where login_id='" + b + "'")
        return redirect('/dealer_view')
    else:
        return redirect('/')


@app.route('/dealer_view')
def dealer_view_form():
    if session['lg'] == "log":
        db = Db()
        ss = db.select("select * from dealer")
        return render_template('admin/dealer_view_form.html', data=ss)
    else:
        return redirect('/')


@app.route('/feedback')
def feedback():
    if session['lg'] == "log":
        db = Db()
        ss = db.select("select * from feedback,user where feedback.user_id=user.login_id")
        return render_template('admin/feedback.html', data=ss)
    return redirect('/')


@app.route('/viewregistereduser')
def viewregistereduser():
    if session['lg'] == "log":
        db = Db()
        ss = db.select("select * from user")
        return render_template('admin/viewregistereduser.html', data=ss)
    else:
        return redirect('/')


@app.route('/adminhome')
def adminhome():
    if session['lg'] == "log":
        return render_template('admin/dashboard.html')

    else:
        return redirect('/')


# ****************************************************second module "dealer"****************************************************#

@app.route('/product_add', methods=['get', 'post'])
def product_add():
    if session['lg'] == "log":
        if request.method == 'POST':
            name = request.form["textfield"]
            category = request.form["select"]
            freshness = request.form["RadioGroup1"]
            quant = request.form["textfield10"]
            image = request.files["fileField"]
            date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
            image.save(r"C:\Users\USER\PycharmProjects\credit_card\static\productimg\\" + date + '.jpg')
            sd = '/static/productimg/' + date + '.jpg'
            descr = request.form["textarea"]
            price = request.form["textfield2"]
            db = Db()
            ss = db.insert(
                "insert into product(prod_name,prod_quantity,price,dealer_id,image,category,fresh,details) values ('" + name + "','" + quant + "','" + price + "','" + str(
                    session['lid']) + "','" + str(sd) + "','" + category + "','" + freshness + "','" + descr + "')")
            return '''<script>alert ('product add');window.location="/product_view"</script>'''
        else:
            return render_template('dealer/product_add.html')
    else:
        return redirect('/')


@app.route('/product_view')
def product_view():
    if session['lg'] == "log":
        db = Db()
        ss = db.select(
            "select * from product,dealer where product.dealer_id=dealer.login_id AND product.dealer_id='" + str(
                session['lid']) + "'")
        return render_template('dealer/product_view.html', data=ss)
    else:
        return redirect('/')


@app.route('/product_update/<p_id>', methods=['get', 'post'])
def product_update(p_id):
    if session['lg'] == "log":
        if request.method == "POST":
            name = request.form["textfield"]
            category = request.form["select"]
            freshness = request.form["RadioGroup1"]
            quant = request.form["textfield10"]


            descr = request.form["textarea"]
            price = request.form["textfield2"]

            if 'file' in request.files:
                image = request.files["file"]
                if image.filename!='':
                    date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
                    image.save(r"C:\Users\USER\PycharmProjects\credit_card\static\productimg\\" + date + '.jpg')
                    sd = '/static/productimg/' + date + '.jpg'
                    db = Db()
                    db.update("update product set prod_name='" + name + "',prod_quantity='" + quant + "',price='" + price + "',image='" + str(sd) + "',category='" + category + "',fresh='" + freshness + "',details='" + descr + "' where product_id='" + p_id + "'")
                    return '''<script> alert ('update successfully');window.location="/product_view"</script>'''
                else:
                    db = Db()
                    db.update("update product set prod_name='" + name + "',prod_quantity='" + quant + "',price='" + price + "',category='" + category + "',fresh='" + freshness + "',details='" + descr + "' where product_id='" + p_id + "'")
                    return '''<script> alert ('update successfully');window.location="/product_view"</script>'''
            else:
                db = Db()
                db.update(
                    "update product set prod_name='" + name + "',prod_quantity='" + quant + "',price='" + price + "',category='" + category + "',fresh='" + freshness + "',details='" + descr + "' where product_id='" + p_id + "'")
                return '''<script> alert ('update successfully');window.location="/product_view"</script>'''

        else:
            db = Db()
            ss = db.selectOne("select * from product where product_id='" + p_id + "'")
            return render_template('dealer/product_update.html', data=ss)
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
        db=Db()
        qry="SELECT `product`.*,`stock`.* FROM `product` INNER JOIN `stock` ON `product`.`product_id`=`stock`.`product_id`"
        res=db.select(qry)
        return render_template('dealer/stock.html',pdct=res)
    else:
        return redirect('/')

@app.route('/update_stock/<id>')
def update_stock(id):
    db=Db()
    qry="SELECT * FROM `stock` WHERE `stock_id`='"+str(id)+"'"
    res=db.selectOne(qry)
    return render_template('dealer/update_stock.html',stock=res)

@app.route('/update_stock_post',methods=['post'])
def update_stock_post():
    s_id=request.form['s_id']
    stock=request.form['textfield']
    db = Db()
    qry="UPDATE `stock` SET `stock_quantity`='"+stock+"' WHERE `stock_id`='"+str(s_id)+"'"
    res=db.update(qry)
    return '''<script>alert('updated');window.location='/stock'</script>'''


@app.route('/addstock/<id>')
def addstock(id):
    db=Db()
    qry="SELECT * FROM `product` WHERE `product_id`='"+str(id)+"'"
    res=db.selectOne(qry)
    return render_template('dealer/add_stock.html',data=res)

@app.route('/addstock_post',methods=['post'])
def addstock_post():
    pdct_id=request.form['pdct_id']
    stock=request.form['textfield']
    db = Db()
    qry="INSERT INTO `stock` (`product_id`,`stock_quantity`) VALUES('"+str(pdct_id)+"','"+stock+"')"
    res=db.insert(qry)
    return render_template('dealer/add_stock.html',data=res)


@app.route('/view_orders')
def view_orders():
    if session['lg'] == "log":
        db = Db()
        ss = db.select("select * from cart,bookings,product,user where cart.user_id=user.login_id AND cart.cart_id=bookings.cart_id AND cart.prod_id=product.product_id AND cart.c_status='booked' AND bookings.b_status='booked'")
        print(ss)
        return render_template('dealer/view_orders.html', data=ss)
    else:
        return redirect('/')


@app.route('/complaint_view')
def complaint_view():
    if session['lg'] == "log":
        db = Db()
        se = db.select(
            "select * from user,complaint where user.login_id=complaint.user_id")
        return render_template('dealer/complaint.html', data=se)
    else:
        return redirect('/')


@app.route('/replay/<complaint_id>', methods=['get', 'post'])
def replay(complaint_id):

    if session['lg'] == "log":
        if request.method == "POST":
            c_id = request.form['c_id']
            replay = request.form["textarea"]
            db = Db()
            db.update("update complaint set replay='" + replay + "',rep_date=curdate() where comp_id='" +str(c_id)+ "'")
            return '''<script> alert ('successfully updated');window.location="/complaint_view"</script>'''  # window.location="/comaplint_view"-rule name#
        else:
            db = Db()
            ss = db.selectOne("select * from complaint where comp_id='" + complaint_id + "'")
            return render_template('dealer/replay.html', data=ss)
    else:
        return redirect('/')


@app.route('/dealerhome')
def dealerhome():
    if session['lg'] == "log":
        return render_template('dealer/dashboard_dealer.html')
    else:
        return redirect('/')


@app.route('/logout')
def logout():
    session.clear()
    session['lg'] = " "

    return redirect('/')


# ---------------------------------------third module("user module")--------------------------------------------------#

@app.route('/userhome')
def userhome():
    # if session['lg'] == "log":
    return render_template('user/user_home.html')
    #else:
     #   return redirect('/')



@app.route('/user_register', methods=['get','post'])
def u_register():
    if request.method=="POST":
        name = request.form["textfield"]
        a=request.files["a"]
        dob=request.form["textfield2"]
        place=request.form["textarea6"]
        post = request.form["textarea7"]
        phone = request.form["textfield3"]
        pin = request.form["textfield4"]
        email = request.form["textfield5"]
        passw = request.form["textfield8"]


        db=Db()
        us=db.selectOne("select * from login where username='"+email+"'")
        if us is not None:
            return '''<script>alert('user aready registered');window.location="/user_register"</script>'''

        else:
            sb=db.insert("insert into login (username,password,usertype) values ('"+email+"','"+passw+"','user')")
            a.save("C:\\Users\\USER\\PycharmProjects\\credit_card\\static\\user\\" +str(sb)+".jpg")
            path="/static/user/"+str(sb)+".jpg"
            sd=db.insert("insert into user (login_id,user_name,dob,place,post,phone,email,pin,photo) values ('"+str(sb)+"','"+name+"','"+dob+"','"+place+"','"+post+"','"+phone+"','"+email+"','"+pin+"','"+path+"')")
            return '''<script>alert ('Registered Successfully');window.location="/"</script>'''
    else:
        return render_template('user/user_regform.html')


@app.route('/view_product')
def view_product():
    db = Db()
    ss = db.select("select * from product,dealer where product.dealer_id=dealer.login_id ")
    return render_template('user/user_product_view.html',data=ss)


@app.route('/book/<d>',methods=['get','post'])
def book(d):
    if request.method=="POST":
        quantity=request.form["textarea"]

        db=Db()
        sd = db.selectOne("select * from cart where user_id='" + str(session['lid']) + "' and prod_id='" + d + "'")
        sa=db.selectOne("select * from product where product_id='"+d+"'")
        res= str (sa['prod_quantity'])
        if sd is not None:
            if res >= quantity:
                db.update("update cart set quantity='"+quantity+"' where user_id='"+str(session['lid'])+"' and prod_id='"+d+"'")
                print(sd)
                return '''<script>alert("updated");window.location="/userhome"</script>'''
            else:
                return '''<script>alert("enter proper quantity");window.location="/view_product"</script>'''
        else:
            if res >= quantity:
                ss=db.insert ("insert into cart (prod_id,user_id,quantity,c_status)VALUES ('"+d+"','"+str(session['lid'])+"','"+quantity+"','add to cart')")
                se=db.insert("insert into bookings (cart_id,amount, b_status) VALUE ('"+str(ss)+"',0,'pending')")
                return '''<script>alert("product add to cart");window.location="/view_cart"</script>'''
            else:
                return '''<script>alert("quantity is high!");window.location="/view_product"</script>'''

    else:
        db=Db()
        ss=db.selectOne("select * from product where product_id='"+d+"'")
        return render_template('user/add_quantity.html',data=ss)



@app.route('/view_cart')
def view_cart():
    db=Db()
    sf = db.select("select * from product,user, cart where cart.user_id=user.login_id and product.product_id=cart.prod_id  and cart.user_id='"+str(session['lid'])+"'")
    print("select * from product,user, cart where cart.user_id=user.login_id and product.product_id=cart.prod_id and  cart.user_id='"+str(session['lid'])+"'")
    return render_template('user/cart.html',data=sf)


@app.route('/bookings')
def bookings():
    db=Db()
    bc=db.select("select * from bookings,cart,product where bookings.cart_id=cart.cart_id and bookings.b_status='booked' and cart.c_status='booked' and bookings.amount!=0 and cart.prod_id=product.product_id")
    return render_template('user/booking.html',data=bc)


@app.route('/card_details')
def card_details():
    db=Db()
    sa=db.select("select * from credit_card where user_id='"+str(session['lid'])+"' ")
    return render_template('user/card.html',data=sa)



@app.route('/card_update/<c_id>',methods=['get','post'])
def card_update(c_id):
    if request.method=="POST":
        cardnumber=request.form["textfield"]
        cvv=request.form["textfield2"]
        expirydate=request.form["textfield3"]
        # num = request.form["num"]
        db=Db()
        db.update("update credit_card set card_number='"+cardnumber+"',cvv='"+cvv+"',expiry_date='"+expirydate+"' where card_id='"+c_id+"'")
        return '''<script>alert("update successfully!");window.location="/card_details"</script>'''
    else:
        db=Db()
        cd=db.selectOne("select * from credit_card where card_id='"+c_id+"'")
        return render_template('user/card_update.html',data=cd)

@app.route('/card_add',methods=['get','post'])
def card_add():
    if request.method=="POST":
        cardnumber=request.form["textfield"]
        cvv=request.form["textfield2"]
        expirydate=request.form["textfield3"]
        holfe = request.form["bb"]
        num = request.form["num"]
        db=Db()
        db.insert("INSERT INTO `credit_card` (`user_id`,`card_number`,`cvv`,`expiry_date`,`holder's name`,balance)VALUES('"+str(session["lid"])+"','"+cardnumber+"','"+cvv+"','"+expirydate+"','"+holfe+"','"+num+"')")
        return '''<script>alert("update successfully!");window.location="/view_cart"</script>'''
    else:

        return render_template('user/card_add.html')




@app.route('/card_delete/<c_id>')
def card_delete(c_id):
    db = Db()
    db.delete("delete from credit_card where card_id='"+c_id+"'")
    return '''<script>alert("deleted");window.location="/card_details"</script>'''
    return render_template('user/card.html')



@app.route('/transaction')
def register():
    qry="SELECT * FROM `bookings` INNER JOIN `bstatus` ON `bookings`.`booking_id`=`bstatus`.`bid` INNER JOIN `cart` ON cart.`cart_id`=`bookings`.`cart_id` INNER JOIN product ON `product`.`product_id` = `cart`.`prod_id` WHERE `bstatus`.`uid`='"+str(session["lid"])+"'"
    db=Db()
    res=db.select(qry)
    print(qry)
    print(res)
    return render_template('user/user_view_transaction.html',data=res)


@app.route('/user_feedback', methods=['get','post'])
def user_feedback():
    if request.method=="POST":
        feedback=request.form["textarea"]

        db = Db()
        ss = db.insert("insert into feedback (user_id,feedback,feedback_date) value ('"+str(session['lid'])+"','"+feedback+"',curdate())")
        return '''<script> alert("feedback send successfully");window.location="/userhome"</script>'''
    return render_template('user/user_feedback.html')


@app.route('/user_complaint',methods=['get','post'])
def user_complaint():
    if request.method == "POST":
        complaint = request.form["textarea"]

        db = Db()
        ss = db.insert("insert into complaint (user_id,complaint,comp_date,replay) values ('"+str(session['lid'])+"','" + complaint + "',curdate(),'pending')")
        return '''<script> alert("complaint send successfully");window.location="/userhome"</script>'''
    return render_template('user/user_complaint.html')



@app.route('/make_payements/<cart_id>',methods=['get','post'])
def make_payement(cart_id):
    session["cart_id"]=cart_id
    return render_template('user/user_payement.html')

@app.route("/add_otp")
def add_otp():
    return render_template("user/add_otp.html")

@app.route("/add_otp_post",methods=['POST'])
def add_otp_post():
    otp=request.form["textarea"]
    print(otp,otp1,"==============================")

    qry="SELECT `bookings`.*,`bstatus`.* FROM `bstatus` INNER JOIN `bookings` ON `bookings`.`booking_id`=`bstatus`.bid WHERE sid='"+str(session["bid"])+"' and otp='"+str(otp)+"'"
    print(qry)
    db=Db()
    res=db.selectOne(qry)
    print(res)
    if res is not None:
        amount=res["amount"]
        book=res["booking_id"]
        print("select * from credit_card where user_id='" + str(session['lid']) + "' and card_number='" + str(session["cno"]) + "' and cvv='" + str(session["cvv"]) + "' and expiry_date='" + str(session["expiry"]) + "'")
        cv = db.selectOne("select * from credit_card where user_id='" + str(session['lid']) + "' and card_number='" + str(session["cno"]) + "' and cvv='" + str(session["cvv"]) + "' and expiry_date='" + str(session["expiry"]) + "'")
        if cv is not None:
            ij=cv["card_id"]
            qry="UPDATE `bookings` SET `b_status`='completed' WHERE `booking_id`='"+str(book)+"'"
            db.update(qry)
            print(qry)
            qryq="UPDATE `credit_card` SET `balance`=balance-'"+str(amount)+"' WHERE `card_id`='"+str(ij)+"' "
            db.update(qryq)
            print(qryq)
        return view_cart()
    else:
        return render_template("user/add_otp.html")


@app.route('/user_complaint_view')
def user_complaint_view():

    db = Db()
    se = db.select(
        "select * from user,complaint where user.login_id=complaint.user_id and user.login_id='"+str(session["lid"])+"'")
    return render_template('user/vccomplaint.html', data=se)

@app.route('/book_product',methods=['get','post'])
def book_product():
    if request.method=="POST":
        cardno=request.form["textfield"]
        expiry=request.form["textfield2"]
        cvv=request.form["textfield3"]
        db=Db()
        cv=db.selectOne("select * from credit_card where user_id='"+str(session['lid'])+"' and card_number='"+cardno+"' and cvv='"+cvv+"' and expiry_date='"+expiry+"'")
        if cv is not None:
            session["cno"]=cardno
            session["expiry"]=expiry
            session["cvv"]=cvv
            qryy="SELECT `cart`.*,`product`.* ,`product`.`price`*`cart`.`quantity` AS qty FROM `cart` INNER JOIN `product` ON `product`.`product_id`=`cart`.`prod_id` WHERE `cart_id`='"+str(session["cart_id"])+"' and c_status!='done'"
            db=Db()
            ss=db.selectOne(qryy)
            if ss is not None:
                print(str(ss["qty"]))
                if str(ss["qty"]) !="0":
                    sds=db.insert("INSERT INTO `bookings`(`cart_id`,`amount`,`b_status`)values('"+str(session["cart_id"])+"','"+str(ss["qty"])+"','pending')")
                    sds=db.insert("INSERT INTO `bstatus`(`bid`,`uid`,`status`)values('" +str(sds) +"','" + str(session["lid"]) + "','pending')")
                    session["bid"]=str(sds)
                    ww="update `cart` set c_status='done' WHERE `cart_id`='"+str(session["cart_id"])+"'"
                    db.delete(ww)
                    return '''<script>alert("saved");window.location="/add_otp"</script>'''
                else:
                    return '''<script>alert("Invalid Card Details");window.location="/card_details"</script>'''

            else:
                return '''<script>alert("enter correct card details");window.location="/card_details"</script>'''

        else:
            return '''<script>alert("invalid");window.location="/card_details"</script>'''

    else:
        return '''<script>alert("enter valid number");window.location="/card_details"</script>'''


# ============================================android=================================================================================================

@app.route('/login',methods=['post'])
def login():
    an_username = request.form["u"]
    an_password = request.form["p"]
    db=Db()
    ss = db.selectOne("select * from login where username='" + an_username + "'and password='" + an_password + "'")
    # res={}
    if ss is not None:
    #     if ss['usertype']=='user':
    #         res['type']=ss['usertype']
    #         res['lid']=ss['login_id']
    #         res['status']="ok"
        return jsonify (type=ss['usertype'],lid=ss['login_id'],status="ok")
    else:
        return jsonify(status="no")





@app.route("/view_not_and",methods=['post'])
def view_not_and():
    bid=request.form["sid"]
    uid=request.form["uid"]
    db=Db()
    qry="SELECT * FROM `bstatus` WHERE `sid`>'"+bid+"' AND `uid`='"+uid+"'"
    # print(qry)
    res=db.selectOne(qry)
    if res is not None:
        return jsonify(status="ok",sid=res["sid"])
    else:
        return jsonify(status="no")

@app.route("/update_status",methods=['post'])
def update_status():
    bid=request.form["sid"]
    uid=request.form["uid"]
    db=Db()
    qry="UPDATE `bstatus` SET `status`='rejected' WHERE `sid`='"+bid+"' AND `uid`='"+uid+"'"
    res=db.selectOne(qry)
    if res is not None:
        return jsonify(status="ok")
    else:
        return jsonify(status="no")

@app.route("/detect_knownperson", methods=["post"])
def blind_comment():

    sid = request.form["sid"]
    lid = request.form["lid"]

    files = request.files['pic']

    files.save("C:\\Users\\USER\\PycharmProjects\\credit_card\\static\\Payment\\1.jpg")


    db = Db()
    print("SELECT * FROM `user` WHERE `login_id`='"+lid+"' ")
    qry = db.selectOne("SELECT * FROM `user` WHERE `login_id`='"+lid+"' ")

    faceencoding = []
    import face_recognition
    if qry is not None:

        ab = qry["photo"].split("/")
        picture_of_me = face_recognition.load_image_file(
            "C:\\Users\\USER\\PycharmProjects\\credit_card\\static\\user\\" + ab[3])
        my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]
        faceencoding.append(my_face_encoding)
        print("person added")
        print("C:\\Users\\USER\\PycharmProjects\\credit_card\\static\\user" + ab[3])

    unknown_image = face_recognition.load_image_file("C:\\Users\\USER\\PycharmProjects\\credit_card\\static\\Payment\\1.jpg")
    indux = 0
    unknown_faces = []
    detecteduserids = []
    indxc = 0
    try:
        m = len(face_recognition.face_encodings(unknown_image))
        print(m);
        msg = ""
        # if m == 0:
        #     return jsonify(status="ok", otp="1234")

        print("printing results")
        for a in range(m):
            s = face_recognition.face_encodings(unknown_image)[a]
            unknown_face_encoding = face_recognition.face_encodings(unknown_image)[a]
            results = face_recognition.compare_faces(faceencoding, unknown_face_encoding)

            print(results)
            print("koooooooooi")
            for i in range(len(results)):
                if results[i] == True:
                    import random
                    msg = str(random.randint(0000,9999))

                    if len(msg) > 0:
                        msg =  msg
                    else:
                        msg = 0000
                    qq="update bstatus set otp='"+str(msg)+"' where sid='"+sid+"'"
                    db.update(qq)
                    otp1=msg
                    sid1=sid
                    return jsonify(status="ok", otp=msg)
    except a:
        pass


        # detecteduserids.insert(indxc, pid[i])
        # indxc = indxc + 1

        return jsonify(status="no")
    else:
        return jsonify(status="no")


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=4000,debug=True)
