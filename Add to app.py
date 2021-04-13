@app.route('/interests', methods=['GET', 'POST'])
def index():
    interests = db.get_interest_tags()
    interest_list = []
    if request.method == 'POST':
        request.form.getlist('checkboxes')
    for checkbox in checkboxes:
        interest_list.append(checkbox)

    updateinterests = db.update_interest_tags(interest_list)

    return redirect('foryou.html')

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
def mine():
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
