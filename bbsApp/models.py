from mongoengine import *

class Comment(EmbeddedDocument):
    author = StringField(max_length=50)
    content = StringField()
    date =  StringField(max_length=50)

class Post(Document):
    title = StringField(required=True)
    content = StringField()
    author = StringField(max_length=50)
    date =  StringField(max_length=50)
    comment= ListField(EmbeddedDocumentField(Comment))

    meta = {
        'ordering': ['-id']
    }