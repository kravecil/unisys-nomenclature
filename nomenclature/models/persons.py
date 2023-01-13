from nomenclature.services import get_user_by_auth_id

class Person():
    pk = None
    username = None
    lastname = None
    firstname = None
    middlename = None
    
    class Meta(object):
        app_label = 'nomenclature'

    def __init__(self, id, token = None):
        user = get_user_by_auth_id(id)
        if user:
            self.pk = user['id']
            self.username = user['username']
            self.lastname = user['lastname']
            self.firstname = user['firstname']
            self.middlename = user['middlename']

    def __bool__(self):
        return self.pk is not None

    def __str__(self):
        return self.get_shortname()

    def get_shortname(self):
        return "%s %s.%s." % (
            self.lastname or '',
            self.firstname and self.firstname[0],
            self.middlename and self.middlename[0]
        )
