from mongoengine import *
import datetime

# Create your models here.
class Users(Document):         
    first_name=StringField(required=True)
    last_name=StringField(required=True)
    email=StringField(required=True)    
    password=StringField(required=True)                
    auth_token=StringField()
    updated_at=DateTimeField(default=datetime.datetime.utcnow)
    created_at=DateTimeField(required=True)

class VerificationCodes(Document):
    user_id = ReferenceField(Users, reverse_delete_rule=CASCADE)
    code = StringField(required=True)    
    used = BooleanField(default=False)
    created_at = DateTimeField(required=True)

class Projects(Document):
    user_id = ReferenceField(Users, reverse_delete_rule=CASCADE)
    name = StringField(required=True)        
    description = StringField(required=True)    
    technologies = StringField(required=True)    
    link = StringField(required=True)    
    updated_at=DateTimeField(default=datetime.datetime.utcnow)
    created_at = DateTimeField(required=True)