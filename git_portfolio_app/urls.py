from django.urls import path
from .views import *

urlpatterns = [    
    # APIs for all users
    path('sign_up_user', sign_up_user, name='sign_up_user'),    
    path('sign_in_user', sign_in_user, name='sign_in_user'),                        
    path('forgot_password', forgot_password, name='forgot_password'),                        
    path('reset_password', reset_password, name='reset_password'),    

    path('add_project', add_project, name='add_project'),    
    path('update_project', update_project, name='update_project'),        
    path('delete_project/<str:project_id>', delete_project, name='delete_project'),        
    path('get_projects/<str:user_id>', get_projects, name='get_projects'),    

    path('add_experience', add_experience, name='add_experience'),    
    path('update_experience', update_experience, name='update_experience'),        
    path('delete_experience/<str:experience_id>', delete_experience, name='delete_experience'),        
    path('get_experiences/<str:user_id>', get_experiences, name='get_experiences'),    

    
    path('update_socials', update_socials, name='update_socials'),        
    path('get_user/<str:email>', get_user, name='get_user'),        


    path('add_skill', add_skill, name='add_skill'),    
    path('update_skill', update_skill, name='update_skill'),        
    path('delete_skill/<str:skill_id>', delete_skill, name='delete_skill'),        
    path('get_skills/<str:user_id>', get_skills, name='get_skills'),    
    
]