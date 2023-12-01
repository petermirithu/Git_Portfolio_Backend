from django.urls import path
from .views import *

urlpatterns = [    
    # APIs for all users
    path('sign_up_user', sign_up_user, name='sign_up_user'),    
    path('sign_in_user', sign_in_user, name='sign_in_user'),                        
    path('forgot_password', forgot_password, name='forgot_password'),                        
    path('reset_password', reset_password, name='reset_password'),    
]