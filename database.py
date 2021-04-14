import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

products_db = myclient["products"]
order_management_db = myclient["customers"]

def get_user(username):
    customers_coll = order_management_db['customers']
    user = customers_coll.find_one({"username":username})
    return user

def get_product(code):
    products_coll = products_db["products"]
    product = products_coll.find_one({"code":code},{"_id":0})

    return product

def get_products():
    product_list = []
    products_coll = products_db["products"]

    for p in products_coll.find({},{"_id":0}):
        product_list.append(p)

    return product_list

def create_order(order):
    orders_coll = order_management_db['orders']
    orders_coll.insert(order)

def get_pastorders():
    pastorder_list = []
    pastorders_coll = order_management_db['orders']
    for p in pastorders_coll.find({"username":session["user"]["username"]}):
        pastorder_list.append(p)

    return pastorder_list

def get_interest():
    interest_list=[]
    customers_coll = order_management_db['customers']
    interest_coll=customers_coll['interests'] #change according to jules' variables

    for i in interest_coll.find({}):
        interest_list.append(i)

    return interest_list

def get_tag():
    tag_list=[]
    products_coll = products_db['products']
    tag_coll=products_coll['interest_tags']

    for t in tag_coll.find({}):
      tag_list.append(t)

    return tag_list

def get_following():
    following_list=[]
    customers_coll = order_management_db['customers']
    following_coll=customers_coll['following']

    for f in following_coll.find({}):
        following_list.append(f)

    return following_list

def get_sellers():
    seller_list=[]
    products_coll = products_db['products']
    seller_coll=products_coll['seller_name']

    for s in seller_coll.find({}):
      seller_list.append(s)

    return seller_list

def match_iproducts(interest_list, tag_list):
    product_list=[]
    for i in interest_list: #curate page by interests
        for t in tag_list:
            if i == t: #matched interest
                for p in products_coll.find({'interest_tag':i}):
                    product_list.append(p)
    return product_list

def match_fproducts(following_list, seller_list):
    fproduct_list=[]
    for f in following_list: #show only products from sellers followed
        for s in seller_list:
            if f == s: #matched seller account
                for p in products_coll.find({'seller_name':f}):
                    fproduct_list.append(p)
    return fproduct_list
