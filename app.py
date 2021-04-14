from flask import Flask, redirect, render_template, request, session, make_response
from bson.json_util import loads, dumps
import database as db
import authentication
import logging
import ordermanagement as om

app = Flask(__name__)

# Set the secret key to some random bytes.
# Keep this really secret!
app.secret_key = b's@g@d@c0ff33!'

logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.INFO)

#from intro to flask
@app.route('/login', methods=['GET', 'POST'])
def login():
	return render_template('login.html')

@app.route('/auth', methods = ['POST'])
def auth():
	username = request.form.get('username')
	password = request.form.get('password')

	is_valid_login, user = authentication.login(username, password)
	app.logger.info('%s', is_valid_login)

	if(is_valid_login):
		session["user"] = user
		return redirect('/')
	else:
		return render_template('loginfailed.html')

@app.route('/productdetails')
def productdetails():
    code = request.args.get('code', '')
    product = db.get_product(int(code))

    return render_template('productdetails.html', code=code, product=product)

@app.route('/changepassword', methods = ['GET','POST'])
def changepassword():
    username = session["user"]["username"]
    newpassword = request.form.get("newpassword")
    verifypassword = request.form.get("verifypassword")
    updatepassword = None
    error = None

    if newpassword == None:
        error = None
    elif verifypassword==newpassword:
        updatepassword=db.update_password(username,newpassword)
    elif verifypassword!=newpassword:
        error = "Password does not match."

    return render_template("changepassword.html", page="Change Password", updatepassword=updatepassword, error=error)

@app.route('/logout')
def logout():
	session.pop("user",None)
	session.pop("cart",None)
	return redirect('/')

@app.route('/removecart', methods=["POST"])
def removecart():
    cart = session["cart"]
    code = request.form.get('code')
    del cart[code]
    session["cart"]=cart
    return render_template("cart.html")

@app.route('/cart')
def cart():
	return render_template('cart.html')

@app.route('/checkout')
def checkout(): # clear cart in session memory upon checkout
    om.create_order_from_cart()
    session.pop("cart",None)
    return redirect('/ordercomplete')

@app.route('/ordercomplete')
def ordercomplete():
    return render_template('ordercomplete.html')

@app.route('/history')
def pastorders():
    pastorders = db.get_pastorders()
    pastorder_list = []
    counter1 = 0
    for pastorder in pastorders:
        counter1 += 1
        for info in pastorder['details']:
            pastorder_list.append(info)

    return render_template('pastorders.html', page="Past Orders", pastorders = pastorder_list, counter1 = counter1)

#sign up
@app.route("/register", methods=['GET', 'POST'])
def register(): #issue: does not update database
    return render_template("register.html")

@app.route('/s_auth', methods = ['POST'])
def s_auth():
	username = request.form.get('username')
	password = request.form.get('password')

	is_valid_signup, user = authentication.signup(username, password)
	app.logger.info('%s', is_valid_signup)

	if(is_valid_signup):
		session["user"] = user
		updateuser = db.insert_one(user)
		return redirect('/')
	else:
		return render_template('registerfail.html')

#for you (home) page
@app.route('/')
def match_interests():
    interest_list = db.get_interest()
    tag_list = db.get_tag()
    product_list=[]

    if not interest_list: #list is empty
        product_list=db.get_products() #show all products
    else:
        for i in interest_list: #curate page by interests
            for t in tag_list:
                if i == t: #matched interest
                    for p in products_coll.find({'interest_tag':i}):
                        product_list.append(p)

    return render_template('foryou.html', page="For You", product_list=product_list)

#following page
@app.route('/following')
def followings():
    following_list = db.get_following()
    seller_list = db.get_sellers()
    not_following = True
    fproduct_list=[]

    if not following_list: #list is empty
        not_following = True
    else:
        not_following = False
        for f in following_list: #show only products from sellers followed
            for s in seller_list:
                if f == s: #matched seller account
                    for p in products_coll.find({'seller_name':f}):
                        fproduct_list.append(p)

    return render_template('following.html', page="Following", fproduct_list=fproduct_list, not_following=not_following)

#account interests
@app.route('/account')
def profile():
	return render_template('profile.html', page='Profile')

@app.route('/interests', methods=['GET', 'POST'])
def interests():
    interests = db.get_tag()
    interest_list = []
    if request.method == 'POST':
        request.form.getlist('checkboxes')
    for checkbox in checkboxes:
        interest_list.append(checkbox)

    updateinterests = db.update_interest_tags(interest_list)

    return redirect('foryou.html')

#mine, grab, steal
@app.route('/mine')
def mine():
    code = request.args.get('code', '')
    product = db.get_product(int(code))
    item=dict()

    item["name"] = product["name"]
    item["subtotal"] = product["price1"]
    item["code"] = code

    if(session.get("cart") is None):
        session["cart"]={}

    cart = session["cart"]
    cart[code]=item
    session["cart"]=cart
    return redirect('/cart')

@app.route('/grab')
def grab():
    code = request.args.get('code', '')
    product = db.get_product(int(code))
    item=dict()

    item["name"] = product["name"]
    item["subtotal"] = product["price2"]
    item["code"] = code

    if(session.get("cart") is None):
        session["cart"]={}

    cart = session["cart"]
    cart[code]=item
    session["cart"]=cart
    return redirect('/cart')

@app.route('/steal')
def steal():
    code = request.args.get('code', '')
    product = db.get_product(int(code))
    item=dict()

    item["name"] = product["name"]
    item["subtotal"] = product["price3"]
    item["code"] = code

    if(session.get("cart") is None):
        session["cart"]={}

    cart = session["cart"]
    cart[code]=item
    session["cart"]=cart
    return redirect('/cart')
