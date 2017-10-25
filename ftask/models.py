from flask_mongoengine import MongoEngine

db = MongoEngine()

class Task(db.Document):
    title = db.StringField(max_length=20,required=True)
    start = db.DateTimeField(required=True)
    finish = db.DateTimeField()
    project = db.StringField(max_length=20)
    description = db.StringField()
    tags = db.ListField(db.StringField(max_length=20))
