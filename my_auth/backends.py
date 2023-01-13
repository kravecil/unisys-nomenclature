from django.contrib.auth.backends import BaseBackend
import requests
from django.conf import settings
from .models import AuthUser

class AuthBackend (BaseBackend):
    # def get_user (self, user_id):
    #     user = None #somehow_create_an_instance_of (MyUser, user_id)
    #     return user

    def authenticate (self, request, token=None):
        response = requests.post(
            settings.HOST_AUTH + '/api/token',
            headers={
                'Authorization': request.headers['Authorization'],
                'Accept': 'application/json',
            }
        )

        # print ('USER: ', response.json())
        try:
            user = AuthUser(response.json()) 
            return user
        except Exception as e:
            None