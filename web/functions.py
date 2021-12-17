import bcrypt 

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

def verify_user(username, password, db, check_role=False):
    pass
    # if not check_role:
    #     hashed_pw = db.find({
    #         "Username":username
    #     })[0]["password"]

    #     if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
    #         return True
    #     else:
    #         return False
    # else:

    # True if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed else False