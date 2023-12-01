from rest_framework_mongoengine import serializers
from .models import *

class UsersSerializer(serializers.DocumentSerializer):
    class Meta:
        model=Users
        exclude=("password",)

class ProjectsSerializer(serializers.DocumentSerializer):
    class Meta:
        model=Projects
        fields="__all__" 

        