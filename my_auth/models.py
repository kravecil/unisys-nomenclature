# from django.contrib.auth.models import User

class AuthUser():
    is_active = True
    
    def __init__(self, payload):
        self.id = payload['id']
        self.username = payload['username']
        self.permissions = payload['permissions']

        self.is_authenticated = True

    def has_perm(permission):
        pass

    def is_active(self):
        return True
