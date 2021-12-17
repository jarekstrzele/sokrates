from flask import Flask, jsonify, request
from flask_restful import Api, Resource
# from pymongo import MongoClient
from functions import verify_user, hash_password
from flask_mongoengine import MongoEngine




app = Flask(__name__)
db = MongoEngine()

#Settings
app.config["MONGODB_SETTINGS"] = {
    "db" : "SokratesDB",
    "host":"mongodb://db:27017"
}


api = Api(app)
db.init_app(app)


class User(db.Document):
    name = db.StringField()
    password = db.StringField()
    role = db.StringField()
 




# connector = MongoClient("mongodb://db:27017")
# db = connector.SokratesDB
# users = db["users"]



class Register(Resource):
    def post(self):
        postedData = request.get_json()

        name = postedData["user_name"]
        password = postedData["password"]
        hashed_pw = hash_password(password) 
        role = postedData["role"]

        user = User(name=name, password=hashed_pw, role = role)
        user.save()

        return jsonify({
            "status" : 200,
            "msg" : "Registration - done",
            "name" :user.name,
            "password": user.password,
            "role" :role
        })



# class AdminPanel(Resource):
#     def post(self):
#         postedData = request.getjson()

#         user_name = postedData["user_name"]
#         password = postedData["password"]
        

#         isAdmin = verify_user(user_name, password, db, check_role=True)
#         if not isAdmin:
#             return jsonify({
#                 "status" :302,
#                 "msg" : "Incorrect password or user name"
#             })

#         return jsonify({
#             "msg" : "You are admin"
#         })





class Test(Resource):
    def get(self):
        # db.users.drop()
        # dbs_list = connector.list_database_names()
        # cols_list = db.list_collection_names()
        # users_names = []
        # for user in users.find({}, {"_id": 0, "user_name": 1, "role": 1}):
        #     users_names.append(user)
        # users_names = str(users_names)
        
        # users_list = []
        # for u in User.objects():
        #     users_list.append(u)
        user = User.objects(name='Tess').first()


        return jsonify( {
            "msg": "test web Sokrates_app. OK!",
            "name": user.name,
            "pasword": user.password,
            "role": user.role

        } )


api.add_resource(Test, '/test')
api.add_resource(Register, '/register')
# api.add_resource(AdminPanel, '/adminpanel')

if __name__ == "__main__":
    app.run(host='0.0.0.0')