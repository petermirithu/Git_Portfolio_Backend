import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.utils.timezone import now as getTimeNow

from git_portfolio_app.email import send_reset_verification_code
from .permissions import isAuthorized
from .enc_decryption import check_password, encode_value, hash_password
from .helpers import check_if_email_taken, generate_verification_code, verify_verification_code
from .models import *
from .serializers import *
import traceback

# Create your views here.
@api_view(['POST'])
@permission_classes([])
def sign_up_user(request):
    data = json.loads(request.body)
    try:             
        first_name = data['first_name']                  
        last_name = data['last_name']
        email = data['email']
        password = data['password']                   
                        
        if len(first_name)==0 or len(last_name)==0 or len(email)==0 or len(password)==0:
            raise ValueError("Seems some important fields are empty!!!")                
        
        taken=check_if_email_taken(email)
        
        if taken==True:            
            return Response('emailTaken', status=status.HTTP_423_LOCKED)
        else:                                                 
            hashed_password = hash_password(password)                
            new_user = Users(
                        first_name=first_name,
                        last_name=last_name,
                        email=email,                                                 
                        password=str(hashed_password),                                                    
                        created_at=getTimeNow()
                        )
            new_user.save()                                                
            serialised_user = UsersSerializer(new_user, many=False)                                        
            return Response(serialised_user.data, status=status.HTTP_201_CREATED)
    except:    
        # Unmuted to see full error !!!!!!!!!
        print("**********************************************************")
        print(traceback.format_exc())           
        print("**********************************************************")     
        return Response("Error occured while creating an account", status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([])
def sign_in_user(request):
    data = json.loads(request.body)
    try:
        email = data['email']
        password = data['password']                        

        try:
            user = Users.objects.get(email=email)                           

            if(check_password(password, user.password) == True):                    
                now = getTimeNow()   
                serialised_user = UsersSerializer(user, many=False)                                                                 
                payload = {'id': serialised_user.data["id"],'loggedinAt': now.strftime("%m/%d/%Y, %H:%M:%S")}                    
                user.auth_token=encode_value(payload)                                                             
                serialised_user = UsersSerializer(user, many=False)                                        
                return Response(serialised_user.data, status=status.HTTP_200_OK)
            else:
                print("**********************************************************")
                print("Wrong password")           
                print("**********************************************************")     
                return Response("invalidCredentials", status=status.HTTP_400_BAD_REQUEST)                                        
        except Users.DoesNotExist:   
            print("**********************************************************")
            print("User not found")           
            print("**********************************************************")     
            return Response("invalidCredentials", status=status.HTTP_400_BAD_REQUEST)                                                    
    except:
        # Unmuted to see full error !!!!!!!!!
        print("**********************************************************")
        print(traceback.format_exc())           
        print("**********************************************************")     
        return Response("An error occured while authenticating you", status=status.HTTP_400_BAD_REQUEST)                        

@api_view(['PUT'])
@permission_classes([])
def forgot_password(request):
    data = json.loads(request.body)
    try:         
        user=Users.objects.get(email=data["email"])
        verification_code = generate_verification_code(user.id)                    
        send_code_results = send_reset_verification_code(user.first_name, verification_code, user.email)
        send_code_results=""
        if send_code_results=="error":
            return Response("Error while sending you a verification code", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Verification code sent successfully", status=status.HTTP_201_CREATED)                        
    except Users.DoesNotExist:
        return Response("Successfully sent the code if account exists", status=status.HTTP_200_OK)                            
    except:
        print("**********************************************************")
        print(traceback.format_exc())           
        print("**********************************************************")     
        return Response("Error while updating your user profile", status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT'])
@permission_classes([])
def reset_password(request):
    data = json.loads(request.body)
    try:                         
        user=Users.objects.get(email=data["email"])
        results = verify_verification_code(user.id, data["verificationCode"])

        if results == "code okay":   
            hashed_password = hash_password(data["password"])                            
            Users.objects.filter(email=data["email"]).update(password=str(hashed_password))
            return Response("Successfully reset your password", status=status.HTTP_200_OK)                                    
        elif results == "code expired":
            return Response("codeExpired", status=status.HTTP_400_BAD_REQUEST)        
        else:
            return Response("invalidVerificationCode", status=status.HTTP_400_BAD_REQUEST)                                                            
    except:
        print("**********************************************************")
        print(traceback.format_exc())           
        print("**********************************************************")     
        return Response("Error while updating your user profile", status=status.HTTP_400_BAD_REQUEST) 
    
@api_view(['POST'])
@permission_classes([isAuthorized])
def add_project(request):
    data = json.loads(request.body)
    try:                         
        name=data["name"]
        description=data["description"]
        technologies=data["technologies"]
        link=data["link"]
        user_id=data["user_id"]

        try:
            project=Projects.objects.get(name=name)        
            return Response("nameTaken", status=status.HTTP_400_BAD_REQUEST)                            
        except Projects.DoesNotExist:
            new_project = Projects(
                        name=name,
                        description=description,
                        technologies=technologies,                                                 
                        link=link,    
                        user_id=user_id,                   
                        created_at=getTimeNow()
                        )
            new_project.save()  
            return Response("Successfully saved the project", status=status.HTTP_201_CREATED)                            
    except:
        print("**********************************************************")
        print(traceback.format_exc())           
        print("**********************************************************")     
        return Response("Error while saving your project", status=status.HTTP_400_BAD_REQUEST)    

@api_view(['PUT'])
@permission_classes([isAuthorized])
def update_project(request):
    data = json.loads(request.body)
    try:                         
        name=data["name"]
        description=data["description"]
        technologies=data["technologies"]
        link=data["link"]
        project_id=data["project_id"]

        Projects.objects.filter(id=project_id).update(
            name=name,
            description=description,
            technologies=technologies,                                                 
            link=link,       
        )
        return Response("Successfully updated the project", status=status.HTTP_200_OK)                                                
    except:
        print("**********************************************************")
        print(traceback.format_exc())           
        print("**********************************************************")     
        return Response("Error while updating your project", status=status.HTTP_400_BAD_REQUEST)      

@api_view(['DELETE'])
@permission_classes([isAuthorized])
def delete_project(request, project_id):    
    try:                         
        Projects.objects.filter(id=project_id).delete() 
        return Response("Successfully deleted the project", status=status.HTTP_200_OK)                                                
    except:
        print("**********************************************************")
        print(traceback.format_exc())           
        print("**********************************************************")     
        return Response("Error while deleting your project", status=status.HTTP_400_BAD_REQUEST)      

@api_view(['GET'])
@permission_classes([isAuthorized])
def get_projects(request, user_id):    
    try:                         
        projects = Projects.objects.filter(user_id=user_id)
        serialized_projects = ProjectsSerializer(projects, many=True).data
        return Response(serialized_projects, status=status.HTTP_200_OK)
    except:
        print("**********************************************************")
        print(traceback.format_exc())           
        print("**********************************************************")     
        return Response("Error while getting your projects", status=status.HTTP_400_BAD_REQUEST)      

@api_view(['POST'])
@permission_classes([isAuthorized])
def add_experience(request):
    data = json.loads(request.body)
    try:                             
        title=data["title"]
        description=data["description"]
        employmentType=data["employmentType"]
        companyName=data["companyName"]
        location=data["location"]
        locationType=data["locationType"]
        currentlyWorking=data["currentlyWorking"]
        startDate=data["startDate"]
        endDate=data["endDate"]
        user_id=data["user_id"]
        
        new_experience = Experiences(
            title=title,
            description=description,
            employmentType=employmentType,                                                 
            companyName=companyName,    
            location=location,
            locationType=locationType,
            currentlyWorking=currentlyWorking,
            startDate=startDate,
            endDate=endDate,
            user_id=user_id,                   
            created_at=getTimeNow()
        )
        new_experience.save()  
        return Response("Successfully saved the experience", status=status.HTTP_201_CREATED)                            
    except:
        print("**********************************************************")
        print(traceback.format_exc())           
        print("**********************************************************")     
        return Response("Error while saving your experience", status=status.HTTP_400_BAD_REQUEST)        

@api_view(['PUT'])
@permission_classes([isAuthorized])
def update_experience(request):
    data = json.loads(request.body)
    try:                         
        title=data["title"]
        description=data["description"]
        employmentType=data["employmentType"]
        companyName=data["companyName"]
        location=data["location"]
        locationType=data["locationType"]
        currentlyWorking=data["currentlyWorking"]
        startDate=data["startDate"]
        endDate=data["endDate"]
        experience_id=data["experience_id"]

        Experiences.objects.filter(id=experience_id).update(
            title=title,
            description=description,
            employmentType=employmentType,                                                 
            companyName=companyName,    
            location=location,
            locationType=locationType,
            currentlyWorking=currentlyWorking,
            startDate=startDate,
            endDate=endDate,
        )
        return Response("Successfully updated the experience", status=status.HTTP_200_OK)                                                
    except:
        print("**********************************************************")
        print(traceback.format_exc())           
        print("**********************************************************")     
        return Response("Error while updating your experience", status=status.HTTP_400_BAD_REQUEST)          

@api_view(['DELETE'])
@permission_classes([isAuthorized])
def delete_experience(request, experience_id):    
    try:                         
        Experiences.objects.filter(id=experience_id).delete() 
        return Response("Successfully deleted the experience", status=status.HTTP_200_OK)                                                
    except:
        print("**********************************************************")
        print(traceback.format_exc())           
        print("**********************************************************")     
        return Response("Error while deleting your experience", status=status.HTTP_400_BAD_REQUEST)      

@api_view(['GET'])
@permission_classes([isAuthorized])
def get_experiences(request, user_id):    
    try:                         
        experiences = Experiences.objects.filter(user_id=user_id)
        serialized_experiences = ExperiencesSerializer(experiences, many=True).data
        return Response(serialized_experiences, status=status.HTTP_200_OK)
    except:
        print("**********************************************************")
        print(traceback.format_exc())           
        print("**********************************************************")     
        return Response("Error while getting your experiences", status=status.HTTP_400_BAD_REQUEST)          


@api_view(['PUT'])
@permission_classes([isAuthorized])
def update_socials(request):
    data = json.loads(request.body)
    try:                       
        github=data["github"]
        linkedin=data["linkedin"]
        twitter=data["twitter"]
        youtube=data["youtube"]
        whatsapp=data["whatsapp"]       
        user_id=data["user_id"]
        Users.objects.filter(id=user_id).update(
            github=github,
            linkedin=linkedin,
            twitter=twitter,                                                 
            youtube=youtube,    
            whatsapp=whatsapp,            
        )
        return Response("Successfully updated the socials", status=status.HTTP_200_OK)                                                
    except:
        print("**********************************************************")
        print(traceback.format_exc())           
        print("**********************************************************")     
        return Response("Error while updating your socials", status=status.HTTP_400_BAD_REQUEST)          


@api_view(['GET'])
@permission_classes([])
def get_user(request, email):    
    try:                         
        user = Users.objects.filter(email=email)
        serialized_user = UsersSerializer(user, many=False).data
        return Response(serialized_user, status=status.HTTP_200_OK)
    except:
        print("**********************************************************")
        print(traceback.format_exc())           
        print("**********************************************************")     
        return Response("Error while getting the user", status=status.HTTP_400_BAD_REQUEST)          

@api_view(['POST'])
@permission_classes([isAuthorized])
def add_skill(request):
    data = json.loads(request.body)
    try:                             
        name=data["name"]        
        user_id=data["user_id"]
        
        new_skill = Skills(
            name=name,            
            user_id=user_id,                   
            created_at=getTimeNow()
        )
        new_skill.save()  
        return Response("Successfully saved the skill", status=status.HTTP_201_CREATED)                            
    except:
        print("**********************************************************")
        print(traceback.format_exc())           
        print("**********************************************************")     
        return Response("Error while saving your skill", status=status.HTTP_400_BAD_REQUEST)        


@api_view(['PUT'])
@permission_classes([isAuthorized])
def update_skill(request):
    data = json.loads(request.body)
    try:                       
        name=data["name"]        
        skill_id=data["skill_id"]

        Skills.objects.filter(id=skill_id).update(
            name=name,                      
        )
        return Response("Successfully updated the skill", status=status.HTTP_200_OK)                                                
    except:
        print("**********************************************************")
        print(traceback.format_exc())           
        print("**********************************************************")     
        return Response("Error while updating your skill", status=status.HTTP_400_BAD_REQUEST)          


@api_view(['DELETE'])
@permission_classes([isAuthorized])
def delete_skill(request, skill_id):    
    try:                         
        Skills.objects.filter(id=skill_id).delete() 
        return Response("Successfully deleted the skill", status=status.HTTP_200_OK)                                                
    except:
        print("**********************************************************")
        print(traceback.format_exc())           
        print("**********************************************************")     
        return Response("Error while deleting your skill", status=status.HTTP_400_BAD_REQUEST)      
    
@api_view(['GET'])
@permission_classes([isAuthorized])
def get_skills(request, user_id):    
    try:                         
        skills = Skills.objects.filter(user_id=user_id)
        serialized_skills = SkillsSerializer(skills, many=True).data
        return Response(serialized_skills, status=status.HTTP_200_OK)
    except:
        print("**********************************************************")
        print(traceback.format_exc())           
        print("**********************************************************")     
        return Response("Error while getting your skills", status=status.HTTP_400_BAD_REQUEST)          