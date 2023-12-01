from rest_framework_mongoengine import serializers
from .models import *

class UsersSerializer(serializers.DocumentSerializer):
    class Meta:
        model=Users
        exclude=("password",)