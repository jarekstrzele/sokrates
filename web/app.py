from flask import Flask, jsonify, request
from flask_restful import Api, Resource
# from pymongo import MongoClient
from functions import hash_password
from flask_mongoengine import MongoEngine
from datetime import datetime



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
    name = db.StringField(unique=True)
    password = db.StringField()
    admin = db.BooleanField()
    test_creator = db.BooleanField()
    date_of_registration = db.DateTimeField(default=datetime.utcnow)




class Topic(db.EmbeddedDocumentt):
    topic_name = StringField(required=True)
    philosopher = StringField(required=True)
    contents = StringField(required=True)



class Test(db.Document):
    author = ReferenceField(User)
    test_name = StringField(required=True)
    topics = db.EmbeddedDocumentListField(Topic)
    

# connector = MongoClient("mongodb://db:27017")
# db = connector.SokratesDB
# users = db["users"]



class Register(Resource):
    def post(self):
        postedData = request.get_json()

        name = postedData["user_name"]
        password = postedData["password"]
        hashed_pw = hash_password(password) 
       
        user = User(name=name, password=hashed_pw, admin=False, test_creator=False )
        user.save()

        return jsonify({
            "status" : 200,
            "msg" : "Registration - done",
            "name" :user.name,
            "password": user.password,
            "admin" :user.admin,
            "test_creator" : user.test_creator,
            "date_of_regist": user.date_of_registration
        })



class AdminPanel(Resource):
    def post(self):
        postedData = request.get_json()
       
        #Login as an admin
        name = postedData["user_name"]
        password = postedData["password"]
        hashed_pw = hash_password(password)

        user = User.objects(name=name).get()
        if not user:
            return jsonify({
                "status":404,
                "msg": "user not found"
            })

        if not user.admin:
            return jsonify({
                "status": 301,
                "msg": "user is not admin"
            }) 

        
        if postedData['delete_user']:
            user_to_delete=User.objects(name=postedData["user_to_delete"])
            user_to_delete.delete()

            return jsonify({
                "status": 200,
                "msg": "user is deleted "
            })


class TestCreator(Resource):
    def post(self):
        postedData = request.get_json()
       
        #Login as an admin
        name = postedData["user_name"]
        test_name = postedData["test_name"]
        

class AddTopic(Resource):
    pass


api.add_resource(Test, '/test')
api.add_resource(Register, '/register')
api.add_resource(AdminPanel, '/adminpanel')

if __name__ == "__main__":
    app.run(host='0.0.0.0')