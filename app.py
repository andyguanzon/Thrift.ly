from flask import Flask, redirect, render_template, request, session, make_response
from bson.json_util import loads, dumps
import database as db
import authentication
import logging

app = Flask(__name__)

# Set the secret key to some random bytes.
# Keep this really secret!
app.secret_key = b's@g@d@c0ff33!'

logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.INFO)

@app.route('/login', methods=['GET', 'POST'])
def login():
	return render_template('login.html')

@app.route('/auth', methods = ['POST'])
def auth():
	username = request.form.get('username')
	password = request.form.get('password')

	is_successful, user = authentication.login(username, password)
	app.logger.info('%s', is_successful)

	if(is_successful):
		session["user"] = user
		return redirect('/')
	else:
		return render_template('loginfailed.html')

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

@app.route('/following')
def following():
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
