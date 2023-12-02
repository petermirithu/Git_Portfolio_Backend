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

class ExperiencesSerializer(serializers.DocumentSerializer):
    class Meta:
        model=Experiences
        fields="__all__" 

class SkillsSerializer(serializers.DocumentSerializer):
    class Meta:
        model=Skills
        fields="__all__" 




        