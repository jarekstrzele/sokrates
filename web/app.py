from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt 

app = Flask(__name__)
api = Api(app)

connector = MongoClient("mongodb://db:27017")
db = connector.SokratesDB
users = db["users"]



class Register(Resource):
    def post(self):
        postedData = request.get_json()

        name = postedData["user_name"]
        password = postedData["password"]
        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        role = postedData["role"]

        users.insert_one({
            "user_name" : name,
            "password" : hashed_pw,
            "role" : role
        })

        return jsonify( {
            "status" : 200,
            "msg" : "Registration - done"
        })






class Test(Resource):
    def get(self):
        dbs_list = connector.list_database_names()
        cols_list = db.list_collection_names()
        users_names = []
        for user in users.find({}, {"_id": 0, "user_name": 1, "role": 1}):
            users_names.append(user)
        users_names = str(users_names)

        return jsonify( {
            "msg": "test web Sokrates_app. OK!",
            "dbs_list": dbs_list,
            "cols_list": cols_list,
            "users name": users_names
        } )


api.add_resource(Test, '/test')
api.add_resource(Register, '/register')


if __name__ == "__main__":
    app.run(host='0.0.0.0')