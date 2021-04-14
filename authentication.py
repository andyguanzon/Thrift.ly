import database as db

def login(username, password):
    is_valid_login = False
    user=None
    temp_user = db.get_user(username)
    if(temp_user != None):
        if(temp_user["password"]==password):
            is_valid_login=True
            user={"username":username,
                  "interests":temp_user["interests"],
                  "following":temp_user["following"]}

    return is_valid_login, user

def signup(username, password, password2):
	is_valid_signup = False
	user=None
	temp_user = db.get_user(username)
	if temp_user is None:
		if password == password2:
			is_valid_signup = True
			user={"username":username, "password":password,
			"interests":"", "following":""}
	return is_valid_signup, user
