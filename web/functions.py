import bcrypt 

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())


