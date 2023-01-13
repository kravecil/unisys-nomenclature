from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.urls import resolve

class AuthMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ## before

        if resolve(request.path).namespace == 'api_path':       
            # if request.user is None:
            user = authenticate(request)

            if user is None:
                return HttpResponse('Authentication required!', status=401)

            request.auth_user = user
            # login(request, user)

        response = self.get_response(request)

        ## after

        return response