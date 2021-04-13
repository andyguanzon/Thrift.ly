from flask import Flask,redirect
from flask import render_template
from flask import request
from flask import session
from bson.json_util import loads, dumps
from flask import make_response
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


@app.route('/')
def index():
    return render_template('index.html', page="Index")

@app.route('/products')
def products():
    product_list = db.get_products()
    return render_template('products.html', page="Products", product_list=product_list)

@app.route('/productdetails')
def productdetails():
    code = request.args.get('code', '')
    product = db.get_product(int(code))
    return render_template('productdetails.html', code=code, product=product)

@app.route('/branches')
def branches():
    branch_list = db.get_branches()
    return render_template('branches.html', page="Branches", branch_list=branch_list)

@app.route('/branchdetails')
def branchdetails():
    code = request.args.get('code', '')
    branch = db.get_branch(int(code))
    return render_template('branchdetails.html', code=code, branch=branch)

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html', page="About Us")

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/auth', methods = ['GET', 'POST'])
def auth():
    username = request.form.get('username')
    password = request.form.get('password')
    is_successful, user = authentication.login(username, password)
    app.logger.info('%s', is_successful)
    if(is_successful):
        session["user"] = user
        return redirect('/')
    else:
        return render_template('/invalidlogin.html')

@app.route('/addtocart')
def addtocart():
    code = request.args.get('code', '')
    product = db.get_product(int(code))
    item=dict()

    item["qty"] = 1
    item["name"] = product["name"]
    item["subtotal"] = product["price"]*item["qty"]
    item["code"] = code

    if(session.get("cart") is None):
        session["cart"]={}

    cart = session["cart"]
    cart[code]=item
    session["cart"]=cart
    return redirect('/cart')

@app.route('/updatecart', methods=['POST'])
def updatecart():
    cart = session["cart"]
    code = request.form.get('code')
    qty = int(request.form.get('qty'))
    unit_price = request.form.get('price')
    product = db.get_product(int(code))

    for item in cart.values():
        if item["code"] == code:
            item["qty"] = qty
            item["subtotal"] = product["price"]*qty
            cart[code]=item
            session["cart"]=cart
    return render_template("cart.html")

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

@app.route('/pastorders')
def pastorders():
    pastorders = db.get_pastorders()
    pastorder_list = []
    counter1 = 0
    for pastorder in pastorders:
        counter1 += 1
        for info in pastorder['details']:
            pastorder_list.append(info)


    return render_template('pastorders.html', page="Past Orders", pastorders = pastorder_list, counter1 = counter1)

@app.route('/logout')
def logout():
    session.pop("user",None)
    session.pop("cart",None)
    return redirect('/')

@app.route('/checkout')
def checkout():
    # clear cart in session memory upon checkout
    om.create_order_from_cart()
    session.pop("cart",None)
    return redirect('/ordercomplete')

@app.route('/ordercomplete')
def ordercomplete():
    return render_template('ordercomplete.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    return render_template("register.html")
    if request.method == "POST":
        email = request.form["email"]
        if check_data(email):
            email = request.form["email"]
            name = request.form["name"]
            password = request.form["password"]
            print(name)
            print(email)
            print(password)
            insert(name, email, password)
            return redirect('/')
        else:
            return render_template("register_fail.html")

@app.route("/changepassword",methods=["GET","POST"])
def changepassword():
    username = session["user"]["username"]
    newpassword = request.form.get("newpassword")
    verifypassword = request.form.get("verifypassword")
    updatepassword = None
    error = None

    if newpassword == None:
        error=None
    elif verifypassword == newpassword:
        updatepassword=db.update_password(username,newpassword)
    elif verifypassword != newpassword:
        error="Password does not match."

    return render_template("changepassword.html", page="Change Password",updatepassword=updatepassword,error=error)

@app.route('/api/products/<int:code>',methods=['GET'])
def api_get_product(code):
    resp = make_response(dumps(db.get_product(code)))
    resp.mimetype = 'application/json'
    return resp
