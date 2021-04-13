import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

products_db = myclient["products"]
order_management_db = myclient["customers"]

def get_user(username):
    customers_coll = order_management_db['customers']
    user = customers_coll.find_one({"username":username})
    return user

def get_products():
    product_list = []
    products_coll = products_db["products"]

    for p in products_coll.find({},{"_id":0}):
        product_list.append(p)

    return product_list

def get_interest():
    interest_list=[]
    customers_coll = order_management_db['customers']
    interest_coll=customers_coll['interests'] #change according to jules' variables

    for i in interest_coll.find({}):
        interest_list.append()

    return interest_list

def get_tag():
    tag_list=[]
    products_coll = products_db['products']
    tag_coll=products_coll['interest_tags']

    for t in tag_coll.find({}):
      tag_list.append()

    return tag_list

def get_following():
    following_list=[]
    customers_coll = order_management_db['customers']
    following_coll=customers_coll['following'] #change according to jules' variables

    for f in following_coll.find({}):
        following_list.append()

    return following_list

def get_sellers():
    seller_list=[]
    products_coll = products_db['products']
    seller_coll=products_coll['seller_name']

    for s in seller_coll.find({}):
      seller_list.append()

    return seller_list
