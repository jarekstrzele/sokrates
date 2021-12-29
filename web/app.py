from os import remove
from re import DEBUG
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

#############################
#       Collections         #
#############################
class User(db.Document):
    user_name = db.StringField(unique=True)
    password = db.StringField()
    admin = db.BooleanField()
    test_creator = db.BooleanField()
    date_of_registration = db.DateTimeField(default=datetime.utcnow)

class Topic(db.EmbeddedDocument):
    topic_name = db.StringField(required=True)
    philosopher = db.StringField(required=True)
    content = db.StringField(required=True)

class Test(db.Document):
    author = db.ReferenceField(User)
    test_name = db.StringField(required=True, unique=True)
    topics = db.EmbeddedDocumentListField(Topic)


#############
#    API    #
#############
class Register(Resource):
    def post(self):
        postedData = request.get_json()

        user_name = postedData["user_name"]
        password = postedData["password"]
        hashed_pw = hash_password(password) 
       
        user = User(user_name=user_name, password=hashed_pw, admin=False, test_creator=False )
        user.save()

        return jsonify({
            "status" : 200,
            "msg" : "Registration - done",
            "user_name" :user.user_name,
            "password": user.password,
            "admin" :user.admin,
            "test_creator" : user.test_creator,
            "date_of_regist": user.date_of_registration
        })



class AdminPanel(Resource):
    def post(self):
        postedData = request.get_json()
       
        #Login as an admin
        user_name = postedData["user_name"]
        password = postedData["password"]
        hashed_pw = hash_password(password)

        the_user = User.objects(user_name=user_name).get()
        if not the_user:
            return jsonify({
                "status":303,
                "msg": "user not found"
            })

        if not the_user.admin:
            return jsonify({
                "status": 301,
                "msg": "user is not admin"
            }) 

        
        if postedData['delete_user']:
            user_to_delete=User.objects(user_name=postedData["user_to_delete"])
            user_to_delete.delete()

            return jsonify({
                "status": 200,
                "msg": "the user is deleted "
            })


class AddTest(Resource):
    def post(self):
        postedData = request.get_json()
               
        the_user = User.objects(user_name=postedData["user_name"]).get()
        if not the_user.test_creator:
            return jsonify({
                "status":301,
                "msg": "you can't creat a test"
            })
        test_name = postedData["test_name"]

        # create a test as a collection
        Test(author=the_user, test_name=test_name).save()
        
        return jsonify({
            "stauts": 200,
            "msg": str(Test.objects(test_name=test_name)) + "saved."
        })


class RemoveTest(Resource):
    def post(self):
        postedData = request.get_json()
               
        the_user = User.objects(user_name=postedData["user_name"]).first()
        the_test = Test.objects(test_name=postedData["test_name"]).first()

        if  the_user.admin or not the_user.user_name == the_test.author:
            the_test.delete()
            return jsonify({
            "stauts": 200,
            "msg": "Test has been deleted."
        })
        else:
            return jsonify({
                "status":301,
                "user_name" : the_user.user_name,
                "admin?": the_user.admin,
                "msg": "you can't delete the test"
            })


class AddTopic(Resource):
     def post(self):
        postedData = request.get_json()
        
        the_user = User.objects(user_name=postedData["user_name"]).first()
        the_test = Test.objects(test_name=postedData["test_name"]).first()
        
        if the_user.user_name != the_test.author.user_name:
            return jsonify({
                "stauts": 303,
                "msg": "You are not an author of this test."
            })

        topic_name = postedData["topic_name"]
        philosopher = postedData["philosopher"]
        content = postedData["content"]

        topic = Topic(topic_name=topic_name, philosopher=philosopher, content=content)
        the_test.topics.append(topic)
        the_test.save()
        
        return jsonify({
                "stauts": 200,
                "msg": "Topic was added."
            })






class Show(Resource):
    def get(self):

        # create admin
        # User(user_name="admin", password="xyz", admin=True, test_creator=True).save()

        users = []
        tests = []
        topics = []

        for u in User.objects():
            users.append(u.user_name)
        
        tmp = Test.objects()
        for t in tmp:
            tests.append((t.test_name, t.author.user_name, t.topics))
            for topic in t.topics:
                topics.append((topic.topic_name, topic.philosopher, topic.content))

        administator = User.objects(admin=True).first()
        return jsonify({
            "users":str(users),
            "tests":str(tests),
            "topics": str(topics),
            "admin":administator.user_name
        })


api.add_resource(Show, '/show')
api.add_resource(Register, '/register')
api.add_resource(AdminPanel, '/admin_panel')
api.add_resource(AddTest, '/add_test')
api.add_resource(RemoveTest, '/remove_test')
api.add_resource(AddTopic, '/add_topic')

if __name__ == "__main__":
    app.run(host='0.0.0.0')