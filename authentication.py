import database as db

def login(username, password):
	is_valid_login = False
	user=None
	temp_user = db.get_user(username)
	if(temp_user != None):
		if(temp_user["password"]==password):
			is_valid_login=True
			user={"username":username,"password":password, "interests":interests,"following":following}
	return is_valid_login, user

def signup(username, password):
	is_valid_signup = False
	user=None
	temp_user = db.get_user(username)
	if temp_user is None:
		user={"username":username, "password":password,"interests":"","following":""}
	return is_valid_signup, user
