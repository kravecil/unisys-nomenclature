from django.db import models

class Approver(models.Model):
    auth_id = models.PositiveBigIntegerField()
    
    class Meta(object):
        app_label = 'nomenclature'
